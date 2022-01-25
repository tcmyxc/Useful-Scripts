# -*- coding: utf-8 -*-
__author__ = "徐文祥(tcmyxc)"

import os
import platform


def list_dir(path: str = None) -> None:
    r"""
    打印给定目录下的所有文件（包括目录），不递归访问子文件夹
    :param path: 给定的目录
    """

    file_names = os.listdir(path)
    for file_name in file_names:
        print(f"{file_name}")


if __name__ == "__main__":
    if platform.system().lower() == "windows":
        list_dir("C:/")
    elif platform.system().lower() == "linux":
        list_dir("/")
