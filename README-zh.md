# SlothStock

[![PyPI version](https://badge.fury.io/py/slothstock.svg)](https://badge.fury.io/py/slothstock)
[![PyPI license](https://img.shields.io/pypi/l/slothstock.svg)](https://pypi.python.org/pypi/slothstock/)
[![Python Versions](https://img.shields.io/pypi/pyversions/slothstock.svg)](https://pypi.python.org/pypi/slothstock/)
[![Downloads](https://pepy.tech/badge/slothstock)](https://pepy.tech/project/slothstock)

懒人股票

*其他语言版本: [English](README.md), [简体中文](README-zh.md).*

## 入门指南

### 安装

```shell
pip install -U slothstock
```

### 使用

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

## 运行测试

```shell
tox
```

## TODO

- [x] 从雪球获取股票信息。
- [x] MACD 指标。
- [x] 微信消息推送。
- [x] 基本的单元测试，包括正例和基本框架。
- [x] EBK 文件的导入导出。
- [x] 买点信号脚本。
- [ ] 卖点信号脚本。
- [ ] 类似于 Cronjob 的指引。
- [ ] 监控股票管理。
- [ ] 文档。
- [ ] 更完备的单元测试。

## 贡献

- 通过 Github Issues 提交评论或建议。
- 直接提交 Pull Requests 必须没问题。
