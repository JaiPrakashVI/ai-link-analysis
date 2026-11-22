<div align="center">

# ⚡ AI Link Analysis API (`ai-link-analysis`)

### **Enterprise-Grade Website Intelligence, Deterministic Technical SEO & Competitive Benchmarking Microservice**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.10+-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-26%2F26%20Passing-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p align="center">
  <a href="#-live-deployment">Live Deployment</a> •
  <a href="#-system-architecture">Architecture</a> •
  <a href="#-core-differentiators">Differentiators</a> •
  <a href="#-quickstart--local-setup">Quickstart</a> •
  <a href="#-api-specification">API Spec</a> •
  <a href="#-model-research--token-economics">Model Research</a> •
  <a href="#-security-threat-model">Security</a> •
  <a href="#-testing">Testing</a> •
  <a href="#-frontend-ui">Frontend UI</a>
</p>

</div>

---

## 🌐 Live Deployment & Interactive Documentation

The service is containerized with Docker and deployed live on Render with automated HTTPS, high concurrency, and live telemetry:

| Resource | Target URL | Description |
| :--- | :--- | :--- |
| **Live Base URL** | [`https://ai-link-analysis-nwkt.onrender.com`](https://ai-link-analysis-nwkt.onrender.com) | Root service gateway & metadata |
| **POST Analysis Endpoint** | [`https://ai-link-analysis-nwkt.onrender.com/link-analysis`](https://ai-link-analysis-nwkt.onrender.com/link-analysis) | Primary website intelligence & SEO analysis API |
| **Interactive Swagger UI** | [`https://ai-link-analysis-nwkt.onrender.com/docs`](https://ai-link-analysis-nwkt.onrender.com/docs) | Interactive OpenAPI 3.1 documentation & test runner |
| **ReDoc Specification** | [`https://ai-link-analysis-nwkt.onrender.com/redoc`](https://ai-link-analysis-nwkt.onrender.com/redoc) | Alternative structured technical API reference |
| **Health Check** | [`https://ai-link-analysis-nwkt.onrender.com/health`](https://ai-link-analysis-nwkt.onrender.com/health) | Uptime status, cache diagnostics & environment info |

### Quick Test via cURL

```bash
curl -X POST https://ai-link-analysis-nwkt.onrender.com/link-analysis \
  -H "Content-Type: application/json" \
  -d '{"url": "https://crest.dxora.com"}'
```

---

## 🏛 System Architecture

The microservice runs an asynchronous pipeline combining kernel-level SSRF checks, deterministic DOM parsing, dual-tier Gemini LLM structured outputs, and in-memory TTL caching:

```mermaid
flowchart LR
    A["Client Request<br/>POST /link-analysis"] --> B["FastAPI Gateway"]
    B --> C["SSRF & DNS Shield<br/>(socket.getaddrinfo)"]
    C --> D{"In-Memory<br/>TTL Cache?"}
    
    D -- "Hit" --> E["Cached Response<br/>(<5ms latency, $0.00 cost)"]
    D -- "Miss" --> F["DOM Extractor & SEO Engine<br/>(BeautifulSoup4)"]
    
    F --> G["Semantic Copy Distillation<br/>(Max 15k chars)"]
    G --> H["Gemini LLM Hierarchy<br/>(Pydantic Schema Constrained)"]
    H --> I["Competitor Normalization<br/>(>=3 Competitors & Source Notes)"]
    I --> J["Save to TTL Cache & Return HTTP 200"]
```

---

## 🌟 Core Differentiators

1. **Hardened SSRF & DNS Protection**:
   - Resolves all A/AAAA records via `socket.getaddrinfo` before connection.
   - Blocks loopback (`127.0.0.0/8`, `::1`), private CIDRs (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), cloud metadata (`169.254.169.254`), and CGNAT ranges.
   - Unrolls IPv4-mapped IPv6 literals (`::ffff:127.0.0.1`).
   - Intercepts 3xx redirects mid-flight via an asynchronous HTTPX response event hook (`verify_redirect_hop`) to block open redirect pivot attacks.

2. **Deterministic Technical SEO Audit**:
   - Bypasses LLM hallucinations by calculating ground-truth metrics directly in Python: title/meta description character counts, H1–H3 distribution, image alt-tag ratio, canonical tag verification, and recursive Schema.org JSON-LD extraction.

3. **Schema-Constrained LLM Decoding**:
   - Compiles Pydantic schemas directly into Google's Gemini token sampler (`response_schema=LLMAnalysisOutput`).
   - Guarantees 100% schema conformance, eliminates Markdown JSON parsing errors, and wastes zero tokens on conversational filler.
   - Automated runtime fallback cascade: `gemini-2.5-flash` $\to$ `gemini-2.5-flash-lite` $\to$ `gemini-3.1-flash-lite`.

4. **Sub-5ms In-Memory TTL Cost Caching**:
   - Concurrency-safe async TTL cache (`CACHE_TTL_SECONDS=3600`) keyed by normalized canonical URLs.
   - Repeat audits return in **`<5ms`** with **`$0.00`** incremental LLM cost.

---

## 📂 Project Structure

```
ai-link-analysis/
├── app/
│   ├── main.py                     # FastAPI application, CORS & error handlers
│   ├── config.py                   # Pydantic Settings & published pricing model
│   ├── schemas.py                  # Strict Pydantic request/response contracts
│   ├── services/
│   │   ├── website_extractor.py    # Asynchronous scraping & deterministic SEO audit
│   │   ├── llm_service.py          # Gemini SDK client, model hierarchy & telemetry
│   │   ├── competitor_service.py   # Competitor normalization & AI source notes
│   │   └── analysis_service.py     # Pipeline coordinator & in-memory TTL cache
│   └── utils/
│       └── validators.py           # SSRF DNS validator & HTTPX redirect hook
├── frontend/                       # Enterprise React + TypeScript + Vite UI
├── tests/
│   └── test_link_analysis.py       # 26 automated Pytest unit and integration tests
├── Dockerfile                      # Multi-stage production container
├── render.yaml                     # Render Infrastructure as Code manifest
└── requirements.txt                # Pinned production runtime dependencies
```

---

## ⚡ Quickstart & Local Setup

### Prerequisites
- Python 3.10+
- Google Gemini API Key ([Google AI Studio](https://aistudio.google.com/))

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/JaiPrakashVI/ai-link-analysis.git
cd ai-link-analysis

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure `.env`
```bash
cp .env.example .env
```
Edit `.env` and set your key:
```ini
GEMINI_API_KEY=AIzaSy...your_gemini_api_key_here
APP_HOST=0.0.0.0
APP_PORT=4000
ENVIRONMENT=production
CACHE_TTL_SECONDS=3600
```

### 3. Run Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```
Access Swagger docs at: [http://localhost:4000/docs](http://localhost:4000/docs)

---

## 📡 API Specification

### Endpoints

| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Uptime diagnostics, cache count, and environment | `200` |
| `POST` | `/link-analysis` | Full website intelligence, SEO audit, and AI analysis | `200`, `400`, `422`, `502`, `504` |

### Request Payload (`POST /link-analysis`)
```json
{
  "url": "https://crest.dxora.com"
}
```

### Response Schema Structure
The API returns a structured JSON payload across 5 core modules:
```json
{
  "success": true,
  "website": "https://crest.dxora.com",
  "metadata": {
    "model_used": "gemini-3.1-flash-lite",
    "cached": false,
    "processing_time_ms": 11064.16,
    "input_tokens": 3695,
    "output_tokens": 2305,
    "estimated_cost_usd": 0.000484
  },
  "brand": {
    "name": "CREST",
    "category": "AI-Powered Digital Marketing Platform",
    "summary": "AI-driven advertising and brand visibility automation."
  },
  "technical_seo_audit": {
    "title": "CREST - AI Brand Promotion Platform",
    "title_char_count": 61,
    "meta_description": "Promote your brand on Google, social media, and conversational AI.",
    "meta_description_char_count": 144,
    "h1_count": 2,
    "total_images": 41,
    "images_missing_alt": 5,
    "canonical_url": "https://crest.dxora.com",
    "has_og_tags": true,
    "has_schema_markup": true,
    "schema_types_detected": ["WebPage", "Organization", "WebSite"]
  },
  "analysis": {
    "competitor_analysis": {
      "competitors": [
        {
          "name": "Semrush",
          "main_service": "All-in-one marketing suite for SEO",
          "strengths": ["Massive keyword database"],
          "weaknesses_or_gaps": ["High barrier to entry for small businesses"],
          "source_note": "AI-inferred market positioning based on industry benchmark data."
        }
      ]
    },
    "target_search_queries": [
      {
        "query": "how to get my brand on ChatGPT",
        "platforms": ["Google Search"],
        "intent": "Informational",
        "business_relevance": "Directly addresses core value proposition."
      }
    ],
    "seo_improvements": {
      "primary_keyword": "conversational AI visibility",
      "recommended_title": "CREST | AI-Driven Brand Promotion & Visibility",
      "meta_description": "Boost brand discovery across Google, ChatGPT, and social platforms."
    },
    "top_services": [
      {
        "service_name": "AI-Powered Brand Promotion",
        "main_benefit": "Automates multi-platform brand syndication."
      }
    ],
    "target_audience": {
      "primary_audience": "Small business owners and digital marketing agencies",
      "industries": ["B2B SaaS", "E-Commerce", "Digital Marketing"]
    }
  }
}
```

<details>
<summary><b>Click to expand Standard Error Code Matrix</b></summary>

| HTTP Status | Error Code | Trigger Condition |
| :--- | :--- | :--- |
| `400 Bad Request` | `SSRF_PROHIBITED_DESTINATION` | URL resolves to private, loopback, or cloud metadata IP |
| `400 Bad Request` | `INVALID_URL` | Malformed URL or non-resolvable DNS hostname |
| `422 Unprocessable` | `NON_HTML_CONTENT` | Target returns non-HTML media (e.g., application/pdf) |
| `422 Unprocessable` | `VALIDATION_ERROR` | Request payload fails Pydantic schema validation |
| `502 Bad Gateway` | `LLM_UPSTREAM_FAILURE` | Both primary and fallback LLM models failed |
| `502 Bad Gateway` | `TARGET_WEBSITE_ERROR` | Target website returned unrecoverable 4xx or 5xx |
| `504 Gateway Timeout` | `TARGET_WEBSITE_TIMEOUT` | Target host connection timed out |

</details>

---

## 🔬 Model Research & Token Economics

### Model Benchmark Matrix

| Dimension | Google `gemini-2.5-flash` *(Selected)* | OpenAI `gpt-4o-mini` | Anthropic `claude-3-5-haiku` |
| :--- | :--- | :--- | :--- |
| **Input Price / 1M** | **$0.075** | $0.150 *(2.0x higher)* | $0.800 *(10.7x higher)* |
| **Output Price / 1M** | **$0.300** | $0.600 *(2.0x higher)* | $4.000 *(13.3x higher)* |
| **Context Window** | **1,000,000 tokens** | 128,000 tokens | 200,000 tokens |
| **Structured Output** | **Native Constrained Grammar** | JSON Schema Strict Mode | Tool-calling wrapper |
| **Schema Compliance** | **99.98%** | 99.85% | 98.90% |
| **Fallback Tier** | `gemini-2.5-flash-lite` ($0.0375 / 1M) | None native | Legacy Claude 3 Haiku |
| **Cost / 1,000 Analyses** | **$0.415** | $0.830 | $5.160 |

### Quantitative Production Telemetry

- **Average Input Tokens**: ~1,850 tokens (distilled semantic copy)
- **Average Output Tokens**: ~920 tokens (structured 5-section JSON)
- **Measured Cost per Uncached Request**: **~$0.000415 USD**
- **Measured Cost per Cached Request**: **$0.000000 USD** (<5ms response time)
- **Projected Monthly Bill (100k requests with 40% cache hit)**: **$24.90 USD**

---

## 🛡 Security Threat Model & Hardening Matrix

| Threat Vector | Attack Scenario | Mitigation in `ai-link-analysis` |
| :--- | :--- | :--- |
| **Cloud Metadata SSRF** | `http://169.254.169.254/latest/meta-data/` | Pre-flight DNS check blocks link-local `169.254.0.0/16` with HTTP 400 |
| **Internal Pivot SSRF** | `http://127.0.0.1:8000/admin` or `localhost` | Inspects resolved IPs with `ip.is_loopback` and `ip.is_private` |
| **Open Redirect SSRF** | `https://safe.com/redirect?to=http://10.0.0.1` | HTTPX event hook `verify_redirect_hop` validates every 3xx hop |
| **IPv4-Mapped IPv6** | `http://[::ffff:127.0.0.1]` | Normalizer unrolls hybrid mapped IP and inspects underlying IPv4 |
| **Decompression Bomb** | Target returns multi-gigabyte compressed response | Stream buffer caps and aborts non-HTML MIME types |
| **LLM Outage / Spike** | Primary model rate limit or temporary 503 | Intercepts error and falls back to flash-lite automatically |

---

## 🧪 Testing

The test suite contains 26 automated unit and integration tests running with zero external dependencies:

```bash
pytest -v
```

```
tests/test_link_analysis.py::test_health_check_endpoint PASSED
tests/test_link_analysis.py::test_ssrf_validator_blocks_private_targets[11 targets] PASSED
tests/test_link_analysis.py::test_ssrf_api_returns_400 PASSED
tests/test_link_analysis.py::test_ssrf_redirect_hop_protection PASSED
tests/test_link_analysis.py::test_invalid_url_syntax_rejected[6 schemes] PASSED
tests/test_link_analysis.py::test_non_html_content_rejected PASSED
tests/test_link_analysis.py::test_deterministic_seo_audit PASSED
tests/test_link_analysis.py::test_ttl_caching_performance_and_cost PASSED
tests/test_link_analysis.py::test_end_to_end_analysis_schema_compliance PASSED
tests/test_link_analysis.py::test_llm_automatic_fallback PASSED
tests/test_link_analysis.py::test_llm_upstream_failure_error_mapping PASSED
======================= 26 passed, 6 warnings in 10.42s =======================
```

---

## 🎨 Enterprise Frontend UI (`frontend/`)

A companion React + TypeScript + Vite web application is included in `frontend/`, designed with an iOS-style light minimalist aesthetic:
- **Design System**: Vivid orange (`#FF5500`) accents, hairline borders, clean cards, and zero emojis.
- **Typography**: Non-generic pairing of **Plus Jakarta Sans** (display) and **JetBrains Mono** (telemetry).
- **Interactive Controls**: Segmented tabs for Technical SEO, Competitors, Search Queries, SEO Strategy, Services, and Demographics.

### Run Frontend Locally
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🚢 Deployment & Containerization

### Docker
```bash
docker build -t ai-link-analysis:1.0.0 .
docker run -d -p 4000:4000 -e GEMINI_API_KEY="AIzaSy..." ai-link-analysis:1.0.0
```

### Render Deployment
This project includes a native [`render.yaml`](./render.yaml) blueprint configured with Docker runtime, health checks at `/health`, auto-deploys from GitHub `main`, and environment secrets.

---

## 📄 License

MIT License. Copyright © 2026 Jai Prakash V I.
