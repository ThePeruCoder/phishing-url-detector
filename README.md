# 🎣 Phishing URL Detector

A machine learning web application built with Streamlit that analyzes URLs and detects whether they are legitimate or potential phishing threats.

**Live Demo:** [Phishing URL Detector App](https://phishing-url-detector-suhas.streamlit.app/)

---

## Model

- **Algorithm:** Random Forest Classifier (`n_estimators=500`, `max_depth=20`, `class_weight='balanced'`)
- **Features used (12):** `url_length`, `num_dots`, `has_at`, `has_double_slash`, `has_https`, `has_ip`, `num_subdomains`, `is_shortened`, `suspicious_words`, `domain_length`, `num_special_chars`, `url_entropy`

---

## ⚠️ Known Issues / Limitations

### 1. HTTPS ≠ Safe
The model treats `has_https` as a safety signal, but modern phishing sites routinely use HTTPS. This can cause the model to classify a phishing URL as legitimate simply because it uses SSL.

### 2. No Domain Reputation Check
The model only analyses the URL string — it makes no DNS lookup or WHOIS query. A freshly registered lookalike domain (e.g. `paypa1-secure.com`) can easily bypass detection if its string features look normal.

### 3. Keyword List is Easily Evaded
`suspicious_words` relies on a fixed hardcoded list (`login`, `bank`, `paypal`, …). Attackers can avoid all listed words and still craft a phishing URL that scores 0 on this feature.

### 4. Shortened URL List is Incomplete
`is_shortened` only checks a small, hardcoded list of shorteners. Any unlisted service (e.g. `rb.gy`, `cutt.ly`) will not be flagged, even though shortened URLs are a common phishing vector.

### 5. `has_double_slash` Bug
The detection logic always checks `url_str[7:]` regardless of whether the scheme is `http://` (7 chars) or `https://` (8 chars). This means `https://` URLs are sliced incorrectly, producing unreliable results for that feature.

### 6. Entropy Bug (`url_entropy`)
Inside `url_entropy`, the probability is computed as `count / len(url)` instead of `count / len(url_str)`. When `url` is the raw input object and `url_str` is the string copy, this can cause a type error or silently produce a wrong entropy value.

### 7. No Context Awareness
The model cannot understand page content, redirects, or visual similarity (e.g. homograph attacks using Unicode characters). A URL like `xn--pypal-4ve.com` (IDN homograph of `paypal.com`) produces perfectly normal string-level features.

### 8. Static Model — No Retraining
The `.pkl` model is never updated. As phishing tactics evolve, model accuracy degrades over time without periodic retraining on fresh data.
