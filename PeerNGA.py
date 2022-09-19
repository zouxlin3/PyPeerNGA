import os
from seleniumwire import webdriver
from seleniumwire.request import Request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from IO import unZip, downloader
from typing import NoReturn


def _checkStates(level: int):
    def decorator(func):
        def check(self, *args, **kwargs):
            stateNames = list(self.states.keys())
            for i in range(level):
                stateName = stateNames[i]
                if not self.states[stateName]:
                    print('Please {0} before {1}.'.format(stateName, func.__name__))
                    return check
            func(self, *args, **kwargs)

        return check

    return decorator


class PeerNGA:
    def __init__(self, driverPath: str) -> NoReturn:
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')

        self.browser = webdriver.Chrome(driverPath, chrome_options=options)
        self.browser.request_interceptor = self.__interceptor

        self.states = {
            "sign in": False,
            'enter database': False,
            'search records': False
        }

    def signIn(self, email: str, password: str) -> NoReturn:
        self.browser.get('https://ngawest2.berkeley.edu/users/sign_in?unauthenticated=true')

        inputEmail = self.browser.find_element(By.NAME, 'user[email]')
        inputPassword = self.browser.find_element(By.NAME, 'user[password]')
        inputEmail.send_keys(email)
        inputPassword.send_keys(password)
        btnSignIn = self.browser.find_element(By.NAME, 'commit')
        btnSignIn.click()
        parAlert = self.browser.find_element(By.CLASS_NAME, 'alert')
        alert = parAlert.text

        if alert != '':
            print(alert)
        else:
            print('Signed in successfully.')
            self.states['sign in'] = True

    def close(self) -> NoReturn:
        self.browser.quit()

    @_checkStates(1)
    def enterDB(self, label: str):
        DBdict = {
            'NGA West2': 1,
            'NGA east': 2
        }
        self.browser.get('https://ngawest2.berkeley.edu/spectras/new?sourceDb_flag={0}'.format(DBdict[label]))
        self.browser.execute_script('OnSubmit()')
        WebDriverWait(self.browser, 10).until(lambda x: x.find_element(By.NAME, "search[search_nga_number]"))
        self.states['enter database'] = True

    @_checkStates(2)
    def search(self, settings: dict = None):
        if settings:
            for label in settings:
                elemName = self.__getElemName(label)
                if elemName:
                    inputElem = self.browser.find_element(By.NAME, elemName)
                    inputElem.send_keys(settings[label])

        if self.__clickBtnSearch():
            self.states['search records'] = True
            return True
        return False

    @_checkStates(3)
    def download(self, saveDir: str):
        self.browser.execute_script('getSelectedResult(true)')
        alert = self.browser.switch_to.alert
        alert.accept()
        alert = self.browser.switch_to.alert
        alert.accept()

        reqDownload = WebDriverWait(self.browser, 10).until(lambda x: self.__interceptor(x.requests[-1]))
        url = reqDownload.url
        headers = reqDownload.headers
        params = reqDownload.params
        saveName = 'download.zip'
        savePath = downloader(url, saveName, saveDir, headers, params)

        unZip(savePath, saveDir)
        for f in os.listdir(saveDir):
            if f.endswith('.zip') or f.endswith('.csv'):
                os.remove(os.path.join(saveDir, f))

    def __clickBtnSearch(self) -> bool:
        self.browser.execute_script('OnSubmit()')

        divNotice = WebDriverWait(self.browser, 10).until(lambda x: x.find_element(By.ID, 'notice'))
        notice = divNotice.text
        print(notice)
        if ' NO ' in notice or ' exceed ' in notice:
            return False
        return True

    @staticmethod
    def __getElemName(label: str) -> str or bool:
        nameDict = {
            'RSNs': 'search[search_nga_number]',
            'Event Name': 'search[search_eq_name]',
            'Station Name': 'search[search_station_name]',
            'Fault Type': 'search[faultType]',
            'Magnitude': 'search[magnitude]',
            'R_JB': 'search[rjb]',
            'R_rup': 'search[rrup]',
            'Vs30': 'search[vs30]',
            'D5-95': 'search[duration]',
            'Pulse': 'search[pulse]',
            'Max No. Records': 'search[output_num]'
        }

        if label in nameDict:
            return nameDict[label]
        print('There is no such setting item: {0}'.format(label))
        return False

    @staticmethod
    def __interceptor(request: Request) -> Request or bool:
        if request.url.endswith('.zip'):
            request.abort()
            return request
        return False
