import feedparser
import os
from datetime import datetime
from openai import OpenAI

print("ニュース取得開始")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

rss_url = "https://feeds.bbci.co.uk/news/world/rss.xml"
feed = feedparser.parse(rss_url)

links = ""

for i, entry in enumerate(feed.entries[:10], start=1):

    title = entry.title
    summary = entry.summary
    date = datetime.now().strftime("%Y-%m-%d")

    print("ニュース:", title)

    # SEOタイトル生成
    seo_prompt = f"""
次のニュースから
日本人がクリックしたくなるニュースタイトルを作ってください。

{title}
"""

    seo_title = client.responses.create(
        model="gpt-4.1-mini",
        input=seo_prompt
    ).output_text.strip()

    # 記事生成
    article_prompt = f"""
あなたは戦争分析ニュースの専門ライターです。

以下の構成で記事を書いてください。

① 現在の戦争状況  
② 日本経済への影響  
③ 今後どうなる可能性があるか  
④ 日本が取るべき対策  
⑤ なぜこの戦争が起きたのか  
⑥ 今後の予測シナリオ  

ルール

・オリジナル文章
・分析形式
・最後に参考情報を書く

ニュースタイトル
{title}

ニュース内容
{summary}
"""

    article = client.responses.create(
        model="gpt-4.1-mini",
        input=article_prompt
    ).output_text

    # AI画像生成
    image = client.images.generate(
        model="gpt-image-1",
        prompt="国際戦争ニュースの分析記事用イメージ。世界地図、緊張した国際情勢。",
        size="1024x1024"
    )

    image_url = image.data[0].url

    # SEO URL
    slug = seo_title.replace(" ", "-")[:40]

    filename = f"articles/{slug}.html"

    html = f"""
<html>

<head>

<meta charset="UTF-8">
<title>{seo_title}</title>

<style>

body {{
font-family: Arial;
max-width:900px;
margin:auto;
padding:20px;
line-height:1.8;
}}

.category {{
background:black;
color:white;
display:inline-block;
padding:5px 10px;
}}

img {{
width:100%;
margin:20px 0;
}}

</style>

</head>

<body>

<div class="category">戦争分析</div>

<h1>{seo_title}</h1>

<p>{date}</p>

<img src="{image_url}">

<p>{article.replace(chr(10),"<br>")}</p>

</body>

</html>
"""

    os.makedirs("articles", exist_ok=True)

    with open(filename,"w",encoding="utf-8") as f:
        f.write(html)

    links += f'<li><a href="{filename}">{seo_title}</a></li>'

# トップページ

index_html = f"""
<html>

<head>

<meta charset="UTF-8">
<title>戦争分析ニュース</title>

<style>

body {{
font-family: Arial;
max-width:900px;
margin:auto;
padding:20px;
}}

li {{
margin:15px 0;
}}

</style>

</head>

<body>

<h1>戦争分析ニュース</h1>

<p>世界の戦争と日本経済への影響を分析するニュースサイト</p>

<ul>

{links}

</ul>

</body>

</html>
"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(index_html)

print("サイト更新完了")