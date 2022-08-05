# PyPeerNGA

A python tool to download ground motion from PEER NGA database.

## Install

Make sure that you have installed Chrome.

1. Install python package

    ```shell
    $ pip install selenium
    $ pip install selenium-wire
    $ pip install requests
    ```

2. Download [Chrome driver](https://chromedriver.chromium.org/downloads) and make sure it's in the path where the Chrome is installed.

3. Add the path where the Chrome is installed to PATH environment variable.

Go to the document of [selenium](https://pypi.org/project/selenium/) for more details.

## Usage

### Sign in

```python
web = PeerNGA()
web.signIn('your_email', 'ypur_password')
```

```python
import os
from PeerNGA import PeerNGA


if __name__ == '__main__':
    settings = {
        'RSNs': '1'
    }
    saveDir = os.path.join(os.getcwd(), 'data')

    web = PeerNGA()
    web.signIn('zouxlin3@qq.com', 'Sean/2458')
    web.enterDB('NGA West2')
    web.search(settings=settings)
    web.download(saveDir)
    web.close()
```
