import os
import requests

from log import logger


def get_webpage_source(url: str):
    """
    获取网页源码

    :param url: 网页地址
    :return: 网页地址源代码
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Failed to fetch webpage. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return None


def create_directory(directory_path: str) -> None:
    """
    创建文件夹

    :param directory_path: 文件夹目录
    :return: None
    """
    try:
        os.makedirs(directory_path)
        logger.info(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        logger.warning(f"Directory '{directory_path}' already exists.")
    except OSError as e:
        logger.error(f"An error occurred: {e}")


def download_file(url: str, save_path: str) -> None:
    """
    下载论文

    :param url: 论文地址
    :param save_path: 保存地址
    :return: None
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                    logger.info(f"File downloaded and saved at {save_path}")
            except FileNotFoundError:
                logger.error(f"No such file or directory: '{save_path}'")
                exit()
        else:
            logger.error(f"Failed to download file. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
