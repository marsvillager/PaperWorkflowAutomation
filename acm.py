import re

from character import handle_special_character, handle_directory
from log import logger
from tools import get_webpage_source, create_directory, download_file, extract_taxonomy, if_exist


def extract_acm_pdf_urls(html_content: str) -> list:
    """
    提取论文 pdf 地址

    :param html_content: 论文地址
    :return: 论文 pdf 地址
    """
    pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]+)"[^>]*?\btarget="_blank"\s+class="btn red"[^>]*>'

    return re.findall(pattern, html_content)


def add_prefix_links(pdf_url: str) -> str:
    """
    <a href="/doi/pdf/10.1145/3471621.3471854" title="PDF" target="_blank" class="btn red">
    <a href="/doi/pdf/10.1145/3471621.3471841" title="PDF" target="_blank" class="btn red">
    正则提取的网址仅有后半段即 /doi/pdf/10.1145/3471621.3471841, 需要补全前缀

    :param pdf_url: 提取的网址
    :return: 补全前缀的网址
    """
    return "https://dl.acm.org" + pdf_url


if __name__ == '__main__':
    # IP 被墙时输入代理以修改 IP
    proxy: dict[str, str] = {
    }

    # url: str = "https://dblp.org/db/conf/raid/raid2021.html"
    url: str = "https://dblp.org/db/conf/acsac/acsac2020.html"
    logger.info(f"Download from <{url}>")

    # parent_dir_name: str = "2021(24th)"
    parent_dir_name: str = "2020(36h)"
    logger.info(f"Download to './{parent_dir_name}'")

    content: str = get_webpage_source(url, proxy)
    taxonomies: dict = extract_taxonomy(content)

    err_papers: list = []
    for taxonomy, papers in taxonomies.items():
        # 特殊字符问题
        taxonomy: str = handle_directory(taxonomy)

        create_directory(f"./{parent_dir_name}/{taxonomy}")

        for paper_url, paper_title in papers:
            pdf_urls: list = extract_acm_pdf_urls(get_webpage_source(paper_url, proxy))

            # 论文 pdf 地址不符合规范(正则表达式)
            if len(pdf_urls) == 0:
                err_papers.append(paper_url)
                logger.error(f"No paper URLs found for '{paper_url}'")
            else:
                # 特殊字符问题
                paper_title: str = handle_special_character(paper_title)

                paper_path: str = f"{parent_dir_name}/{taxonomy}/{paper_title}pdf"

                # 若路径已存在, 跳过
                if not if_exist(paper_path):
                    download_file(add_prefix_links(pdf_urls[0]), paper_path, proxy)

    print("\n")
    for err in err_papers:
        logger.error(f"未成功下载论文地址: {err}")
