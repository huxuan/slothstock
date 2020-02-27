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

usage: sloth-buy [-h] [--reserve-st] [--reserve-suspend]
                 [--check-great-great-grandparent] [--daemon]
                 [--interval INTERVAL] [--ignore-empty] [--output OUTPUT] [-V]
                 [--ebk EBK] [--period PERIOD] [--loose] [--skip-child]
                 [--title TITLE] [--token TOKEN] [--topic-ids TOPIC_IDS]
                 [--uids UIDS]

optional arguments:
  -h, --help            show this help message and exit
  --daemon
  --interval INTERVAL
  --ignore-empty
  --output OUTPUT
  -V, --version         show program's version number and exit

Buy:
  --reserve-st
  --reserve-suspend
  --check-great-great-grandparent

SlothStock:
  --ebk EBK
  --period PERIOD
  --loose
  --skip-child

WxPusher:
  --title TITLE
  --token TOKEN
  --topic-ids TOPIC_IDS
  --uids UIDS
```

```shell
$ sloth-sell -h

usage: sloth-sell [-h] [--daemon] [--interval INTERVAL] [--ignore-empty]
                  [--output OUTPUT] [-V] [--ebk EBK] [--period PERIOD]
                  [--loose] [--skip-child] [--title TITLE] [--token TOKEN]
                  [--topic-ids TOPIC_IDS] [--uids UIDS]

optional arguments:
  -h, --help            show this help message and exit
  --daemon
  --interval INTERVAL
  --ignore-empty
  --output OUTPUT
  -V, --version         show program's version number and exit

SlothStock:
  --ebk EBK
  --period PERIOD
  --loose
  --skip-child

WxPusher:
  --title TITLE
  --token TOKEN
  --topic-ids TOPIC_IDS
  --uids UIDS
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
- [x] Sell signal script.
- [ ] Add cache for frequent fetched data.
- [ ] logger.
- [ ] Cronjob guide or something similar.
- [ ] Monitored stocks management.
- [ ] Documentation.
- [ ] More robust unittest.

## Contribution

- Comments or suggestions via github issues.
- Pull requests are welcome absolutely.
