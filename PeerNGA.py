import os
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class PeerNGA:
    def __init__(self, saveDir):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': saveDir}
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--incognito')

        self.browser = webdriver.Chrome(chrome_options=options)

        self.saveDir = saveDir
        self.states = {
            "sign in": False,
            'enter database': False,
            'search records': False
        }

    def signIn(self, email, password):
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

    def close(self):
        self.browser.quit()

    @staticmethod
    def __checkStates(level):
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

    @__checkStates(1)
    def enterDB(self, label):
        DBdict = {
            'NGA West2': 1,
            'NGA east': 2
        }
        self.browser.get('https://ngawest2.berkeley.edu/spectras/new?sourceDb_flag={0}'.format(DBdict[label]))
        self.browser.execute_script('OnSubmit()')
        WebDriverWait(self.browser, 10).until(lambda x: x.find_element(By.NAME, "search[search_nga_number]"))
        self.states['enter database'] = True

    @__checkStates(2)
    def search(self, settings=None):
        self.states['search records'] = True

        if not settings:
            self.__clickBtnSearch()
            return None

        for label in settings:
            elemName = self.__getElemName(label)
            if elemName:
                inputElem = self.browser.find_element(By.NAME, elemName)
                inputElem.send_keys(settings[label])

        self.__clickBtnSearch()

    @__checkStates(3)
    def download(self):
        saveDir = self.saveDir
        self.browser.execute_script('getSelectedResult(true)')
        alert = self.browser.switch_to.alert
        alert.accept()
        alert = self.browser.switch_to.alert
        alert.accept()

        zipName = WebDriverWait(self.browser, 10).until(lambda x: self.__findZip(saveDir))
        zipPath = os.path.join(saveDir, zipName)
        self.__unZip(zipPath, saveDir)
        os.remove(zipPath)

    def __clickBtnSearch(self):
        self.browser.execute_script('OnSubmit()')

        divNotice = WebDriverWait(self.browser, 10).until(lambda x: x.find_element(By.ID, 'notice'))
        notice = divNotice.text
        print(notice)

    @staticmethod
    def __getElemName(label):
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
    def __findZip(diR):
        for f in os.listdir(diR):
            if f[-3:] == 'zip':
                return f
        return False

    @staticmethod
    def __unZip(zipPath, exDir):
        zip_file = zipfile.ZipFile(zipPath)
        zip_list = zip_file.namelist()
        for f in zip_list:
            zip_file.extract(f, exDir)
        zip_file.close()

        for f in os.listdir(exDir):
            if f[-3:] == 'csv':
                os.remove(os.path.join(exDir, f))
