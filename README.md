# lbc
[![Latest version](https://img.shields.io/pypi/v/lbc?style=for-the-badge)](https://pypi.org/project/lbc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/lbc?style=for-the-badge)
[![GitHub license](https://img.shields.io/github/license/etienne-hd/lbc?style=for-the-badge)](https://github.com/etienne-hd/lbc/blob/master/LICENSE)

**Unofficial client for Leboncoin API**

```python
import lbc

client = lbc.Client()

location = lbc.City( 
    lat=48.85994982004764,
    lng=2.33801967847424,
    radius=10_000, # 10 km
    city="Paris"
)

result = client.search(
    text="maison",
    locations=[location],
    page=1,
    limit=35,
    sort=lbc.Sort.NEWEST,
    ad_type=lbc.AdType.OFFER,
    category=lbc.Category.IMMOBILIER,
    square=[200, 400],
    price=[300_000, 700_000]
)

for ad in result.ads:
    print(ad.url, ad.subject, ad.price)
```
*lbc is not affiliated with, endorsed by, or in any way associated with Leboncoin or its services. Use at your own risk.*

## Installation
Required **Python 3.10+**
```bash
pip install lbc
```

## Usage

Start with the [examples](examples/) to quickly understand how to use the library in real-world scenarios.

### Client
To create client you need to use `lbc.Client` class
```python
import lbc

client = lbc.Client()
```

#### Proxy
You can also configure the client to use a proxy by providing a `Proxy` object:
```python
# Setup proxy1
proxy1 = lbc.Proxy(
	host="127.0.0.1",
	port=12345,
	username="username",
	password="password",
	scheme="http"
)

# Initialize client with proxy1
client = lbc.Client(proxy=proxy1)

# Setup proxy2
proxy2 = lbc.Proxy(
	host="127.0.0.1",
	port=23456,
)

# Change client proxy to proxy2
client.proxy = proxy2

# Remove proxy
client.proxy = None
```


### Search

To perform a search, use the `client.search` method.

This function accepts keyword arguments (`**kwargs`) to customize your query.
For example, if you're looking for houses that include both land and parking, you can specify:

```python
real_estate_type=["3", "4"]
```

These values correspond to what you’d find in a typical Leboncoin URL, like:

```
https://www.leboncoin.fr/recherche?category=9&text=maison&...&real_estate_type=3,4
```

Here's a complete example of a search query:

```python
client.search(
    text="maison",
    locations=[location],
    page=1,
    limit=35,
    limit_alu=0,
    sort=lbc.Sort.NEWEST,
    ad_type=lbc.AdType.OFFER,
    category=lbc.Category.IMMOBILIER,
    owner_type=lbc.OwnerType.ALL,
    search_in_title_only=True,
    square=[200, 400],
    price=[300_000, 700_000],
)
```

#### Alternatively

You can also perform search using a full Leboncoin URL:

```python
client.search(
    url="https://www.leboncoin.fr/recherche?category=9&text=maison&locations=Paris__48.86023250788424_2.339006433295173_9256&square=100-200price=500000-1000000&rooms=1-6&bedrooms=3-6&outside_access=garden,terrace&orientation=south_west&owner_type=private",
    page=1,
    limit=35
)
```

If `url` is provided, it overrides other keyword parameters such as `text`, `category`, `locations`, etc. However, pagination parameters like `page`, `limit`, and `limit_alu` are still applied.

### Location

The `locations` parameter accepts a list of one or more location objects. You can use one of the following:

* `lbc.Region(...)`
* `lbc.Department(...)`
* `lbc.City(...)`

Each one corresponds to a different level of geographic granularity.

#### City example

```python
location = lbc.City(
    lat=48.85994982004764,
    lng=2.33801967847424,
    radius=10_000,  # in meters
    city="Paris"
)
```

#### Region / Department example

```python
from lbc import Region, Department

region = Region.ILE_DE_FRANCE
department = Department.PARIS
```

### 403 Error

If you encounter a **403 Forbidden** error, it usually means your requests are being blocked by [Datadome](https://datadome.co).
To resolve this:

* Try reducing the request frequency (add delays between requests).
* If you're using a proxy, make sure it is **clean** and preferably located in **France**.

Using residential or mobile proxies can also help avoid detection.

## License

This project is licensed under the MIT License.

## Support

<a href="https://www.buymeacoffee.com/etienneh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

You can contact me via [Telegram](https://t.me/etienne_hd) or [Discord](https://discord.com/users/1153975318990827552) if you need help with scraping services or want to write a library.