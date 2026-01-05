from dataclasses import dataclass
from typing import Union, Optional

@dataclass
class Proxy:
    host: str
    port: Union[str, int]
    username: Optional[str] = None
    password: Optional[str] = None
    scheme: Optional[str] = "http"

    @property
    def url(self):
        if self.username and self.password:
            return f"{self.scheme}://{self.username}:{self.password}@{self.host}:{self.port}"
        else:
            return f"{self.scheme}://{self.host}:{self.port}"