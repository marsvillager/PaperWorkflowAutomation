import PyPDF2


def extract_pdf_content(pdf_file_path: str):
    pdf_file = open(pdf_file_path, 'rb')

    # 创建 PDF 文件阅读器对象
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # 存储提取的文本内容
    extracted_content = []

    # 遍历每一页
    for page_num in range(len(pdf_reader.pages)):
        # 获取当前页面的文本
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()

        # 如果页面包含 "references"，则停止提取
        if 'references' in page_text.lower():
            break

        extracted_content.append(page_text)

    # 关闭 PDF 文件
    pdf_file.close()

    # 返回提取的内容
    return '\n'.join(extracted_content)
