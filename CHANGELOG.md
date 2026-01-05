## 1.1.2
### Changed
* Proxy handling, you can now remove proxy using `client.proxy = None`
* `client._session` is now public -> `client.session`

### Added
* Proxy example at [examples/proxy.py](examples/proxy.py)

## 1.1.1
### Added
* Optional `scheme` attribute on the Proxy dataclass, allowing custom proxy URL schemes (#7)

## 1.1.0
### Changed
* Project structure reorganized: features such as **search**, **user**, and **ad** are now separated using mixins.

### Added
* Realistic dynamic mobile User-Agent generation.

## 1.0.10
### Fix
* KeyError when using shippable=True (#5)

## 1.0.9
### Fix
* Fixed SSL verification issue during Leboncoin cookie initialization.

## 1.0.8
### Added
* `max_retries` and `timeout` parameters to `Client`.
* `NotFoundError` exception raised when an ad or user is not found.

## 1.0.7
### Added
* Automatic rotation of browser impersonation when `impersonate` argument in `Client` is set to None.
* Ability to choose which browser to impersonate via the `impersonate` argument in `Client`.
* Option to disable SSL verification for requests by setting `request_verify` to `False` in `Client`.

## 1.0.6
### Fixed
* "Unknown location type" error when searching with a URL containing a zipcode.

## 1.0.5
### Fixed
* 404 error when fetching a pro user who doesn't have a public page

## 1.0.4
### Added
* A lot of new user information can be retrieved (feedback, badges & professional info).
* New [examples](examples/) directory with practical usage cases.
* `get_ad` function to retrieve ad information.
* `get_user` function to retrieve user information (with pro info such as siret).
* Automatic cookies initialization during session setup to prevent HTTP 403 errors.

### Changed
* Codebase refactored: models are now split by functionality (e.g., all user dataclasses are in `user.py`).
* Proxies can now be updated after `Client` creation via `client.proxy = ...`.
* The session can also be changed dynamically via `client.session = ...`.

### Removed
* Removed the `test/` folder (migrated to `examples/`).

## 1.0.3
### Fixed
* Incorrect raw data extraction for location and owner in `Search.build` function

## 1.0.2
### Added
* Support for full Leboncoin URL in `client.search(url=...)`
* New `shippable` argument in the `search` function

### Fixed
* Incorrect enum key assignment in the `build_search_payload_with_args` function

## 1.0.1
### Added
* Realistic `Sec-Fetch-*` headers to prevent 403 errors

## 1.0.0
* Initial release
