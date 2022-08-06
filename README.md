# PyPeerNGA

[![PyPeerNGA](https://img.shields.io/badge/PyPeerNGA-IEM-brightgreen)](https://github.com/zouxlin3/PyPeerNGA)

A Python tool to download ground motion from PEER NGA database.

## Install

Make sure that you have installed Chrome.

1. Install Python package

    ```shell
    $ pip install selenium
    $ pip install selenium-wire
    $ pip install requests
    ```

2. Download [Chrome driver](https://chromedriver.chromium.org/downloads) 

   Copy to your project directory.

Go to the document of [selenium](https://pypi.org/project/selenium/) for more details.

## Usage

### Sign in

![](https://pic.zouxlin3.com/pic/blog/PyPeerNGA/1.png)

```python
web = PeerNGA()
web.signIn('your_email', 'ypur_password')
```

### Enter a database

![](https://pic.zouxlin3.com/pic/blog/PyPeerNGA/2.png)

Options: 'NGA West2', 'NGA East'

```python
web.enterDB('NGA West2')
```

### Search records

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

Fault Type options:

    1 - All Types(Default)
    2 - Strike Slip (SS)
    3 - Normal/Oblique
    4 - Reverse/Oblique
    5 - SS+Normal
    6 - SS+Reverse
    7 - Normal+Reverse

Pulse options:

    1 - Any Record(Default)
    2 - ONLY Pulse-like Records
    3 - NO Pulse-like Records

```python
web.search(settings=settings)
```

### Download records

```python
web.download(saveDir)
```

## Example

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

## References

> [python实现下载进度条格式化输出](https://blog.csdn.net/weixin_44001521/article/details/107732555)

> [Selenium Wire](https://github.com/wkeeling/selenium-wire)

> [Selenium 网页测试爬虫库简介](https://www.gairuo.com/p/python-selenium)

> [selenium](https://pypi.org/project/selenium/)

## License

[MIT](https://github.com/zouxlin3/PyPeerNGA/blob/master/license) © [zouxlin3](https://zouxlin3.com)
