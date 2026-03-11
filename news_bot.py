import feedparser
import os
import base64
from datetime import datetime
from openai import OpenAI

print("ニュース生成開始")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# フォルダ作成
os.makedirs("articles", exist_ok=True)
os.makedirs("images", exist_ok=True)

rss_url = "https://feeds.bbci.co.uk/news/world/rss.xml"
feed = feedparser.parse(rss_url)

cards = ""

for i, entry in enumerate(feed.entries[:6], start=1):

    title = entry.title
    summary = entry.summary
    date = datetime.now().strftime("%Y-%m-%d")

    print("ニュース:", title)

    # カテゴリー判定
    category_prompt = f"""
このニュースを次のカテゴリーから1つ選んでください

戦争
日本経済
世界情勢
安全保障
エネルギー

ニュース:
{title}
"""

    category = client.responses.create(
        model="gpt-4.1-mini",
        input=category_prompt
    ).output_text.strip()

    # 記事作成
    article_prompt = f"""
あなたは戦争と世界情勢を分析するニュース記者です。

以下の構成で記事を書いてください

① 今起きていること
② 日本への影響
③ 今後どうなるか
④ 日本の対策
⑤ なぜ起きたのか
⑥ 未来シナリオ

最後に参考情報を書く

ニュース
{title}

内容
{summary}
"""

    article = client.responses.create(
        model="gpt-4.1-mini",
        input=article_prompt
    ).output_text

    # サムネイル生成
    image = client.images.generate(
        model="gpt-image-1",
        prompt=f"ニュース記事サムネイル 世界地図と国際情勢 {category}",
        size="1024x1024"
    )

    image_base64 = image.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    image_file = f"images/thumb{i}.png"

    with open(image_file,"wb") as f:
        f.write(image_bytes)

    filename = f"articles/article{i}.html"

    html = f"""
<html>

<head>

<meta charset="UTF-8">

<title>{title}</title>

<style>

body{{
background:#0f172a;
color:white;
font-family:Arial;
max-width:900px;
margin:auto;
padding:20px;
line-height:1.8;
}}

.category{{
background:#b91c1c;
display:inline-block;
padding:4px 10px;
margin-bottom:10px;
}}

img{{
width:100%;
margin:20px 0;
}}

.back{{
display:inline-block;
margin-top:40px;
color:#f59e0b;
}}

</style>

</head>

<body>

<div class="category">{category}</div>

<h1>{title}</h1>

<p>{date}</p>

<img src="../{image_file}">

<p>{article.replace(chr(10),"<br>")}</p>

<a class="back" href="../index.html">← ニュース一覧へ戻る</a>

</body>

</html>
"""

    with open(filename,"w",encoding="utf-8") as f:
        f.write(html)

    cards += f"""

<div class="card">

<a href="{filename}">
<img src="{image_file}">
<h2>{title}</h2>
</a>

<p>{category}</p>

</div>

"""

# トップページ

index = f"""
<html>

<head>

<meta charset="UTF-8">

<title>戦争分析ニュース</title>

<style>

body{{
background:#0f172a;
color:white;
font-family:Arial;
max-width:1000px;
margin:auto;
padding:20px;
}}

h1{{
border-bottom:3px solid #b91c1c;
padding-bottom:10px;
}}

.card{{
background:#1e293b;
padding:15px;
margin-bottom:25px;
border-radius:10px;
}}

.card img{{
width:100%;
border-radius:8px;
}}

a{{
color:white;
text-decoration:none;
}}

</style>

</head>

<body>

<h1>戦争分析ニュース</h1>

<p>戦争・世界情勢・日本経済を分析するニュースサイト</p>

{cards}

</body>

</html>
"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(index)

print("サイト更新完了")
