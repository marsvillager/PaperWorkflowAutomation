import re

from character import handle_special_character, handle_directory
from log import logger
from tools import get_webpage_source, create_directory, download_file, extract_taxonomy, if_exist


def extract_usenix_pdf_urls(html_content: str) -> list:
    """
    提取论文 pdf 地址

    :param html_content: 论文地址
    :return: 论文 pdf 地址
    """
    pattern: str = r'<meta\s+name="citation_pdf_url"\s+content="([^"]+)"\s*/>'

    return re.findall(pattern, html_content)


if __name__ == '__main__':
    proxy: dict[str, str] = {
    }

    # url: str = "https://dblp.uni-trier.de/db/conf/uss/uss2023.html"
    url: str = input("Please input the website of conference: ")
    logger.info(f"Download from <{url}>")

    # parent_dir_name: str = "usenix_paper_2023"
    parent_dir_name: str = input("Please input the name of directory: ")
    logger.info(f"Download to './{parent_dir_name}'")

    content: str = get_webpage_source(url, proxy)
    taxonomies: dict = extract_taxonomy(content)

    err_papers: list = []
    for taxonomy, papers in taxonomies.items():
        # 特殊字符问题
        taxonomy: str = handle_directory(taxonomy)

        create_directory(f"./{parent_dir_name}/{taxonomy}")

        for paper_url, paper_title in papers:
            # 特殊字符问题
            paper_title: str = handle_special_character(paper_title)

            paper_path: str = f"{parent_dir_name}/{taxonomy}/{paper_title}pdf"

            # 若路径已存在, 跳过
            if if_exist(paper_path):
                continue

            pdf_urls: list = extract_usenix_pdf_urls(get_webpage_source(paper_url, proxy))

            # 论文 pdf 地址不符合规范(正则表达式)
            if len(pdf_urls) == 0:
                err_papers.append(paper_url)
                logger.error(f"No paper URLs found for '{paper_url}'")
            else:
                download_file(pdf_urls[0], paper_path, proxy)

    print("\n")
    for err in err_papers:
        logger.error(f"未成功下载论文地址: {err}")
