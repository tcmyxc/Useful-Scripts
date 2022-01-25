# -*- coding: utf-8 -*-
# from https://blog.csdn.net/ezreal_tao/article/details/107411294

import platform


def judge_platform() -> None:
    r"""判断操作系统是 Windows 还是 Linux"""

    if platform.system().lower() == "windows":
        print("Windows")
    elif platform.system().lower() == "linux":
        print("Linux")


if __name__ == "__main__":
    judge_platform()