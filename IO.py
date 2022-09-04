import os
import zipfile
import requests
from typing import NoReturn


def unZip(zipPath: str, exDir: str) -> NoReturn:
    zip_file = zipfile.ZipFile(zipPath)
    zip_list = zip_file.namelist()
    for f in zip_list:
        zip_file.extract(f, exDir)
    zip_file.close()


def downloader(url: str, saveName: str, saveDir: str = os.getcwd(), headers: dict = None, params: dict = None) -> str:
    res = requests.get(url, stream=True, params=params, headers=headers)
    savePath = os.path.join(saveDir, saveName)
    total_size = int(res.headers['Content-Length'])

    count = 0
    with open(savePath, "wb") as f:
        for chunk in res.iter_content(chunk_size=1024):
            f.write(chunk)

            count = count + 1
            now_size = count * 1024
            portion = now_size / total_size
            num_bar = int(portion * 20)
            num_blank = 20 - num_bar
            bar = '█' * num_bar
            blank = '_' * num_blank
            print('\rDownloading ... |{0}{1}| {2}%'.format(bar, blank, int(portion * 100)), end='')
    return savePath
