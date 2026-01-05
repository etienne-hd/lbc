from typing import Optional, Union, List

from ..model import Category, Sort, Region, Department, City, AdType, OwnerType, Search
from ..utils import build_search_payload_with_args, build_search_payload_with_url

class SearchMixin:
    def search(
        self,
        url: Optional[str] = None,
        text: Optional[str] = None,
        category: Category = Category.TOUTES_CATEGORIES,
        sort: Sort = Sort.RELEVANCE,
        locations: Optional[Union[List[Union[Region, Department, City]], Union[Region, Department, City]]] = None, 
        limit: int = 35, 
        limit_alu: int = 3, 
        page: int = 1, 
        ad_type: AdType = AdType.OFFER,
        owner_type: Optional[OwnerType] = None,
        shippable: Optional[bool] = None,
        search_in_title_only: bool = False,
        **kwargs
    ) -> Search:
        """
        Perform a classified ads search on Leboncoin with the specified criteria.

        You can either:
        - Provide a full `url` from a Leboncoin search to replicate the search directly.
        - Or use the individual parameters (`text`, `category`, `locations`, etc.) to construct a custom search.

        Args:
            url (Optional[str], optional): A full Leboncoin search URL. If provided, all other parameters will be ignored and the search will replicate the results from the URL.            
            text (Optional[str], optional): Search keywords. If None, returns all matching ads without filtering by keyword. Defaults to None.
            category (Category, optional): Category to search in. Defaults to Category.TOUTES_CATEGORIES.
            sort (Sort, optional): Sorting method for results (e.g., relevance, date, price). Defaults to Sort.RELEVANCE.
            locations (Optional[Union[List[Union[Region, Department, City]], Union[Region, Department, City]]], optional): One or multiple locations (region, department, or city) to filter results. Defaults to None.
            limit (int, optional): Maximum number of results to return. Defaults to 35.
            limit_alu (int, optional): Number of ALU (Annonces Lu / similar ads) suggestions to include. Defaults to 3.
            page (int, optional): Page number to retrieve for paginated results. Defaults to 1.
            ad_type (AdType, optional): Type of ad (offer or request). Defaults to AdType.OFFER.
            owner_type (Optional[OwnerType], optional): Filter by seller type (individual, professional, or all). Defaults to None.
            shippable (Optional[bool], optional): If True, only includes ads that offer shipping. Defaults to None.
            search_in_title_only (bool, optional): If True, search will only be performed on ad titles. Defaults to False.
            **kwargs: Additional advanced filters such as price range (`price=(min, max)`), surface area (`square=(min, max)`), property type, and more.

        Returns:
            Search: A `Search` object containing the parsed search results.
        """
        if url:
            payload = build_search_payload_with_url(
                url=url, limit=limit, page=page
            )
        else:
            payload = build_search_payload_with_args(
                text=text, category=category, sort=sort, locations=locations, 
                limit=limit, limit_alu=limit_alu, page=page, ad_type=ad_type,
                owner_type=owner_type, shippable=shippable, search_in_title_only=search_in_title_only, **kwargs
            )

        body = self._fetch(method="POST", url="https://api.leboncoin.fr/finder/search", payload=payload, timeout=self.timeout, max_retries=self.max_retries)
        return Search._build(raw=body, client=self)