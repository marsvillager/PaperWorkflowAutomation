import os
import re
import requests

from character import handle_special_character


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
            print(f"Failed to fetch webpage. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def extract_taxonomy(html_content: str) -> dict:
    """
    使用正则表达式提取特征

    :param html_content: HTML 内容
    :return: 匹配得到的分类及其对应分类下的论文标题
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


def extract_pdf_urls(html_content: str) -> list:
    """
    提取论文 pdf 地址

    :param html_content: 论文地址
    :return: 论文 pdf 地址
    """
    pattern: str = r'<meta\s+name="citation_pdf_url"\s+content="([^"]+)"\s*/>'
    pdf_urls: list = re.findall(pattern, html_content)

    return pdf_urls


def create_directory(directory_path: str) -> None:
    """
    创建文件夹

    :param directory_path: 文件夹目录
    :return: None
    """
    try:
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")
    except OSError as e:
        print(f"An error occurred: {e}")


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
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded and saved at {save_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    url: str = "https://dblp.uni-trier.de/db/conf/uss/uss2023.html"
    parent_dir_name: str = "usenix_paper_2023"

    content: str = get_webpage_source(url)
    taxonomy: dict = extract_taxonomy(content)

    err_papers: list = []
    for taxonomy, papers in taxonomy.items():
        create_directory(f"./{parent_dir_name}/{taxonomy}")

        for paper_url, paper_title in papers:
            pdf_urls: list = extract_pdf_urls(get_webpage_source(paper_url))
            # 论文 pdf 地址不符合规范(正则表达式)
            if len(pdf_urls) == 0:
                err_papers.append(paper_url)
                print(f"No paper URLs found for '{paper_url}'")
            else:
                # 特殊字符问题
                paper_title: str = handle_special_character(paper_title)

                download_file(pdf_urls[0], f"./usenix_paper_2023/{taxonomy}/{paper_title}pdf")

    for err in err_papers:
        print(f"未成功下载论文地址: {err}")
