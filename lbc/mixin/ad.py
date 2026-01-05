from typing import Union

from ..model import Ad

class AdMixin:
    def get_ad(self, ad_id: Union[str, int]) -> Ad:
        """
        Retrieve detailed information about a classified ad using its ID.

        This method fetches the full content of an ad, including its description,
        pricing, location, and other relevant metadata made
        available through the public Leboncoin ad API.

        Args:
            ad_id (Union[str, int]): The unique identifier of the ad on Leboncoin. Can be found in the ad URL.

        Returns:
            Ad: An `Ad` object containing the parsed ad information.
        """
        body = self._fetch(method="GET", url=f"https://api.leboncoin.fr/api/adfinder/v1/classified/{ad_id}", timeout=self.timeout, max_retries=self.max_retries)
        return Ad._build(raw=body, client=self)