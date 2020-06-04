# arXiv-newsletter
A simple configurable bot for sending arXiv article alert by mail.

## Prerequisites

```
PyYAML>=5.3.1
arxiv>=0.5.3
```

## Configuration

All configurations can be found in `config.yml`.

* Domains: specify search domains that articles belong to.
* Keywords: specify article queries and support boolean expression. Note that one query sends out one mail.
* Query config: specify query parameters, such as `sort_by`, `sort_order`. See [here](https://github.com/lukasschwab/arxiv.py) for detailed documentation.
* Mail: specify sender’s mail configuration.

After setting up basic configurations, you may configure `crontab` schedule using `crontab -e`. A sample configuration can be:

```
0 2 * * * /path-to-script/run.py >> /path-to-script/run.log
```

which runs at 2 am everyday.

## Example Mail

```
***********************************
arXiv newsletter 2020-06-04 1/3
***********************************

Query: (all:graph) AND (all:unsupervised OR all:self-supervised OR all:representation learning OR all:convolutional networks)

1. Self-supervised Training of Graph Convolutional Networks
Qikui Zhu, Bo Du, Pingkun Yan
Published at: 2020-06-03T16:53:37Z
Updated at: 2020-06-03T16:53:37Z
Categories: cs.CV

http://arxiv.org/abs/2006.02380v1

Abstract:
Omitted
```

