# SlothStock

[![PyPI version](https://badge.fury.io/py/slothstock.svg)](https://badge.fury.io/py/slothstock)
[![PyPI license](https://img.shields.io/pypi/l/slothstock.svg)](https://pypi.python.org/pypi/slothstock/)
[![Python Versions](https://img.shields.io/pypi/pyversions/slothstock.svg)](https://pypi.python.org/pypi/slothstock/)
[![Downloads](https://pepy.tech/badge/slothstock)](https://pepy.tech/project/slothstock)

Stock for Sloth.

*Read this in other languages: [English](README.md), [简体中文](README-zh.md).*

## Getting Started

### Installation

```shell
pip install -U slothstock
```

### Usage

```shell
$ sloth-buy -h

usage: sloth-buy [-h] [--token TOKEN] [--filter-st] [--filter-suspend]
                 [--topic-ids TOPIC_IDS] [--uids UIDS] [-e EBK] [-i INTERVAL]
                 [-o OUTPUT] [-p PERIOD] [-s] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN
  --filter-st
  --filter-suspend
  --topic-ids TOPIC_IDS
  --uids UIDS
  -e EBK, --ebk EBK
  -i INTERVAL, --interval INTERVAL
  -o OUTPUT, --output OUTPUT
  -p PERIOD, --period PERIOD
  -s, --strict
  -v, --version         show program's version number and exit
```

## Running the tests

```shell
tox
```

## TODO

- [x] Fetch stock information from XueQiu.
- [x] MACD indicators.
- [x] Wechat push notification.
- [x] Basic unittest with positive cases and structure.
- [x] EBK file import and export.
- [x] Daemon mode.
- [x] Buy signal script.
- [ ] Sell signal script.
- [ ] Add cache for frequent fetched data.
- [ ] logger.
- [ ] Cronjob guide or something similar.
- [ ] Monitored stocks management.
- [ ] Documentation.
- [ ] More robust unittest.

## Contribution

- Comments or suggestions via github issues.
- Pull requests are welcome absolutely.
