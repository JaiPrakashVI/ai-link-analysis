"""Hardened SSRF Protection and URL Validation Engine."""

import ipaddress
import socket
from typing import Tuple, Union, Optional
from urllib.parse import urlsplit, urlunsplit
import httpx


class SSRFError(Exception):
    """Raised when an outbound URL resolves to a prohibited internal or private network destination."""
    pass


class InvalidURLError(Exception):
    """Raised when a provided URL fails syntactic or protocol specifications."""
    pass


# Specific RFC non-routable / carrier / benchmarking subnets
_PROHIBITED_EXTRA_NETWORKS = [
    ipaddress.ip_network("100.64.0.0/10"),     # RFC 6598 Shared Carrier CGNAT
    ipaddress.ip_network("198.18.0.0/15"),     # RFC 2544 Benchmarking
    ipaddress.ip_network("192.0.0.0/24"),      # RFC 6890 IETF Protocol Assignments
    ipaddress.ip_network("192.0.2.0/24"),      # RFC 5737 TEST-NET-1
    ipaddress.ip_network("198.51.100.0/24"),   # RFC 5737 TEST-NET-2
    ipaddress.ip_network("203.0.113.0/24"),    # RFC 5737 TEST-NET-3
    ipaddress.ip_network("240.0.0.0/4"),       # RFC 1112 Reserved
]


def normalize_url(url: str) -> str:
    """Normalize URL by stripping whitespace, downcasing scheme/hostname, and removing default ports."""
    url = url.strip()
    if not url:
        raise InvalidURLError("URL string cannot be empty.")

    try:
        parts = urlsplit(url)
    except Exception as exc:
        raise InvalidURLError(f"Malformed URL structure: {exc}") from exc

    scheme = parts.scheme.lower()
    if scheme not in ("http", "https"):
        raise InvalidURLError(f"Unsupported scheme '{scheme}'. Only http and https are permitted.")

    if not parts.netloc:
        raise InvalidURLError("URL must contain a valid host identifier.")

    if parts.username or parts.password:
        raise InvalidURLError("Userinfo or embedded credentials in URL are strictly prohibited.")

    hostname = parts.hostname
    if not hostname:
        raise InvalidURLError("Host could not be extracted from URL.")
    hostname = hostname.lower()

    # Format host properly for IPv6 literals (which require brackets)
    formatted_host = f"[{hostname}]" if ":" in hostname else hostname

    # Reconstitute netloc without default ports
    port = parts.port
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        netloc = formatted_host
    elif port is not None:
        netloc = f"{formatted_host}:{port}"
    else:
        netloc = formatted_host

    # Ensure path has at least a root slash
    path = parts.path or "/"

    return urlunsplit((scheme, netloc, path, parts.query, parts.fragment))


def is_ip_prohibited(ip: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]) -> Tuple[bool, str]:
    """Inspect IP address against all internal, private, loopback, and reserved ranges."""
    # Unwrap IPv4-mapped IPv6 addresses (e.g. ::ffff:127.0.0.1)
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        ip = ip.ipv4_mapped

    if ip.is_loopback:
        return True, "loopback address"
    if ip.is_private:
        return True, "private RFC 1918 / RFC 4193 network"
    if ip.is_link_local:
        return True, "link-local address (including cloud metadata services)"
    if ip.is_multicast:
        return True, "multicast range"
    if ip.is_reserved:
        return True, "IETF reserved network"
    if ip.is_unspecified:
        return True, "unspecified 0.0.0.0 or :: address"

    for prohibited_net in _PROHIBITED_EXTRA_NETWORKS:
        if isinstance(ip, ipaddress.IPv4Address) and ip in prohibited_net:
            return True, f"prohibited special subnet ({prohibited_net})"

    return False, ""


def validate_url_for_ssrf(url: str) -> str:
    """Perform full DNS resolution and SSRF validation on target URL.

    Raises:
        InvalidURLError: For malformed URLs or unreachable DNS names.
        SSRFError: If destination resolves to any private, loopback, or internal IP.

    Returns:
        The normalized URL string if safe.
    """
    normalized = normalize_url(url)
    parts = urlsplit(normalized)
    hostname = parts.hostname

    if not hostname:
        raise InvalidURLError("URL must contain a valid hostname.")

    # Check for direct prohibited names
    lower_host = hostname.lower()
    if lower_host in ("localhost", "localhost.localdomain", "broadcasthost", "internal"):
        raise SSRFError(f"Access to host '{hostname}' is blocked by SSRF policy (restricted hostname).")
    if lower_host.endswith(".localhost") or lower_host.endswith(".local") or lower_host.endswith(".internal"):
        raise SSRFError(f"Access to host '{hostname}' is blocked by SSRF policy (restricted domain suffix).")

    # If host is an IP literal
    try:
        ip_obj = ipaddress.ip_address(hostname)
        prohibited, reason = is_ip_prohibited(ip_obj)
        if prohibited:
            raise SSRFError(f"Access to IP '{hostname}' ({reason}) is blocked by SSRF policy.")
        return normalized
    except ValueError:
        # Not an IP literal, proceeds to DNS resolution
        pass

    # Resolve all DNS records
    target_port = parts.port or (443 if parts.scheme == "https" else 80)
    try:
        addr_info = socket.getaddrinfo(
            hostname,
            target_port,
            proto=socket.IPPROTO_TCP,
        )
    except socket.gaierror as exc:
        raise InvalidURLError(f"DNS resolution failed for host '{hostname}': {exc.strerror or exc}") from exc
    except Exception as exc:
        raise InvalidURLError(f"DNS resolution error for host '{hostname}': {exc}") from exc

    if not addr_info:
        raise InvalidURLError(f"Host '{hostname}' resolved to no valid network addresses.")

    for item in addr_info:
        sockaddr = item[4]
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            continue

        prohibited, reason = is_ip_prohibited(ip_obj)
        if prohibited:
            raise SSRFError(
                f"DNS resolved host '{hostname}' to prohibited IP address '{ip_str}' ({reason}). "
                "Blocked by SSRF protection policy."
            )

    return normalized


async def verify_redirect_hop(response: httpx.Response) -> None:
    """Async event hook for HTTPX to validate every redirect hop against SSRF rules.

    Instantly aborts redirection if the target Location header points to a private or
    loopback destination, neutralizing open redirect exploits.
    """
    if response.is_redirect:
        location = response.headers.get("Location")
        if not location:
            return

        # Resolve relative redirects against current response URL
        target_url = str(response.url.join(location))
        validate_url_for_ssrf(target_url)
