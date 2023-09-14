import os
import PyPDF2


def find_pdf(target_directory: str) -> list:
    """
    找到该目录下所有的 pdf 文件

    :param target_directory:
    :return: pdf 列表
    """
    pdf_files: list = []

    # 遍历目录及其子目录
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            # 检查文件扩展名是否为.pdf
            if file.endswith('.pdf'):
                # 构建完整的文件路径并添加到 pdf_files 列表中
                pdf_files.append(os.path.join(root, file))

    return pdf_files


def extract_all_pdf_content(pdf_file_path: str) -> list:
    """
    提取 pdf 内容, 每 4 页为一组(tokens)

    :param pdf_file_path: pdf 路径
    :return: pdf 内容
    """
    pdf_file = open(pdf_file_path, 'rb')

    # 创建 PDF 文件阅读器对象
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # 存储提取的文本内容
    extracted_content: list = []

    # 用于累积每 4 页的文本内容
    current_group = []

    # 遍历每一页
    for page_num in range(len(pdf_reader.pages)):
        # 获取当前页面的文本
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()

        # 如果页面包含 "references"，则停止提取
        if 'references' in page_text.lower():
            break

        # 将当前页的文本添加到当前组中
        current_group.append(page_text)

        # 当达到4页时，将当前组添加到结果列表，并清空当前组
        if len(current_group) == 4:
            extracted_content.append("\n".join(current_group))
            current_group = []

    # 关闭 PDF 文件
    pdf_file.close()

    # 如果当前组不为空，将其添加到结果列表
    if current_group:
        extracted_content.append("\n".join(current_group))

    return extracted_content


def extract_specified_pdf_title(pdf_content: str):
    """
    提取 pdf 标题

    :param pdf_content: pdf 内容
    :return: pdf 标题
    """
    # 将字符串拆分为行
    lines = pdf_content.splitlines()

    if lines:
        # 提取第一行
        first_line = lines[0].strip()  # 去除首尾的空白字符
        return first_line
    else:
        return None


def extract_specified_pdf_content(pdf_content: str, start: str, end: str):
    """
    提取 pdf 特定内容

    :param pdf_content: pdf 内容
    :param start: 开始位置
    :param end: 结束位置
    :return: pdf 摘要
    """
    # 找到开始字符串的位置
    start_index = pdf_content.find(start)

    if start_index != -1:
        # 找到结束字符串的位置，从开始字符串之后开始查找
        end_index = pdf_content.find(end, start_index + len(start))

        if end_index != -1:
            # 提取从开始字符串到结束字符串之间的内容
            extracted_content = pdf_content[start_index + len(start):end_index].strip()
            return extracted_content

    # 如果未找到开始或结束字符串，则返回 None
    return None


# content = extract_all_pdf_content('/Volumes/frp-ask.top-1/Library/Papers/IEEE S&P/2023(44th)SP/Session 1A：Infrastructure security/Red Team vs. Blue Team：A Real-World Hardware Trojan Detection Case Study Across Four Modern CMOS Technology Generations.pdf')
#
# print(extract_specified_pdf_content(content, 'Abstract', '1.'))
