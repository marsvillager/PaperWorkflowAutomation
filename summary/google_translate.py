import json
import os
import requests
import sys
import time

from pdf_tools import find_pdf, extract_group_pdf_content, extract_pdf_title_by_path

# 获取当前模块所在的目录
current_dir = os.path.dirname(__file__)
# 获取根目录的路径
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 将根目录添加到模块搜索路径中
sys.path.append(root_dir)
from log import logger


def translate_abstract(rapid_api_key: str, content: str, proxy: dict[str, str]) -> json:
	"""
	翻译论文摘要部分

	:param rapid_api_key: RapidAPI key
	:param content: 论文内容
	:param proxy: 代理
	:return: 翻译内容
	"""
	url: str = "https://google-translate1.p.rapidapi.com/language/translate/v2"

	payload: dict = {
		"q": content,
		"target": "zh",  # 翻译成中文
		"source": "en"
	}

	headers: dict = {
		"content-type": "application/x-www-form-urlencoded",
		"Accept-Encoding": "application/gzip",
		"X-RapidAPI-Key": rapid_api_key,
		"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
	}

	response = requests.post(url, data=payload, headers=headers, proxies=proxy)
	if "data" in response.json() and isinstance(response.json()["data"], dict) and len(
			response.json()["data"]) > 0:  # data 存在且为非空列表
		content: str = response.json()["data"]["translations"][0]["translatedText"]
		logger.debug(f"Translating...")

		return content
	else:  # choices 不存在或为空列表
		logger.error(f"RapidAPI has a processing error: {response.json()}")
		sys.exit()


if __name__ == '__main__':
	# proxy, 最好不直接用代理, 路由器接代理更不易察觉
	# ports: str = input("Please input the proxy port number(default is 1087): ") or '1087'
	proxies: dict[str, str] = {
		# 'http': f'http://127.0.0.1:{ports}',
		# 'https': f'http://127.0.0.1:{ports}'
	}
	# logger.info(f"Your proxy is http://127.0.0.1:{ports}")
	# time.sleep(0.5)

	# RapidAPI API key
	rapid_api: str = input("Please input the API Key of RapidAPI: ")
	logger.info(f"Your API key is <{rapid_api}>")
	time.sleep(0.5)

	# result path
	saved_path: str = input(
		"Please input the path to save results(default is ./data/sp_2023.json): ") or './data/sp_2023.json'
	logger.info(f"Saved path is <{saved_path}>")
	time.sleep(0.5)

	# paper path
	papers: str = input(
		"Please input the absolute path of papers: "
		"(If it's not a PDF file, then traverse the files in its subdirectories)\n")
	logger.info(f"Process <{papers}>")

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
		# 跳过 Table of Contents.pdf
		if "Table of Contents.pdf" in paper:
			logger.warning(f'Skipping <{paper}>.')
			continue

		# 跳过已处理文件
		if paper in summary_papers:
			logger.warning(f'<{paper}> has already been processed.')
			continue

		item_paper: dict = {}  # title, abstract(self), abstract(gpt)

		paper_content: list = extract_group_pdf_content(paper, 2)

		logger.debug(f"Processing <{paper}> ...")

		item_paper['title'] = extract_pdf_title_by_path(paper)  # ⚠️ 如果论文路径包含论文题目则推荐通过路径获取题目
		# item_paper['title'] = extract_pdf_title_by_content(paper_content)  # ⚠️ 通过内容获取可能不准确, 因为只取 pdf 第一行
		item_paper['abstract'] = translate_abstract(rapid_api, paper_content[0], proxies)  # basic: 5 requests per second

		summary_papers[paper] = item_paper

		# 以防万一保存已处理结果
		with open(saved_path, 'w', encoding='utf-8') as file:
			json.dump(summary_papers, file, indent=4, ensure_ascii=False)
		logger.info(f"Results saved to <{saved_path}>")
