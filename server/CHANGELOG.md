# Changelog

## [0.3.6](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-server-v0.3.5...weather-map-server-v0.3.6) (2025-12-16)


### Bug Fixes

* **server:** handle timezone-aware comparison in filter_install_date ([#50](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/50)) ([fa5cfe7](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/fa5cfe7e49c80dc8daec507e7acc6c4d2ec9581b))

## [0.3.5](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-server-v0.3.4...weather-map-server-v0.3.5) (2025-12-16)


### Performance Improvements

* **server:** further memory optimization for plot generation ([#47](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/47)) ([c617d1a](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/c617d1a5a4ee46107015cc54a19bcf121aa1b446))

## [0.3.4](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-server-v0.3.3...weather-map-server-v0.3.4) (2025-12-16)


### Performance Improvements

* **server:** optimize memory usage for plot generation ([#44](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/44)) ([eff7745](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/eff7745a740cd2b8a58e3bae9b299cdce0686c65))

## [0.3.3](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-server-v0.3.2...weather-map-server-v0.3.3) (2025-12-15)


### Bug Fixes

* **server:** run plot generation in thread pool to prevent event loop blocking ([#40](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/40)) ([1db5682](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/1db5682d589f837cebf292ffa48b26c42fcfe13a))

## [0.3.2](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-server-v0.3.1...weather-map-server-v0.3.2) (2025-12-11)


### Bug Fixes

* **server:** set MPLCONFIGDIR to resolve matplotlib config error ([f645256](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/f6452560e364dbcf3aef875c7c737f0e57308fb8))

## [0.3.1](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-server-v0.3.0...weather-map-server-v0.3.1) (2025-12-02)


### Bug Fixes

* **server:** create weather schema on startup ([#14](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/14)) ([2a992d3](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/2a992d341db2566ccfeaf691ed7bde86a0fe57e6))

## [0.3.0](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-server-v0.2.0...weather-map-server-v0.3.0) (2025-11-28)


### Features

* **server:** make CORS origins configurable via environment variable ([#10](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/10)) ([19a148a](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/19a148afe3c3fc3deda504f19b400e13bfad4f64))

## [0.2.0](https://github.com/ForumViriumHelsinki/metropolia-weather-map/compare/weather-map-server-v0.1.0...weather-map-server-v0.2.0) (2025-11-26)


### Features

* add Skaffold orchestration and GitOps deployment infrastructure ([#1](https://github.com/ForumViriumHelsinki/metropolia-weather-map/issues/1)) ([314bc33](https://github.com/ForumViriumHelsinki/metropolia-weather-map/commit/314bc3330f0aefdce196e16840908d8e277f52e2))
