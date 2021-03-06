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
                 [--ebk EBK] [--period PERIOD] [--loose]
                 [--child {cross,divergence}] [--datetime DATETIME]
                 [--title TITLE] [--token TOKEN] [--topic-ids TOPIC_IDS]
                 [--uids UIDS]

optional arguments:
  -h, --help            show this help message and exit
  --daemon              Flag of daemon mode, no console output. (default:
                        False)
  --interval INTERVAL   Time interval in seconds between successive requests
                        in providers. (default: 0.1)
  --ignore-empty        Flag for no output or notification when the result is
                        empty. (default: False)
  --output OUTPUT       The output file in ebk format for the results.
                        (default: None)
  -V, --version         show program's version number and exit

Buy:
  --reserve-st          Flag to reserve ST stocks. (default: False)
  --reserve-suspend     Flag to reserve suspended stocks. (default: False)
  --check-great-great-grandparent
                        Flag to check great_great_grandparent period.
                        (default: False)

SlothStock:
  --ebk EBK             Stock candidates in ebk format file. If not specified,
                        all stocks are processed. Note that multiple of them
                        are supported. (default: [])
  --period PERIOD       Check signal for specific period. Valid choices are
                        `1m`, `5m`, `15m`, `60m`, `day`, `week`, `month`,
                        `quarter`, `year`. (default: day)
  --loose               Flag of loose mode for signal check. (default: False)
  --child {cross,divergence}
                        Child check mode, it should be `cross` or
                        `divergence`. If no specified, child period check will
                        be skipped. (default: None)
  --datetime DATETIME   The datetime compatible with ISO 8601 format (`YY-MM-
                        DD` or `YYYY-MM-DDTHH:MM`) for signal check, mostly
                        for testing purpose. (default: None)

WxPusher:
  --title TITLE         The `title` for the notification. (default: None)
  --token TOKEN         The `token` for the notification. None means no
                        notification (default: None)
  --topic-ids TOPIC_IDS
                        The `topic_ids` for the notification. Note that
                        multiple of them are supported and no notification
                        will be sent if both `topic_ids` and `uids` are None,
                        (default: [])
  --uids UIDS           The `uids` for the notification. Note that multiple of
                        them are supported and no notification will be sent if
                        both `topic_ids` and `uids` are None. (default: [])
```

```shell
$ sloth-sell -h

usage: sloth-sell [-h] [--daemon] [--interval INTERVAL] [--ignore-empty]
                  [--output OUTPUT] [-V] [--check-parent] [--ebk EBK]
                  [--period PERIOD] [--loose] [--child {cross,divergence}]
                  [--datetime DATETIME] [--title TITLE] [--token TOKEN]
                  [--topic-ids TOPIC_IDS] [--uids UIDS]

optional arguments:
  -h, --help            show this help message and exit
  --daemon              Flag of daemon mode, no console output. (default:
                        False)
  --interval INTERVAL   Time interval in seconds between successive requests
                        in providers. (default: 0.1)
  --ignore-empty        Flag for no output or notification when the result is
                        empty. (default: False)
  --output OUTPUT       The output file in ebk format for the results.
                        (default: None)
  -V, --version         show program's version number and exit

Sell:
  --check-parent        Flag to check parent period. (default: False)

SlothStock:
  --ebk EBK             Stock candidates in ebk format file. If not specified,
                        all stocks are processed. Note that multiple of them
                        are supported. (default: [])
  --period PERIOD       Check signal for specific period. Valid choices are
                        `1m`, `5m`, `15m`, `60m`, `day`, `week`, `month`,
                        `quarter`, `year`. (default: day)
  --loose               Flag of loose mode for signal check. (default: False)
  --child {cross,divergence}
                        Child check mode, it should be `cross` or
                        `divergence`. If no specified, child period check will
                        be skipped. (default: None)
  --datetime DATETIME   The datetime compatible with ISO 8601 format (`YY-MM-
                        DD` or `YYYY-MM-DDTHH:MM`) for signal check, mostly
                        for testing purpose. (default: None)

WxPusher:
  --title TITLE         The `title` for the notification. (default: None)
  --token TOKEN         The `token` for the notification. None means no
                        notification (default: None)
  --topic-ids TOPIC_IDS
                        The `topic_ids` for the notification. Note that
                        multiple of them are supported and no notification
                        will be sent if both `topic_ids` and `uids` are None,
                        (default: [])
  --uids UIDS           The `uids` for the notification. Note that multiple of
                        them are supported and no notification will be sent if
                        both `topic_ids` and `uids` are None. (default: [])
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
