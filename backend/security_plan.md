# Security Enhancements for Deployment

## 1. CORS Configuration (Cross-Origin Resource Sharing)
Currently, `CORS_ALLOW_ALL_ORIGINS = True` is insecure. We will restrict this to trusted domains.
-   **Action**: Replace `CORS_ALLOW_ALL_ORIGINS` with `CORS_ALLOWED_ORIGINS`.
-   **Values**: `["http://localhost:5173", "http://127.0.0.1:5173"]` (for local dev) and placeholders for production domains.

## 2. HTTPS & SSL/TLS Configuration
To secure data in transit (including authentication tokens), we must enforce HTTPS.
-   **Action**: Add security headers in `settings.py`.
-   **Condition**: These settings should generally apply when `DEBUG = False` (Production).

### settings to add:
```python
# Security settings for production
if not DEBUG:
    # Enforce HTTPS
    SECURE_SSL_REDIRECT = True
    # Secure Cookies (prevent sending over HTTP)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

## 3. Allowed Hosts
-   **Action**: Update `ALLOWED_HOSTS` to include the deployed domain.

## Verification
-   Run the backend and ensure `http://` requests still work locally (since `DEBUG=True`).
-   Verify CORS allows the frontend to connect.
