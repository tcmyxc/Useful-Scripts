import os

path = "path/to/folder"  # 文件夹路径
# 文件夹中所有文件的文件名（all file names)
file_names = os.listdir(path)

for name in file_names:
    old_name = name
    # 下划线就是你想修改的字符
    if "_" in old_name:
        # print(old_name)
        # 这里我把下划线变成了中文的冒号
        new_name = str(old_name).replace("_", "：")
        print(new_name)
        # 重命名文件
        os.renames(os.path.join(path, name),os.path.join(path, new_name)) 
