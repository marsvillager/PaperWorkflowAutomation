import re

from character import handle_special_character, handle_directory
from log import logger
from tools import get_webpage_source, create_directory, download_file, extract_taxonomy


def extract_ndss_pdf_urls(html_content: str) -> list:
    """
    提取论文 pdf 地址

    :param html_content: 论文地址
    :return: 论文 pdf 地址
    """
    pattern: str = r'href="(https?://.*?\.pdf)"'

    return re.findall(pattern, html_content)


if __name__ == '__main__':
    # url: str = "https://dblp.uni-trier.de/db/conf/ndss/ndss2023.html"
    url: str = "https://dblp.uni-trier.de/db/conf/ndss/ndss2021.html"
    logger.info(f"Download from <{url}>")

    # parent_dir_name: str = "2023(30th)"
    parent_dir_name: str = "2021(28th)"
    logger.info(f"Download to './{parent_dir_name}'")

    content: str = get_webpage_source(url)
    taxonomy: dict = extract_taxonomy(content)

    err_papers: list = []
    for taxonomy, papers in taxonomy.items():
        # 特殊字符问题
        taxonomy: str = handle_directory(taxonomy)

        create_directory(f"./{parent_dir_name}/{taxonomy}")

        for paper_url, paper_title in papers:
            pdf_urls: list = extract_ndss_pdf_urls(get_webpage_source(paper_url))
            # 论文 pdf 地址不符合规范(正则表达式)
            if len(pdf_urls) == 0:
                err_papers.append(paper_url)
                logger.error(f"No paper URLs found for '{paper_url}'")
            else:
                # 特殊字符问题
                paper_title: str = handle_special_character(paper_title)

                download_file(pdf_urls[0], f"{parent_dir_name}/{taxonomy}/{paper_title}pdf")

    print("\n")
    for err in err_papers:
        logger.error(f"未成功下载论文地址: {err}")
