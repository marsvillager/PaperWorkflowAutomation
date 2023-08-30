# <img src="./img/usenix_logo_300x150_neat_2.png" alt="usenix" style="zoom:33%;" />  [USENIX Security](https://dblp.uni-trier.de/db/conf/uss/index.html)

## Use

输入**会议地址**和**要保存的目录名称**

```python
url: str = "https://dblp.uni-trier.de/db/conf/uss/uss2023.html"
parent_dir_name: str = "usenix_paper_2023"
```

## Details

### 1. 关键信息

#### （1）大标题

```html
<h2 id="secBreakingWirelessProtocols">Breaking Wireless Protocols</h2>
<h2 id="secInterpersonalAbuse">Interpersonal Abuse</h2>
```

正则表达：

```python
pattern = r'<h2 id="[^"]+">([^<]+)</h2>'
```

#### （2）论文题目

```html
<span class="title" itemprop="name">PhyAuth: Physical-Layer Message Authentication for ZigBee Networks.</span>
<span class="title" itemprop="name">Time for Change: How Clocks Break UWB Secure Ranging.</span>
```

正则表达：

```python
pattern = r'<span class="title" itemprop="name">([^<]+)</span>'
```

#### （3）论文地址

```html
<a href="https://www.usenix.org/conference/usenixsecurity23/presentation/li-ang" itemprop="url">
<a href="https://www.usenix.org/conference/usenixsecurity23/presentation/anliker" itemprop="url">
```

正则表达：

```python
pattern = r'<a\s+href="([^"]+)"\s+itemprop="url">'
```

### 2. 获取论文

```html
<meta name="citation_pdf_url" content="https://www.usenix.org/system/files/usenixsecurity23-dong-feng.pdf" />
```

正则表达：

```python
pattern = r'<meta\s+name="citation_pdf_url"\s+content="([^"]+)"\s*/>'
```

### 3. 遗漏

```python
err_papers: list = []

# 论文 pdf 地址不符合规范(正则表达式)
if len(pdf_urls) == 0:
		err_papers.append(paper_url)
		print(f"No paper URLs found for '{paper_url}'")
    
for err in err_papers:
    print(f"未成功下载论文地址: {err}")
```

# <img src="./img/ieee_logo_white.svg" alt="ieee" width="20%">  [S&P](https://dblp.org/db/conf/sp/index.html)

> - S&P 本身是分类了的，但在官网却没有分类归纳，只能从《Table of Contents》中得知分类信息
> - 需要登录信息，爬取返回 418
> - 官网可批量下载，较为方便

# <img src="./img/NDSS-Logo-120x37.svg" alt="ndss"/> [NDSS](https://dblp.uni-trier.de/db/conf/ndss/index.html)

## Use

输入**会议地址**和**要保存的目录名称**

```python
url: str = "https://dblp.uni-trier.de/db/conf/ndss/ndss2023.html"
parent_dir_name: str = "2023(30th)"
```

## Details

### 获取论文

> 其它部分均与 USENIX Security 一样，只有在官网获取论文的部分有所区别

```html
<a role="button" class="btn btn-light btn-sm pdf-button" target="_blank" href="https://www.ndss-symposium.org/wp-content/uploads/2023-289-paper.pdf">Paper</a>

<a role="button" class="btn btn-light btn-sm pdf-button" target="_blank" href="https://www.ndss-symposium.org/wp-content/uploads/2023-362-paper.pdf">Paper</a>
```

正则表达：

```python
pattern = r'href="(https?://.*?\.pdf)"'
```

# <img src="./img/acm-logo-3.png" alt="ACM"/> ACM

## Use

> ⚠️ ACM 有可能会因为爬虫遇到 [ERROR] Failed to fetch webpage. Status code: 403, 此时 ACM 会封锁你的 IP: Your IP Address has been blocked, Please contact [dl-support@acm.org](mailto:dl-support@acm.org)

输入**会议地址**和**要保存的目录名称**

### 1. [ACSAC](https://dblp.org/db/conf/acsac/index.html)

```python
url: str = "https://dblp.org/db/conf/acsac/acsac2022.html"
parent_dir_name: str = "2022(38th)"
```

### 2. [RAID](https://dblp.org/db/conf/raid/index.html)

```python
url: str = "https://dblp.org/db/conf/raid/raid2022.html"
parent_dir_name: str = "2022(25th)"
```

## Details

### 获取论文

> 其它部分均与 USENIX Security 一样，只有在官网获取论文的部分有所区别

```html
<a href="/doi/pdf/10.1145/3471621.3471854" title="PDF" target="_blank" class="btn red">
  
<a href="/doi/pdf/10.1145/3471621.3471841" title="PDF" target="_blank" class="btn red">
```

正则表达：

```python
pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]+)"[^>]*?\btarget="_blank"\s+class="btn red"[^>]*>'
```

补上前缀：

```python
def add_prefix_links(pdf_url: str) -> str:
    """
    正则提取的网址仅有后半段即 /doi/pdf/10.1145/3471621.3471841, 需要补全前缀

    :param pdf_url: 提取的网址
    :return: 补全前缀的网址
    """
    return "https://dl.acm.org" + pdf_url
```

# Appendix

## 网页源代码

```python
def get_webpage_source(url: str):
    """
    获取网页源码

    :param url: 网页地址
    :return: 网页地址源代码
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch webpage. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
```

## 特殊字符问题

### 1. 目录名称

```python
directory: str = directory.replace('&#34;', '"')  # HTML 中双引号编码成 &#34;
directory: str = directory.replace('&#38;', '&')  # HTML 中 & 编码成 &#38;
directory: str = directory.replace(': ', '：')
directory: str = directory.replace('.', '')
directory: str = directory.replace('...', '')
directory: str = directory.replace('\n', ' ')
```

### 2. 标题名称

有些操作系统的文件名和文件夹名不能包含以下特殊字符：\ / : * ? " < > |

```python
paper_title: str = paper_title.replace(': ', '：')
paper_title: str = paper_title.replace('/', ' or ')
paper_title: str = title.replace('\n', ' ')
paper_title: str = paper_title.replace('&#34;', '"')  # HTML 中双引号编码成 &#34;
paper_title: str = title.replace('&#38;', '&')  # HTML 中 & 编码成 &#38;
paper_title: str = paper_title.replace('&#181;', 'μ')  # HTML 中 μ 编码成 &#181;
paper_title: str = title.replace('&#241;', 'ñ')  # HTML 中 ñ 编码成 &#241;
paper_title: str = title.replace('&#248;', 'ø')  # HTML 中 ø 编码成 &#248;

# 有些论文以问号或感叹号结尾, 但这里下载用的它原本的 . 加 pdf, 所以需要统一转为 .
paper_title: str = paper_title.replace('?', '.') 
paper_title: str = paper_title.replace('!', '.')  
```
