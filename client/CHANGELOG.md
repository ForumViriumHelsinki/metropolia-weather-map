# Changelog

## [0.3.1](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-client-v0.3.0...weather-map-client-v0.3.1) (2025-12-09)


### Bug Fixes

* **client:** add defensive array checks to prevent filter errors ([#23](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/23)) ([80692c8](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/80692c86f39f7bb86cc19cb6890fccdc9f53586b))

## [0.3.0](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-client-v0.2.3...weather-map-client-v0.3.0) (2025-12-03)


### Features

* **db:** add dbmate migrations for production database ([#19](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/19)) ([ab477df](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/ab477df71d99ce79144dc29d9355123e983e90ea))


### Bug Fixes

* **client:** add defensive error handling for sensors API ([#18](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/18)) ([05e2653](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/05e26537d061f76784ec18c9c614e5a6d5929f56))

## [0.2.3](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-client-v0.2.2...weather-map-client-v0.2.3) (2025-11-28)


### Bug Fixes

* **client:** use build args for Next.js public env vars ([d512974](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/d5129747f579196ec3bb83d66250902814b9e650))

## [0.2.2](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-client-v0.2.1...weather-map-client-v0.2.2) (2025-11-27)


### Bug Fixes

* **client:** add TypeScript type annotations to Graphs component ([244fa6d](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/244fa6de030c861669c5932ec741f0c9720b6414))
* **client:** force dynamic rendering for pages with API calls ([043c35e](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/043c35e931e0852fc268e0ff2e4af3cc36f81574))
* **client:** remove unused fetchedEndpoints from Graphs section ([167c625](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/167c62593c5a28b55b6d928090e87c651c7da571))
* **client:** remove unused LoadAllImages function and fetchedEndpoints state ([7ca34ce](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/7ca34ce179618ef2745037fd7cbbbef75dfec458))

## [0.2.1](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-client-v0.2.0...weather-map-client-v0.2.1) (2025-11-27)


### Bug Fixes

* **deps:** regenerate pnpm-lock.yaml to match package.json ([#6](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/6)) ([a058358](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/a058358f5c675c059913c0bce15d34dc5f7156ca))

## [0.2.0](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-client-v0.1.0...weather-map-client-v0.2.0) (2025-11-26)


### Features

* add Skaffold orchestration and GitOps deployment infrastructure ([#1](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/1)) ([314bc33](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/314bc3330f0aefdce196e16840908d8e277f52e2))


### Bug Fixes

* **docker:** upgrade Node.js to v22 and fix pnpm version mismatch ([#4](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/4)) ([2f40e3f](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/2f40e3f03bb60f0afc1a62e58182de5e52c2feb2))
