from dataclasses import dataclass


@dataclass
class Proxy:
    host: str
    port: str | int
    username: str | None = None
    password: str | None = None
    scheme: str = "http"

    @property
    def url(self):
        if self.username and self.password:
            return f"{self.scheme}://{self.username}:{self.password}@{self.host}:{self.port}"
        else:
            return f"{self.scheme}://{self.host}:{self.port}"
