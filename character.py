def handle_special_character(title: str):
    """
    处理特殊字符

    :param title: 带有特殊字符的标题
    :return: 修正后的标题
    """
    title: str = title.replace(': ', '：')
    title: str = title.replace('/', ' or ')
    title: str = title.replace('&#34;', '"')  # HTML 中双引号编码成 &#34;
    title: str = title.replace('&#181;', 'μ')  # HTML 中 μ 编码成 &#181;
    title: str = title.replace('&#248;', 'ø')  # HTML 中 ø 编码成 &#248;
    title: str = title.replace('?', '.')
    title: str = title.replace('!', '.')

    return title
