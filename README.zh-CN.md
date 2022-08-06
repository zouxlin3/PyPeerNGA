# PyPeerNGA

[![PyPeerNGA](https://img.shields.io/badge/PyPeerNGA-IEM-brightgreen)](https://github.com/zouxlin3/PyPeerNGA)

一个能自动从PEER NGA数据库中下载地震动的Python工具。

## 安装

确保你已经安装了Chrome浏览器。

1. 安装Python依赖

    ```shell
    $ pip install selenium
    $ pip install selenium-wire
    $ pip install requests
    ```

2. 下载浏览器驱动 [Chrome driver](https://chromedriver.chromium.org/downloads) 

   解压后复制到你的项目目录下。

查阅[官方文档](https://pypi.org/project/selenium/)获取详细信息。

## 使用说明

### 登录

![](https://pic.zouxlin3.com/pic/blog/PyPeerNGA/1.png)

```python
web = PeerNGA()
web.signIn('your_email', 'ypur_password')
```

### 选择数据库

![](https://pic.zouxlin3.com/pic/blog/PyPeerNGA/2.png)

可选项: 'NGA West2', 'NGA East'

```python
web.enterDB('NGA West2')
```

### 搜索记录

![](https://pic.zouxlin3.com/pic/blog/PyPeerNGA/3.png)

```python
settings = {
    'RSNs': '',
    'Event Name': '',
    'Station Name': '',
    'Fault Type': '', 
    'Magnitude': '',
    'R_JB': '',
    'R_rup': '',
    'Vs30': '',
    'D5-95': '',
    'Pulse': '',
    'Max No. Records': ''
}
```

Fault Type 可选项:

    1 - All Types(Default)
    2 - Strike Slip (SS)
    3 - Normal/Oblique
    4 - Reverse/Oblique
    5 - SS+Normal
    6 - SS+Reverse
    7 - Normal+Reverse

Pulse 可选项:

    1 - Any Record(Default)
    2 - ONLY Pulse-like Records
    3 - NO Pulse-like Records

```python
web.search(settings=settings)
```

### 下载记录

```python
web.download(saveDir)
```

## 示例

```python
import os
from PeerNGA import PeerNGA


if __name__ == '__main__':
    settings = {
        'RSNs': '1'
    }
    saveDir = os.path.join(os.getcwd(), 'data')

    web = PeerNGA()
    web.signIn('email', 'password')
    web.enterDB('NGA West2')
    web.search(settings=settings)
    web.download(saveDir)
    web.close()
```

## 参考资料

> [python实现下载进度条格式化输出](https://blog.csdn.net/weixin_44001521/article/details/107732555)

> [Selenium Wire](https://github.com/wkeeling/selenium-wire)

> [Selenium 网页测试爬虫库简介](https://www.gairuo.com/p/python-selenium)

> [selenium](https://pypi.org/project/selenium/)

## 使用许可

[MIT](https://github.com/zouxlin3/PyPeerNGA/blob/master/license) © [zouxlin3](https://zouxlin3.com)
