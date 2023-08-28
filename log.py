import logging
from colorama import init, Fore, Style, Back

# 初始化 colorama, 使颜色在终端中生效
init(autoreset=True)

# 创建一个 Logger 实例
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# 创建一个控制台处理器，并设置日志级别为 DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)


class ColoredFormatter(logging.Formatter):
    """
    设置自定义的 Formatter 类
    """

    def __init__(self, fmt=None, datefmt=None, style='{'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        level_colors = {
            logging.DEBUG: Fore.GREEN,
            logging.INFO: Fore.CYAN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.MAGENTA
        }

        level_color = level_colors.get(record.levelno, Fore.RESET)

        back_colors = {
            logging.WARNING: Back.YELLOW,
            logging.ERROR: Back.RED,
            logging.CRITICAL: Back.MAGENTA
        }

        back_color = back_colors.get(record.levelno, Back.RESET)

        log_format = (
            f"[{Fore.CYAN}{self.formatTime(record, self.datefmt)}{Style.RESET_ALL}]"
            f"[{back_color}{level_color}{record.levelname}{Style.RESET_ALL}]"
        )

        message_colors = {
            logging.DEBUG: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.MAGENTA
        }

        message_color = message_colors.get(record.levelno, Fore.RESET)

        message = (
            f"{message_color}{record.getMessage()}{Style.RESET_ALL}"
        )

        return log_format + " " + message


# 创建一个自定义的日志格式
formatter = ColoredFormatter()
console_handler.setFormatter(formatter)

# 将控制台处理器添加到Logger实例中
logger.addHandler(console_handler)
