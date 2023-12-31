import os
import re
import requests

from log import logger


def get_webpage_source(url: str, proxy: dict[str, str]):
    """
    获取网页源码

    :param url: 网页地址
    :param proxy: 代理
    :return: 网页地址源代码
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
    }

    try:
        response = requests.get(url, headers=headers, proxies=proxy)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Failed to fetch webpage. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return None


def get_webpage_source_by_browser(url: str, driver):
    """
    通过 Selenium 模拟浏览器的行为以获取网页源代码

    :param url: 网页地址
    :param driver: 浏览器实例
    :return: 网页地址源代码
    """
    # 访问网页
    driver.get(url)

    # 获取网页源代码
    page_source = driver.page_source

    return page_source


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


def download_file(url: str, save_path: str, proxy: dict[str, str]) -> None:
    """
    下载论文

    :param url: 论文地址
    :param save_path: 保存地址
    :param proxy: 代理
    :return: None
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
    }

    try:
        response = requests.get(url, headers=headers, proxies=proxy)
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


def extract_taxonomy(html_content: str) -> dict:
    """
    使用正则表达式提取特征, 获取分类及其下的论文

    :param html_content: HTML 内容
    :return: 匹配得到的分类及其对应分类下的论文标题、论文网址
    """
    taxonomy_pattern: str = r'<h2 id="([^"]+)">([^<]+)</h2>([\s\S]*?)(?=(?:<h2 id="|$))'
    matches: list = re.findall(taxonomy_pattern, html_content)

    taxonomy_dict: dict = {}
    for match in matches:
        taxonomy_id, taxonomy_title, paper_content = match

        paper_pattern = r'<a href="([^"]+)" itemprop="url">[\s\S]*?<span class="title" itemprop="name">([^<]+)</span>'
        papers_list: list = re.findall(paper_pattern, paper_content)

        taxonomy_dict[taxonomy_title] = papers_list

    return taxonomy_dict


def extract_paper_url_without_taxonomy(html_content: str) -> list:
    """
    使用正则表达式提取特征, 获取论文

    :param html_content: HTML 内容
    :return: 匹配得到论文标题、论文网址
    """
    paper_pattern = r'<a href="([^"]+)" itemprop="url">[\s\S]*?<span class="title" itemprop="name">([^<]+)</span>'
    return re.findall(paper_pattern, html_content)


def if_exist(paper_path: str) -> bool:
    """
    判断论文路径是否已存在, 避免重复下载

    :param paper_path: 论文路径
    :return: 是否存在
    """
    if os.path.exists(paper_path):
        logger.warning(f"The paper path '{paper_path}' already exists. Skipping....")

        return True

    return False
