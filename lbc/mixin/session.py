from curl_cffi import requests, BrowserTypeLiteral
from typing import Optional
import random
import uuid

from ..model import Proxy

class SessionMixin:
    def __init__(self, proxy: Optional[Proxy] = None, impersonate: BrowserTypeLiteral = None, request_verify: bool = True, **kwargs):
        self._session = self._init_session(proxy=proxy, impersonate=impersonate, request_verify=request_verify)
        self._proxy = proxy
        self._impersonate = impersonate
        super().__init__(**kwargs)

    def _generate_user_agent(self) -> str:
        # LBC;iOS;26.2;iPhone;phone;01234567-89AB-CDEF-0123-456789ABCDEF;wifi;101.44.0
        # LBC;Android;11;Android SDK built for arm64;phone;0123456789ABCDEF;wifi;100.85.2
        # LBC;<OS>;<OS_VERSION>;<MODEL>;phone;<DEVICE_ID>;wifi;<APP_VERSION>
        os = random.choice(["iOS", "Android"])
        if os == "iOS":
            os_version = random.choice(["18.0", "18.1", "18.2", "18.3", "18.4", "18.5", "18.6", "18.7", "18.7.3",
                    "26.0", "26.1", "26.2"])
            model = "iPhone"
            device_id = str(uuid.uuid4())
            app_version = random.choice(["101.45.0", "101.44.0", "101.43.1", "101.43.0", "101.42.1", "101.42.0", "101.41.0", "101.40.0", "101.39.0", "101.38.0"])
        else:
            os_version = random.choice(["11", "12", "13", "14", "15"])
            model = random.choice(["SM-G991B", "SM-G996B", "SM-G998B", "SM-S911B", "SM-S916B", "SM-S918B", "SM-A505F", "SM-A546B", "SM-A137F", "SM-M336B",
                    "Pixel 5", "Pixel 6", "Pixel 6a", "Pixel 7", "Pixel 7 Pro", "Pixel 8", "Pixel 8 Pro",
                    "Mi 10", "Mi 11", "Mi 11 Lite", "Redmi Note 10", "Redmi Note 11", "Redmi Note 12", "POCO F3", "POCO F4", "POCO X3 Pro",
                    "ONEPLUS A6003", "ONEPLUS A6013", "ONEPLUS A5000", "ONEPLUS A5010", "OnePlus 8", "OnePlus 9", "OnePlus 10 Pro", "OnePlus Nord"])
            device_id = uuid.uuid4().hex[:16]
            app_version = random.choice(["100.85.2", "100.84.1", "100.83.1", "100.82.0", "100.81.1"])
        return f"LBC;{os};{os_version};{model};phone;{device_id};wifi;{app_version}"

    def _init_session(self, proxy: Optional[Proxy] = None, impersonate: BrowserTypeLiteral = None, request_verify: bool = True) -> requests.Session:
        """
        Initializes an HTTP session with optional proxy configuration and browser impersonation.

        If no `impersonate` value is provided, a random browser type will be selected among common options.

        Args:
            proxy (Optional[Proxy], optional): Proxy configuration to use for the session. If provided, it will be applied to both HTTP and HTTPS traffic. Defaults to None.
            impersonate (BrowserTypeLiteral, optional): Browser type to impersonate for requests (e.g., "firefox", "chrome", "edge", "safari", "safari_ios", "chrome_android"). If None, a random browser type will be chosen.            
            request_verify (bool, optional): Whether to verify SSL certificates for HTTPS requests. Defaults to True.

        Returns:
            requests.Session: A configured session instance ready to send requests.
        """
        if impersonate == None: # Pick a random browser client
            impersonate: BrowserTypeLiteral = random.choice(
                [
                    "safari",
                    "safari_ios",
                    "chrome_android",
                    "firefox"
                ]
            )

        session = requests.Session(
            impersonate=impersonate,
        )

        session.headers.update(
            {
                'User-Agent': self._generate_user_agent(),
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
            }
        )
        if proxy:
            session.proxies = {
                "http": proxy.url,
                "https": proxy.url
            }

        session.get("https://www.leboncoin.fr/", verify=request_verify) # Init cookies
        return session

    @property
    def session(self) -> requests.Session:
        return self._session
    
    @session.setter
    def session(self, value: requests.Session):
        if isinstance(value, requests.Session):
            self._session = value
        else:
            raise TypeError("Session must be an instance of the curl_cffi.requests.Session")
    
    @property
    def proxy(self) -> Proxy:
        return self._proxy
    
    @proxy.setter
    def proxy(self, value: Proxy):
        if isinstance(value, Proxy):
            self._session.proxies = {
                "http": value.url,
                "https": value.url
            }
        else:
            raise TypeError("Proxy must be an instance of the Proxy class")
