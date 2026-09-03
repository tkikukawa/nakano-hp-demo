# -*- coding: utf-8 -*-
"""
研究室サイト ビルドスクリプト

  data/    … 中身のデータ（CSV）。ニュースや業績を足すときはここに1行足す
  pages/   … 本文だけを書いたHTMLの断片
  assets/  … スタイルシートと画像
       ↓  python build.py
  docs/    … 出来上がったサイト。このフォルダごと公開する

トップに出るのは「現行デザインの再現」版。
CMSを使わず、HTMLとCSSだけで今のサイトと同じ見た目を出している。
デザイン候補（案A・案B・案C）は build_variants.py が docs/styles/ に作る。

使い方:  python build.py
"""
import csv, os, shutil, html, io

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "docs")

SITE_NAME = "サンプル研究室"
SITE_SUB = "◯◯大学大学院工学研究科　マテリアル工学専攻"

# 左メニューに並べるページ（上から順に）
NAV = [
    ("ホーム", ""),
    ("研究内容", "research/"),
    ("メンバー", "members/"),
    ("研究業績", "publications/"),
    ("研究設備", "facilities/"),
    ("最新情報", "news/"),
    ("問い合わせ・アクセス", "access/"),
]

# 右側のバナー欄
BANNERS = ["研究室訪問を歓迎します", "大型プロジェクトの紹介", "関連学会",
           "オープンアクセス論文", "高校生向けの公開講義",
           "◯◯大学", "大学院工学研究科", "マテリアル工学専攻"]

DEMO_NOTE = ("これは研究室サイトの構成デモです。文章・氏名・業績はすべて架空のサンプルで、"
             "実在の研究室の情報は含まれていません。")

# ---- デザイン切替バー（デモ用。本番サイトでは呼ばない） ----
SWITCH = [
    ("genkou", "現行デザイン（このサイト）", "{root}"),
    ("c", "案C 青・情報密度", "{root}styles/c/"),
    ("a", "案A 白・余白", "{root}styles/a/"),
    ("b", "案B ダーク", "{root}styles/b/"),
    ("index", "見比べ一覧", "{root}styles/"),
]


def switcher(root, current):
    links = "".join(
        '<a href="%s"%s>%s</a>' % (href.format(root=root),
                                   ' aria-current="true"' if key == current else "", label)
        for key, label, href in SWITCH)
    return '<div class="swbar"><b>DESIGN</b>%s</div>' % links


def read_csv(name):
    with io.open(os.path.join(HERE, "data", name), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def esc(s):
    return html.escape(s or "", quote=False)


def frag(name):
    with io.open(os.path.join(HERE, "pages", name), encoding="utf-8") as f:
        return f.read()


def head(title, root, desc):
    full = title + "｜" + SITE_NAME if title else SITE_NAME + "｜" + SITE_SUB
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="{root}assets/genkou.css">
</head>
<body>
<div class="demo">{esc(DEMO_NOTE)}</div>
{switcher(root, "genkou")}
<a class="skip" href="#main">本文へ</a>
"""


def header(root):
    return f"""<!-- [header] ロゴと検索 -->
<div class="gh"><div class="gh__in">
  <a class="gh__logo" href="{root}"><span class="gh__mark">SL</span>
    <span><b>{esc(SITE_NAME)}</b><span>{esc(SITE_SUB)}</span></span></a>
  <div class="gh__util">
    <input class="gh__search" type="search" placeholder="サイト内検索" aria-label="サイト内検索">
    <a class="gh__btn" href="#">English</a>
  </div>
</div></div>
"""


def leftnav(root, current):
    items = ""
    for label, href in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items += f'<a href="{root}{href}"{cur}>{esc(label)}</a>'
    return f'<!-- [nav] 左メニュー -->\n<nav class="gnav" aria-label="メインメニュー">{items}</nav>'


def sidebar():
    bans = "".join(f'<a class="gban" href="#">{esc(t)}</a>' for t in BANNERS)
    return ('<!-- [sidebar] 右のバナー欄 -->\n<div class="gside">' + bans
            + '<div class="gcount">あなたは<b>439,526</b>人目の訪問者です</div></div>')


def footer():
    return f"""<!-- [footer] フッタ -->
<footer class="gf"><div class="gf__in">
  <p>{esc(SITE_NAME)}　〒000-0000　◯◯県◯◯市◯◯1-1　◯◯棟◯階　TEL/FAX 00-0000-0000</p>
  <p>copyright © Sample Laboratory. All Rights Reserved.</p>
</div></footer>
</body>
</html>
"""


def news_rows(root, limit=None):
    rows = read_csv("news.csv")
    if limit:
        rows = rows[:limit]
    return "".join(
        f'<a href="{root}news/"><time>{esc(r["date"].replace("-", "."))}</time>'
        f'<em>{esc(r["category"])}</em>{esc(r["title"])}</a>' for r in rows)


def pub_rows(limit=None):
    rows = read_csv("publications.csv")
    if limit:
        rows = rows[:limit]
    out = []
    for r in rows:
        oa = '　<span class="oa">OPEN ACCESS</span>' if r.get("oa") == "yes" else ""
        out.append(f'<tr><th>{esc(r["year"])}</th><td><b>{esc(r["type"])}</b>　{esc(r["title"])}'
                   f'<br><span class="src">{esc(r["source"])}</span>{oa}</td></tr>')
    return "".join(out)


def member_rows(root, limit=None):
    rows = read_csv("members.csv")
    if limit:
        rows = rows[:limit]
    out = []
    for r in rows:
        if r.get("photo"):
            ph = f'<img src="{root}assets/img/{esc(r["photo"])}" alt="" width="260" height="347">'
        else:
            ph = '<span class="noimg">写真</span>'
        mail = esc(r["email"] + "(at)example.ac.jp") if r["email"] else "—"
        out.append(f'<tr><td class="mphoto">{ph}</td><th>{esc(r["name"])}</th>'
                   f'<td>{esc(r["role"])}</td><td>{esc(r["field"])}</td><td>{mail}</td></tr>')
    return "".join(out)


def page(path, title, desc, main_html, current, root=""):
    body = (head(title, root, desc) + header(root)
            + '<div class="gwrap">' + leftnav(root, current)
            + f'<main class="gmain" id="main">{main_html}</main>'
            + sidebar() + "</div>" + footer())
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with io.open(full, "w", encoding="utf-8") as f:
        f.write(body)
    print("  ", path)


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(OUT, "assets"))
    print("生成中:")
    r = "../"

    # ---------------- ホーム ----------------
    page("index.html", "", "研究室サイトの構成デモ。文章・氏名・業績はすべて架空のサンプルです。", f"""
<h1>{esc(SITE_NAME)}へようこそ。</h1>

<!-- [lead] 冒頭のあいさつ文 -->
<p>ここにリード文が入ります。研究室が何を目指し、どんな手法で取り組んでいるかを書く場所です。
このページは<b>CMSを一切使わず、HTMLファイルとCSSファイルだけ</b>で作られています。
見た目は現行サイトのままですが、更新の権限はすべて研究室側にあります。</p>

<div class="gfigs">
  <img src="assets/img/fig-grain.png" alt="" width="760" height="428">
  <img src="assets/img/fig-lattice.svg" alt="" width="760" height="428">
</div>

<!-- [news] 最新情報 -->
<h2>最新情報</h2>
<div class="gnews">{news_rows("", 6)}</div>
<p class="gmore"><a href="news/">一覧を見る ▶</a></p>

<!-- [research] 研究内容 -->
<h2>研究内容</h2>
<table class="gtbl">
  <tr><th>テーマ名 A</th><td>ここに一行の説明が入ります</td></tr>
  <tr><th>テーマ名 B</th><td>ここに一行の説明が入ります</td></tr>
  <tr><th>テーマ名 C</th><td>ここに一行の説明が入ります</td></tr>
</table>
<p class="gmore"><a href="research/">研究内容を見る ▶</a></p>

<!-- [publications] 研究業績 -->
<h2>最近の研究業績</h2>
<table class="gtbl">{pub_rows(4)}</table>
<p class="gmore"><a href="publications/">研究業績を見る ▶</a></p>
""", current="")

    # ---------------- 研究内容 ----------------
    page("research/index.html", "研究内容", "研究テーマの紹介ページ。内容はすべて架空のサンプルです。",
         "<h1>研究内容</h1>" + frag("research.html"), current="research/", root=r)

    # ---------------- メンバー ----------------
    page("members/index.html", "メンバー", "教員・研究員・スタッフの一覧。氏名はすべて架空のサンプルです。", f"""
<h1>メンバー</h1>
<p>ここにメンバー紹介の導入文が入ります。氏名・役職・専門分野は
<b>data/members.csv</b> から自動で表に組まれます。
迷惑メール対策のため、＠を(at)と表記しています。</p>
<div class="scroll"><table class="gtbl gtbl--mem">
  <thead><tr><th></th><th>氏名</th><th>役職</th><th>専門分野</th><th>メールアドレス</th></tr></thead>
  <tbody>{member_rows(r)}</tbody>
</table></div>
""", current="members/", root=r)

    # ---------------- 研究業績 ----------------
    page("publications/index.html", "研究業績", "論文・受賞の一覧。内容はすべて架空のサンプルです。", f"""
<h1>研究業績</h1>
<p>論文・受賞・学会発表・特許を1つのデータ（<b>data/publications.csv</b>）から生成しています。
1本追加するときはCSVに1行足すだけで、この一覧とトップページの両方に反映されます。</p>
<table class="gtbl">{pub_rows()}</table>
""", current="publications/", root=r)

    # ---------------- 研究設備 ----------------
    page("facilities/index.html", "研究設備", "保有する主要な実験設備の紹介。内容はすべて架空のサンプルです。",
         "<h1>研究設備</h1>" + frag("facilities.html"), current="facilities/", root=r)

    # ---------------- 最新情報 ----------------
    page("news/index.html", "最新情報", "お知らせの一覧。内容はすべて架空のサンプルです。", f"""
<h1>最新情報</h1>
<p>受賞・論文掲載・報道・行事などをお知らせします。
追加するときは <b>data/news.csv</b> に1行足すだけです。</p>
<div class="gnews">{news_rows(r)}</div>
""", current="news/", root=r)

    # ---------------- アクセス ----------------
    page("access/index.html", "問い合わせ・アクセス", "所在地・連絡先・アクセス方法。内容はすべて架空のサンプルです。",
         "<h1>問い合わせ・アクセス</h1>" + frag("access.html"), current="access/", root=r)

    # デザイン候補のページも続けて生成する
    import build_variants
    build_variants.build()

    n = sum(len(files) for _, _, files in os.walk(OUT))
    print(f"\n完了。docs/ に {n} ファイル生成しました。")
    print("確認: docs/index.html をブラウザで開く")


if __name__ == "__main__":
    build()
