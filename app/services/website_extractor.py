"""High-signal website content extraction and deterministic technical SEO auditing."""

import json
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlsplit
import httpx
from bs4 import BeautifulSoup, Tag

from app.config import get_settings
from app.schemas import TechnicalSeoAudit
from app.utils.validators import validate_url_for_ssrf, verify_redirect_hop

logger = logging.getLogger(__name__)


class WebsiteExtractionError(Exception):
    """Base exception for errors encountered during website ingestion."""
    pass


class NonHtmlContentError(WebsiteExtractionError):
    """Raised when the fetched URL does not deliver HTML content."""
    pass


class WebsiteTimeoutError(WebsiteExtractionError):
    """Raised when fetching the target website times out."""
    pass


class WebsiteHTTPError(WebsiteExtractionError):
    """Raised when the target website returns an unrecoverable HTTP status code."""
    def __init__(self, status_code: int, message: str):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code


class ExtractedWebsiteData:
    """Encapsulates extracted SEO audit metrics and high-signal LLM text payload."""

    def __init__(
        self,
        audit: TechnicalSeoAudit,
        distilled_content: str,
        final_url: str,
    ):
        self.audit = audit
        self.distilled_content = distilled_content
        self.final_url = final_url


class WebsiteExtractor:
    """Asynchronous website downloader, parser, and deterministic SEO auditor."""

    def __init__(self):
        self.settings = get_settings()
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/128.0.0.0 Safari/537.36 (ai-link-analysis/1.0)"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
        }

    async def fetch_html(self, url: str) -> Tuple[str, int, str]:
        """Fetch raw HTML from target URL while enforcing SSRF validations and redirect safety.

        Returns:
            Tuple of (html_text, status_code, final_url)
        """
        # Validate initial URL
        validated_url = validate_url_for_ssrf(url)

        timeout = httpx.Timeout(
            timeout=self.settings.REQUEST_TIMEOUT_SECONDS,
            connect=5.0,
        )

        limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)

        async with httpx.AsyncClient(
            timeout=timeout,
            limits=limits,
            headers=self.headers,
            follow_redirects=True,
            max_redirects=self.settings.MAX_REDIRECTS,
            event_hooks={"response": [verify_redirect_hop]},
        ) as client:
            try:
                response = await client.get(validated_url)
            except httpx.TimeoutException as exc:
                logger.warning("Timeout fetching URL %s: %s", validated_url, exc)
                raise WebsiteTimeoutError(
                    f"Connection timed out after {self.settings.REQUEST_TIMEOUT_SECONDS}s while reaching {validated_url}."
                ) from exc
            except httpx.RequestError as exc:
                logger.error("Request error fetching URL %s: %s", validated_url, exc)
                raise WebsiteExtractionError(f"Network request error reaching target URL: {exc}") from exc

            # Verify content-type
            content_type = response.headers.get("content-type", "").lower()
            if not ("text/html" in content_type or "application/xhtml+xml" in content_type):
                raise NonHtmlContentError(
                    f"Target URL returned non-HTML media type '{content_type}'. "
                    "Link analysis requires an HTML webpage."
                )

            # Check HTTP status
            if response.status_code >= 400:
                raise WebsiteHTTPError(
                    response.status_code,
                    f"Target website returned error status code {response.status_code}."
                )

            return response.text, response.status_code, str(response.url)

    def parse_and_audit(
        self,
        html: str,
        url: str,
        status_code: int = 200,
    ) -> ExtractedWebsiteData:
        """Parse raw HTML, calculate deterministic SEO metrics, and extract high-signal content."""
        soup = BeautifulSoup(html, "html.parser")
        parsed_base = urlsplit(url)
        base_domain = parsed_base.netloc.lower()

        # 1. Document Title
        title_tag = soup.find("title")
        title_text = title_tag.get_text(strip=True) if title_tag else None
        title_char_count = len(title_text) if title_text else 0

        # 2. Meta Description
        meta_desc_tag = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "description"})
        if not meta_desc_tag:
            meta_desc_tag = soup.find("meta", attrs={"property": lambda x: x and x.lower() == "description"})
        meta_desc = meta_desc_tag.get("content", "").strip() if meta_desc_tag else None
        if meta_desc == "":
            meta_desc = None
        meta_desc_char_count = len(meta_desc) if meta_desc else 0

        # 3. Canonical Link
        canonical_tag = soup.find("link", rel=lambda x: x and "canonical" in [item.lower() for item in x.split()])
        canonical_url = None
        if canonical_tag and canonical_tag.get("href"):
            canonical_url = urljoin(url, canonical_tag.get("href").strip())

        # 4. OpenGraph Tags
        og_tags: Dict[str, str] = {}
        for tag in soup.find_all("meta"):
            prop = tag.get("property") or tag.get("name")
            content = tag.get("content")
            if prop and content and prop.lower().startswith("og:"):
                og_tags[prop.lower()] = content.strip()
        has_og_tags = len(og_tags) > 0

        # 5. Schema.org / JSON-LD structured data
        schema_types: List[str] = []
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            raw_json = script.string or script.get_text()
            if not raw_json:
                continue
            try:
                data = json.loads(raw_json)
                self._extract_schema_types(data, schema_types)
            except Exception:
                # Ignore malformed JSON-LD snippets
                pass
        unique_schema_types = sorted(list(set(schema_types)))
        has_schema_markup = len(unique_schema_types) > 0

        # 6. Headings
        h1_elements = soup.find_all("h1")
        h1_tags = [h.get_text(" ", strip=True) for h in h1_elements if h.get_text(strip=True)]
        h1_count = len(h1_tags)

        h2_elements = soup.find_all("h2")
        h2_count = len([h for h in h2_elements if h.get_text(strip=True)])

        h3_elements = soup.find_all("h3")
        h3_count = len([h for h in h3_elements if h.get_text(strip=True)])

        # 7. Images & Alt attributes
        img_tags = soup.find_all("img")
        total_images = len(img_tags)
        images_with_alt = 0
        for img in img_tags:
            alt_val = img.get("alt")
            if alt_val is not None and alt_val.strip() != "":
                images_with_alt += 1
        images_missing_alt = total_images - images_with_alt

        # 8. Internal Navigation Links
        internal_links = set()
        nav_containers = soup.find_all(["nav", "header"])
        candidate_anchors = []
        for container in nav_containers:
            candidate_anchors.extend(container.find_all("a", href=True))
        if not candidate_anchors:
            candidate_anchors = soup.find_all("a", href=True)

        for a in candidate_anchors:
            href = a.get("href", "").strip()
            anchor_text = a.get_text(" ", strip=True)
            if not href or not anchor_text or href.startswith("#") or href.startswith("javascript:"):
                continue

            full_href = urljoin(url, href)
            target_domain = urlsplit(full_href).netloc.lower()

            if target_domain == "" or target_domain == base_domain:
                if 2 <= len(anchor_text) <= 40:
                    internal_links.add(anchor_text)
                    if len(internal_links) >= 15:
                        break

        internal_nav_links = sorted(list(internal_links))

        # 9. Distill High-Signal Content for LLM
        distilled_text = self._distill_content_for_llm(soup, title_text, meta_desc)
        content_char_count = len(distilled_text)

        # Assemble Technical SEO Audit
        audit = TechnicalSeoAudit(
            title=title_text,
            title_char_count=title_char_count,
            meta_description=meta_desc,
            meta_description_char_count=meta_desc_char_count,
            h1_count=h1_count,
            h1_tags=h1_tags,
            h2_count=h2_count,
            h3_count=h3_count,
            total_images=total_images,
            images_missing_alt=images_missing_alt,
            images_with_alt=images_with_alt,
            internal_nav_links=internal_nav_links,
            canonical_url=canonical_url,
            has_og_tags=has_og_tags,
            og_tags=og_tags,
            has_schema_markup=has_schema_markup,
            schema_types_detected=unique_schema_types,
            content_char_count=content_char_count,
            status_code=status_code,
        )

        return ExtractedWebsiteData(
            audit=audit,
            distilled_content=distilled_text,
            final_url=url,
        )

    def _extract_schema_types(self, item, types_accumulator: List[str]) -> None:
        """Recursively walk JSON-LD structures to harvest all @type annotations."""
        if isinstance(item, dict):
            if "@type" in item:
                val = item["@type"]
                if isinstance(val, str):
                    types_accumulator.append(val)
                elif isinstance(val, list):
                    for v in val:
                        if isinstance(v, str):
                            types_accumulator.append(v)
            if "@graph" in item and isinstance(item["@graph"], list):
                for node in item["@graph"]:
                    self._extract_schema_types(node, types_accumulator)
            for v in item.values():
                if isinstance(v, (dict, list)):
                    self._extract_schema_types(v, types_accumulator)
        elif isinstance(item, list):
            for element in item:
                self._extract_schema_types(element, types_accumulator)

    def _distill_content_for_llm(
        self,
        soup: BeautifulSoup,
        title: Optional[str],
        meta_desc: Optional[str],
    ) -> str:
        """Strip non-semantic markup and extract deduplicated high-signal text within budget."""
        # Create a working copy
        working_soup = BeautifulSoup(str(soup), "html.parser")

        # Strip unneeded structural & decorative tags
        for unwanted in working_soup(
            ["script", "style", "noscript", "svg", "iframe", "link", "meta", "template", "footer"]
        ):
            unwanted.decompose()

        lines: List[str] = []

        if title:
            lines.append(f"# Document Title: {title}")
        if meta_desc:
            lines.append(f"## Meta Description: {meta_desc}")

        seen_blocks = set()

        # Prioritize key content containers if available
        content_root = (
            working_soup.find("main")
            or working_soup.find("article")
            or working_soup.find("body")
            or working_soup
        )

        # Iterate over semantic content nodes
        for element in content_root.find_all(["h1", "h2", "h3", "h4", "p", "li", "span", "div"]):
            tag_name = element.name.lower()
            text = element.get_text(" ", strip=True)

            if not text or len(text) < 15:
                continue

            # Skip if this element is already a parent or child of a processed block
            normalized_block = " ".join(text.split()).lower()
            if normalized_block in seen_blocks:
                continue
            seen_blocks.add(normalized_block)

            if tag_name == "h1":
                lines.append(f"\n# {text}")
            elif tag_name == "h2":
                lines.append(f"\n## {text}")
            elif tag_name == "h3":
                lines.append(f"\n### {text}")
            elif tag_name == "li":
                lines.append(f"* {text}")
            else:
                lines.append(text)

            # Check character accumulation
            current_length = sum(len(line) + 1 for line in lines)
            if current_length >= self.settings.MAX_CONTENT_CHARS:
                break

        final_text = "\n".join(lines)
        if len(final_text) > self.settings.MAX_CONTENT_CHARS:
            final_text = final_text[: self.settings.MAX_CONTENT_CHARS].rsplit(" ", 1)[0] + "..."

        return final_text
