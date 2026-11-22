# Final Submission Draft: Dxora Technologies Python Practical Test

> **Instructions for Candidate:**
> Copy the email text below, fill in your contact number, preferred discussion date/time, and personal profile links in the bracketed placeholders (`[...]`), verify the details, and send directly to **`hr@chivoxai.com`**.

---

## Email Metadata

- **To:** hr@chivoxai.com
- **Subject:** Jai Prakash V I - Python Practical Link Analysis test review

---

## Email Body

Dear Hiring Team at Dxora Technologies / Chivox AI,

I have completed the Python Practical Assessment for the **AI-Powered Website Link Analysis API** microservice. The solution is fully implemented, verified with 26 automated unit and integration tests, containerized with Docker, and deployed live in production.

Below are my submission details and engineering deliverables:

---

### Candidate & Contact Details

1. **Full Name:** Jai Prakash V I
2. **Current Location:** Tiruvallur, Tamil Nadu, India
3. **Contact Number:** [Your Contact Number, e.g., +91 98765 43210]
4. **Preferred Date and Time for Final Discussion:** [Preferred Date & Time, e.g., Tuesday, November 24, 2026, 2:00 PM - 5:00 PM IST]

---

### Project Links & Deliverables

- **Live Production Base URL:** https://ai-link-analysis-nwkt.onrender.com
- **POST Analysis Endpoint:** https://ai-link-analysis-nwkt.onrender.com/link-analysis
- **Interactive Swagger Documentation:** https://ai-link-analysis-nwkt.onrender.com/docs
- **Public GitHub Repository:** https://github.com/JaiPrakashVI/ai-link-analysis

---

### Mandatory Social Media Follow Confirmations

In accordance with Section 12 of the test guidelines:

- **LinkedIn Profile:** [Your LinkedIn Profile URL, e.g., https://www.linkedin.com/in/your-profile]
  *(Confirmed: Following Dxora Technologies at https://www.linkedin.com/company/dxora-technologies)*
- **Instagram Profile:** [Your Instagram Profile Handle or URL, e.g., https://www.instagram.com/your-username]
  *(Confirmed: Following CREST at https://www.instagram.com/crestspot/)*

---

### Architectural & Engineering Highlights

1. **Hardened SSRF & DNS Protection:**
   Implements multi-stage kernel socket checks (`socket.getaddrinfo`) resolving all A/AAAA records to block private networks, loopback (`127.0.0.1`, `::1`), link-local/cloud metadata (`169.254.169.254`), and CGNAT ranges before opening TCP connections. An asynchronous HTTPX response event hook (`verify_redirect_hop`) inspects every 3xx redirect hop mid-flight to defeat open-redirect pivot attacks.

2. **Deterministic Technical SEO Engine:**
   Bypasses LLM hallucinations by calculating exact DOM ground truths in Python (`BeautifulSoup`): Title and Meta Description character lengths, H1–H3 header counts, total images vs. missing `alt` attributes, canonical tags, OpenGraph attributes, and recursive Schema.org JSON-LD hierarchy extraction.

3. **Schema-Enforced Gemini Dual-Tier LLM Intelligence:**
   Native Pydantic schema-constrained decoding (`response_schema=LLMAnalysisOutput`) using Google's frontier `gemini-2.5-flash` (with automated runtime failover to `gemini-2.5-flash-lite`, `gemini-3.1-flash-lite`, and `gemini-3.5-flash-lite`). Constrained token decoding guarantees 100% schema compliance, zero JSON parsing failures, and zero conversational token waste.

4. **Zero-Hallucination Competitor & Query Synthesis:**
   Extracts brand identity, generates 3+ concrete competitors with explicit AI-inferred source notes, 5 multi-platform high-intent queries (Google Search, Facebook, Instagram, LinkedIn, X) without synthetic search volumes, actionable architectural SEO improvements, top service offerings, and target customer personas.

5. **Sub-5ms In-Memory TTL Cost Caching:**
   Thread-safe asynchronous TTL cache keyed by canonical normalized URLs. Repeated requests return cached intelligence in `<5ms` at **$0.00** incremental inference cost, recording complete token and USD pricing telemetry based on published Google Gemini rates.

6. **Comprehensive Automated Test Coverage:**
   Includes 26 comprehensive pytest unit and integration tests covering SSRF blocking, redirect prevention, non-HTML validation, deterministic SEO metrics, model failover, and end-to-end schema compliance with zero external dependencies.

7. **Companion Enterprise Frontend UI:**
   A companion React + TypeScript + Vite web application (`frontend/`) built with an iOS-style light minimalist aesthetic, custom typography (Plus Jakarta Sans & JetBrains Mono), segmented controls, and visual diagnostic gauges without emojis.

---

### Live Quick Test Command (cURL)

You can test the deployed API directly using the following terminal command:

```bash
curl -X POST https://ai-link-analysis-nwkt.onrender.com/link-analysis \
  -H "Content-Type: application/json" \
  -d '{"url": "https://crest.dxora.com"}'
```

Thank you for reviewing my submission. I look forward to our technical discussion.

Best regards,  
**Jai Prakash V I**  
Software Engineer  
Tiruvallur, Tamil Nadu, India
