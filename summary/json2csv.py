import csv
import json
import os
import sys
import time

# 获取当前模块所在的目录
current_dir = os.path.dirname(__file__)
# 获取根目录的路径
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 将根目录添加到模块搜索路径中
sys.path.append(root_dir)
from log import logger


def transfer_json_to_csv(json_file: str, output: str):
    """
    将 json 转化为 csv

    :param json_file: json 文件
    :param output: 指定输出的 CSV文件名
    :return: none
    """
    # 嵌套字典
    with open(json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # 提取嵌套字典中的所有字段名（列名）和 "path" 字段
    fieldnames = set(["path"])
    for key, value in json_data.items():
        fieldnames.update(value.keys())

    # 将数据写入 CSV 文件
    with open(output, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in json_data.items():
            value["path"] = key  # 将 path 字段添加到字典中
            writer.writerow(value)

    logger.info(f"嵌套字典数据已成功转换为 CSV 文件: {csv_file}")

    return None


if __name__ == '__main__':
    # json path
    json_path: str = input("Please input the json path(usually under <PREFIX>/summary/data): ")
    logger.info(f"Load from <{json_path}>")
    time.sleep(0.5)

    # output path
    output_path: str = input("Please input the path for saving(default is <data/output.csv>): ") or 'data/output.csv'
    logger.info(f"Saved in <{output_path}>")
    time.sleep(0.5)

    transfer_json_to_csv(json_path, output_path)
