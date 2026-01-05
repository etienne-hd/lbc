from typing import Optional, Union
from curl_cffi import BrowserTypeLiteral

from .mixin import (
    SessionMixin,
    SearchMixin,
    UserMixin,
    AdMixin
)
from .model import Proxy
from .exceptions import DatadomeError, RequestError, NotFoundError

class Client(
    SessionMixin,
    SearchMixin,
    UserMixin,
    AdMixin
):
    def __init__(self, proxy: Optional[Proxy] = None, impersonate: BrowserTypeLiteral = None, 
			request_verify: bool = True, timeout: float = 30.0, max_retries: int = 5):
        """
        Initializes a Leboncoin Client instance with optional proxy, browser impersonation, and SSL verification settings.

        If no `impersonate` value is provided, a random browser type will be selected among common options.
        
        Args:
            proxy (Optional[Proxy], optional): Proxy configuration to use for the client. If provided, it will be applied to all requests. Defaults to None.
            impersonate (BrowserTypeLiteral, optional): Browser type to impersonate for requests (e.g., "firefox", "chrome", "edge", "safari", "safari_ios", "chrome_android"). If None, a random browser type will be chosen.
            request_verify (bool, optional): Whether to verify SSL certificates when sending requests. Set to False to disable SSL verification (not recommended for production). Defaults to True.
            timeout (int, optional): Maximum time in seconds to wait for a request before timing out. Defaults to 30.
            max_retries (int, optional): Maximum number of times to retry a request in case of failure (403 error). Defaults to 5.
        """
        super().__init__(proxy=proxy, impersonate=impersonate, request_verify=request_verify)
        
        self.request_verify = request_verify
        self.timeout = timeout
        self.max_retries = max_retries

    def _fetch(self, method: str, url: str, payload: Optional[dict] = None, timeout: int = 30, max_retries: int = 5) -> Union[dict, None]:
        """
        Internal method to send an HTTP request using the configured session.

        Args:
            method (str): HTTP method to use (e.g., "GET", "POST").
            url (str): Full URL of the API endpoint.
            payload (Optional[dict], optional): JSON payload to send with the request. Used for POST/PUT methods. Defaults to None.
            timeout (int, optional): Timeout for the request, in seconds. Defaults to 30.
            max_retries (int, optional): Number of times to retry the request in case of failure. Defaults to 5.

        Raises:
            DatadomeError: Raised when the request is blocked by Datadome protection (HTTP 403).
            RequestError: Raised for any other non-successful HTTP response.

        Returns:
            dict: Parsed JSON response from the server.
        """
        response = self.session.request(
            method=method,
            url=url, 
            json=payload,
            timeout=timeout,
            verify=self.request_verify,
        )
        if response.ok:
            return response.json()
        elif response.status_code == 403:
            if max_retries > 0:
                self.session = self._init_session(proxy=self._proxy, impersonate=self._impersonate, request_verify=self.request_verify) # Re-init session
                return self._fetch(method=method, url=url, payload=payload, timeout=timeout, max_retries=max_retries - 1)
            if self.proxy:
                raise DatadomeError(f"Access blocked by Datadome: your proxy appears to have a poor reputation, try to change it.")
            else:
                raise DatadomeError(f"Access blocked by Datadome: your activity was flagged as suspicious. Please avoid sending excessive requests.")
        elif response.status_code == 404 or response.status_code == 410:
            raise NotFoundError(f"Unable to find ad or user.")
        else:
            raise RequestError(f"Request failed with status code {response.status_code}.")