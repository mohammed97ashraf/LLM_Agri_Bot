# Security Policy

## Supported Versions

We actively maintain and support the latest stable release of LLM Agri Bot. Older versions may receive security updates on a case-by-case basis.

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of LLM Agri Bot and its users seriously. If you discover a security vulnerability, we appreciate your responsible disclosure.

To report a vulnerability, please email us directly at **security@[example-domain].com** (replace with the repository maintainer’s actual security contact). Alternatively, you can open a [draft security advisory](https://github.com/mohammed97ashraf/LLM_Agri_Bot/security/advisories/new) on GitHub.

Please include the following details in your report:

- A clear description of the vulnerability.
- Steps to reproduce the issue (proof of concept is helpful).
- The impact you believe the vulnerability could have.
- Any relevant configuration or environment details (OS, Python version, dependencies).

We will acknowledge receipt within **48 hours** and will work with you to understand, validate, and address the issue promptly. We aim to release a fix within **90 days** for critical issues, depending on complexity.

### What to Expect

- **Confirmation**: We will confirm receipt of your report.
- **Validation**: We will assess the vulnerability and determine its severity.
- **Resolution**: We will develop a fix and test it thoroughly.
- **Disclosure**: Once a fix is released, we may publish a security advisory with appropriate credit to the reporter (unless you prefer anonymity).

## Responsible Disclosure

We ask that you do not publicly disclose the vulnerability until we have had a chance to address it. This protects all users of the software.

## Scope

This security policy applies to the LLM Agri Bot codebase, including:

- All Python backend code (Flask routes, API integrations).
- Frontend assets (HTML, CSS, JavaScript).
- Configuration and environment variable handling (API keys, tokens).

**Out of scope:**

- Third-party dependencies (please report to their respective maintainers).
- The OpenAI API or HuggingFace services themselves (contact those providers directly).

## Security Best Practices for Users

To keep your instance of LLM Agri Bot secure:

- **Protect your API keys**: Never commit your OpenAI API key or HuggingFace token to version control. Use environment variables or a `.env` file (excluded from Git via `.gitignore`).
- **Keep dependencies updated**: Regularly run `pip list --outdated` and update packages, especially Flask and its extensions.
- **Sanitize user input**: Although the chatbot is designed for agriculture queries, avoid echoing arbitrary user input back without validation to prevent XSS or injection attacks.
- **Use HTTPS in production**: When deploying, always serve the web interface over HTTPS.
- **Limit network exposure**: If running locally, bind Flask to `127.0.0.1` rather than `0.0.0.0` to avoid external access.

## Vulnerability Disclosure Timeline

| Stage               | Timeframe        |
|---------------------|------------------|
| Receipt             | Within 48 hours  |
| Triage & validation | Within 7 days    |
| Fix development     | Varies (target 90 days for critical) |
| Public disclosure   | After fix release |

## Contact

For any security-related questions, reach out to **security@[example-domain.com]** or open a [GitHub Issue](https://github.com/mohammed97ashraf/LLM_Agri_Bot/issues/new) with the label "security".

---

Thank you for helping keep LLM Agri Bot safe for everyone.