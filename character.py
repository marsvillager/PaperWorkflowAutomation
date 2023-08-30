def handle_special_character(title: str) -> str:
    """
    处理特殊字符

    :param title: 带有特殊字符的标题
    :return: 修正后的标题
    """
    title: str = title.replace(': ', '：')
    title: str = title.replace('/', ' or ')
    title: str = title.replace('&#34;', '\'')  # HTML 中双引号编码成 &#34;
    title: str = title.replace('&#38;', '&')  # HTML 中 & 编码成 &#38;
    title: str = title.replace('&#181;', 'μ')  # HTML 中 μ 编码成 &#181;
    title: str = title.replace('&#241;', 'ñ')  # HTML 中 ñ 编码成 &#241;
    title: str = title.replace('&#248;', 'ø')  # HTML 中 ø 编码成 &#248;
    title: str = title.replace('&#956;', 'μ')  # HTML 中 μ 编码成 &#956;
    title: str = title.replace('?', '.')
    title: str = title.replace('!', '.')
    title: str = title.replace('\n', ' ')

    return title


def handle_directory(directory: str) -> str:
    """
    处理特殊字符

    :param title: 带有特殊字符的目录名称
    :return: 修正后的目录名称
    """
    directory: str = directory.replace('&#34;', '"')  # HTML 中双引号编码成 &#34;
    directory: str = directory.replace('&#38;', '&')  # HTML 中 & 编码成 &#38;
    directory: str = directory.replace(': ', '：')
    directory: str = directory.replace('.', '')
    directory: str = directory.replace('...', '')
    directory: str = directory.replace('\n', ' ')

    return directory
