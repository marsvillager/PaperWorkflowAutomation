import re

from character import handle_special_character
from log import logger
from tools import get_webpage_source, extract_paper_url_without_taxonomy, if_exist, download_file, create_directory


def extract_sp_pdf_urls(html_content: str) -> list:
    """
    提取论文 pdf 地址

    :param html_content: 论文地址
    :return: 论文 pdf 地址
    """
    pattern: str = r'"pdfUrl":"\/stamp\/stamp\.jsp\?tp=&arnumber=(\d+)"'

    return re.findall(pattern, html_content)


def add_prefix_links(pdf_url: str) -> str:
    """
    '/stamp/stamp.jsp?tp=&arnumber=10179411'
    '/stamp/stamp.jsp?tp=&arnumber=10179343'
    正则提取的网址仅有后半段的 arnumber, 需要补全能获取论文的网址前缀

    :param pdf_url: 提取的网址
    :return: 补全前缀的网址
    """
    return "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=" + pdf_url


if __name__ == '__main__':
    proxy: dict[str, str] = {
    }

    # url: str = "https://dblp.org/db/conf/sp/sp2023.html"
    url: str = input("Please input the website of conference: ")
    logger.info(f"Download from <{url}>")

    # parent_dir_name: str = "2023(44th)"
    parent_dir_name: str = input("Please input the name of directory: ")
    create_directory(f"./{parent_dir_name}")
    logger.info(f"Download to './{parent_dir_name}'")

    content: str = get_webpage_source(url, proxy)

    papers: list = extract_paper_url_without_taxonomy(content)

    err_papers: list = []
    for paper_url, paper_title in papers:
        # 特殊字符问题
        paper_title: str = handle_special_character(paper_title)

        paper_path: str = f"{parent_dir_name}/{paper_title}pdf"

        # 若路径已存在, 跳过
        if if_exist(paper_path):
            continue

        # 去除总集
        if "IEEE Symposium on Security and Privacy, SP" in paper_title:
            continue

        pdf_urls: list = extract_sp_pdf_urls(get_webpage_source(paper_url, proxy))

        # 论文 pdf 地址不符合规范(正则表达式)
        if len(pdf_urls) == 0:
            err_papers.append(paper_url)
            logger.error(f"No paper URLs found for '{paper_url}'")
        else:
            # ❓实际发现不加 &ref= 的后缀也可以下载
            download_file(add_prefix_links(pdf_urls[0]), paper_path, proxy)

    print("\n")
    for err in err_papers:
        logger.error(f"未成功下载论文地址: {err}")
