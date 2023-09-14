import json
import os
import requests
import sys
import time

from log import logger


def add_pdf_via_file_upload(filepath: str, chatpdf_api_key: str, proxy: dict[str, str]):
    """
    Add a PDF file by uploading it to ChatPDF as a multipart form data. You can only upload one file at a time.
    This endpoint returns a source ID that can be used to interact with the PDF file.

    :param filepath: paper or set of paper
    :param chatpdf_api_key: you can find your API key in https://www.chatpdf.com/
    :param proxy:
    :return:
    """
    files = [
        ('file', ('file', open(filepath, 'rb'), 'application/octet-stream'))
    ]

    headers = {
        'x-api-key': chatpdf_api_key
    }

    response = requests.post('https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files, proxies=proxy)

    if response.status_code == 200:
        source_id: str = response.json()['sourceId']
        logger.info('Source ID: %s', source_id)

        return source_id
    else:
        logger.error('Status: %s', response.status_code)
        logger.error('Error: %s', response.text)

        return None


def chat_with_pdf(chatpdf_api_key: str, source_id: str, messages: list, proxy: dict[str, str]):
    """
    Send a chat message to a PDF file using its source ID.

    :param chatpdf_api_key:
    :param source_id:
    :param content:
    :param proxy:
    :return:
    """
    headers = {
        'x-api-key': chatpdf_api_key,
        "Content-Type": "application/json",
    }

    data = {
        'sourceId': source_id,
        'messages': messages
    }

    response = requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data, proxies=proxy)

    if response.status_code == 200:
        content: str = response.json()['content']
        logger.info('Result: %s', content)

        return content
    else:
        logger.error('Status: %s', response.status_code)
        logger.error('Error: %s', response.text)
        return None


def find_pdf(target_directory: str) -> list:
    """

    :param target_directory:
    :return:
    """
    # 定义一个空列表来存储PDF文件的路径
    pdf_files = []

    # 遍历目录及其子目录
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            # 检查文件扩展名是否为.pdf
            if file.endswith('.pdf'):
                # 构建完整的文件路径并添加到pdf_files列表中
                pdf_files.append(os.path.join(root, file))

    return pdf_files


if __name__ == '__main__':
    # proxy
    ports: str = input("Please input the proxy port number(default is 1087): ") or '1087'
    proxies: dict[str, str] = {
        # 'http': f'http://127.0.0.1:{ports}',
        # 'https': f'http://127.0.0.1:{ports}'
    }
    logger.info(f"Your proxy is http://127.0.0.1:{ports}")
    time.sleep(0.5)

    # ChatPDF API key
    chatpdf: str = input("Please input the API Key of ChatPDF(You can find your API key in https://www.chatpdf.com/): ")
    logger.info(f"Your API key is <{chatpdf}>")
    time.sleep(0.5)

    # messages
    user_requests_1: list = [
        {
            'role': "user",
            'content': '请将论文开头的摘要部分完整地提取出来并逐句翻译为中文'
        }
    ]
    user_requests_2: list = [
        {
            'role': "user",
            'content': input(
                "Please input the ask question about the paper: (or use default)")
                       or "请用一长段话连贯地讲述论文的核心问题、主要贡献、解决方法等（中文表述）"
        }
    ]

    # result path
    saved_path: str = input(
        "Please input the path to save results(default is ./summary/sp_2023.json): ") or './summary/sp_2023.json'
    logger.info(f"Saved path is <{saved_path}>")
    time.sleep(0.5)

    # paper path
    papers: str = input(
        "Please input the absolute path of papers: "
        "(If it's not a PDF file, then traverse the files in its subdirectories)\n")
    logger.info(f"Upload from <{papers}>")
    
    # process
    paper_list: list = []

    summary_papers: dict = {}  # summary of item_paper
    # 避免重复上传
    if os.path.exists(saved_path):
        with open(saved_path, "r", encoding='utf-8') as json_file:
            summary_papers = json.load(json_file)

    if os.path.splitext(papers)[1] == '.pdf':  # pdf 文件
        paper_list.append(papers)
    else:
        paper_list: list = find_pdf(papers)  # 目录
    for paper in paper_list:
        # 跳过已处理文件
        if paper in summary_papers:
            logger.warning(f'<{paper}> has already been processed.')
            continue

        item_paper: dict = {}  # directory, name, abstract(self), abstract(gpt)

        paper_id: str = add_pdf_via_file_upload(paper, chatpdf, proxies)

        if paper_id is None:
            # 保存已处理结果
            with open(saved_path, 'w', encoding='utf-8') as file:
                json.dump(summary_papers, file, indent=4, ensure_ascii=False)
            logger.info(f"Results saved to <{saved_path}>")
            sys.exit()

        item_paper['src_id'] = paper_id
        item_paper['abstract(self)'] = chat_with_pdf(chatpdf, paper_id, user_requests_1, proxies)
        item_paper['abstract(gpt)'] = chat_with_pdf(chatpdf, paper_id, user_requests_2, proxies)
        summary_papers[paper] = item_paper

    with open(saved_path, 'w', encoding='utf-8') as file:
        json.dump(summary_papers, file, indent=4, ensure_ascii=False)
    logger.info(f"Results saved to <{saved_path}>")
