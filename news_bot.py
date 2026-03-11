import feedparser
from openai import OpenAI

print("ニュース取得プログラム開始")

# OpenAI設定
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# RSSニュース
rss_url = "https://feeds.bbci.co.uk/news/world/rss.xml"

feed = feedparser.parse(rss_url)

print("ニュース一覧:")

# ニュース3件
for i, entry in enumerate(feed.entries[:3], start=1):

    title = entry.title
    summary = entry.summary

    print("ニュースタイトル:", title)

    # AIに記事を書かせる
    prompt = f"""
次のニュースを日本語でわかりやすく説明してください。

タイトル:
{title}

内容:
{summary}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    article = response.output_text

    print("\nAI記事:\n")
    print(article)

    # HTML作成
    html_content = f"""
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
</head>
<body>
<h1>{title}</h1>
<p>{article}</p>
</body>
</html>
"""

    # ファイル保存
    filename = f"output/article_{i}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("HTML記事を保存しました:", filename)


# index.html作成
links = ""

for i in range(1, 4):
    links += f'<li><a href="output/article_{i}.html">記事{i}</a></li>\n'

index_html = f"""
<html>
<head>
<meta charset="UTF-8">
<title>AIニュースサイト</title>
</head>

<body>

<h1>AIニュースサイト</h1>

<ul>
{links}
</ul>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("index.html を作成しました")

# index.htmlを自動生成

links = ""

for i in range(1, 4):
    links += f'<li><a href="output/article_{i}.html">記事{i}</a></li>\n'

index_html = f"""
<html>
<head>
<meta charset="UTF-8">
<title>AIニュースサイト</title>
</head>

<body>

<h1>AIニュースサイト</h1>

<ul>
{links}
</ul>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("index.html を更新しました")