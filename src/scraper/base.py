"""Base HTTP session with SSL handling, retry, and rate limiting."""

import time
import urllib3
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.config import (
    USER_AGENT, SSL_VERIFY, REQUEST_DELAY, REQUEST_TIMEOUT,
    MAX_RETRIES, RETRY_BACKOFF,
)

# Suppress InsecureRequestWarning when SSL_VERIFY is False
if not SSL_VERIFY:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ScraperSession:
    """Polite HTTP session with automatic retry and rate limiting."""

    def __init__(self, delay: float = REQUEST_DELAY):
        self.delay = delay
        self._last_request_time = 0.0
        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en;q=0.5",
        })
        session.verify = SSL_VERIFY

        retry = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_BACKOFF,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def _rate_limit(self):
        elapsed = time.time() - self._last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self._last_request_time = time.time()

    def get(self, url: str, **kwargs) -> requests.Response:
        """GET with rate limiting. Raises on HTTP errors."""
        self._rate_limit()
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)
        response = self.session.get(url, **kwargs)
        response.raise_for_status()
        return response

    def get_safe(self, url: str, **kwargs) -> requests.Response | None:
        """GET that returns None instead of raising on error."""
        try:
            return self.get(url, **kwargs)
        except requests.RequestException:
            return None

    def test_connection(self, url: str) -> dict:
        """Test if a URL is reachable. Returns diagnostic info."""
        result = {
            "url": url,
            "reachable": False,
            "status_code": None,
            "content_type": None,
            "content_length": None,
            "error": None,
        }
        try:
            resp = self.get(url)
            result["reachable"] = True
            result["status_code"] = resp.status_code
            result["content_type"] = resp.headers.get("Content-Type")
            result["content_length"] = len(resp.content)
        except requests.RequestException as e:
            result["error"] = str(e)
            if hasattr(e, "response") and e.response is not None:
                result["status_code"] = e.response.status_code
        return result
