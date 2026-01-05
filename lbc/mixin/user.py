from ..model import User
from ..exceptions import NotFoundError

class UserMixin:
    def get_user(self, user_id: str) -> User:
        """
        Retrieve information about a user based on their user ID.

        This method fetches detailed user data such as their profile, professional status,
        and other relevant metadata available through the public user API.

        Args:
            user_id (str): The unique identifier of the user on Leboncoin. Usually found in the url (e.g 57f99bb6-0446-4b82-b05d-a44ea7bcd2cc).

        Returns:
            User: A `User` object containing the parsed user information.
        """
        user_data = self._fetch(method="GET", url=f"https://api.leboncoin.fr/api/user-card/v2/{user_id}/infos", timeout=self.timeout, max_retries=self.max_retries)

        pro_data = None
        if user_data.get("account_type") == "pro":
            try:
                pro_data = self._fetch(method="GET", url=f"https://api.leboncoin.fr/api/onlinestores/v2/users/{user_id}?fields=all", timeout=self.timeout, max_retries=self.max_retries)
            except NotFoundError:
                pass # Some professional users may not have a Leboncoin page.
        return User._build(user_data=user_data, pro_data=pro_data)