# 需要结合 02 号脚本食用


import time
import sys
import cv2
import torchvision.models as models
from torchsummary import summary
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
    

def main():
    output_file = "imbalance.md"  # 输出文件名
    file_lists = ["2017.csv", "2018.csv", "2019.csv", "2020.csv","2021.csv", "2022.csv"]
    for csv_file in file_lists:
        # use `id` column
        arxiv_id = pd.read_csv(csv_file, usecols=[1])
        # print(arxiv_id)
        # to list
        arxiv_id = arxiv_id.values.flatten().tolist()
        # 追加模式，所以每次需要先删除原先的 md 文件
        with open(output_file, "a", encoding="utf-8") as f:
            for id in (arxiv_id):
                id = str(id)
                # 会莫名少个末尾0，我们这里再加上，之后再写入文件
                if len(id) != 10:
                    id += "0"
                f.write(f"- [{id}]\n")
        
    
        
 
main()
