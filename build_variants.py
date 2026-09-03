# -*- coding: utf-8 -*-
"""
デザイン候補のページを作る（見せるだけの参考用）。

  themes/c.css … 案C 青・情報密度
  themes/a.css … 案A 白・余白・端正
  themes/b.css … 案B ダーク・写真主導

サイト本体（現行デザインの再現）は build.py が docs/ に作る。
出力: docs/styles/index.html と docs/styles/{c,a,b}/index.html
中身は data/ のダミーデータを使う。実在の研究室の情報は入れない。
"""
import csv, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "docs", "styles")
NAME = "サンプル研究室"
SUB = "◯◯大学大学院工学研究科　マテリアル工学専攻"
NOTE = ("これは研究室サイトの構成デモです。文章・氏名・業績はすべて架空のサンプルで、"
        "実在の研究室の情報は含まれていません。")

VARIANTS = {
    "c": ("案C｜青・情報密度",
          "現行の青（#003399）を引き継ぎ、2カラムの情報量が多い構成を今風に組み直したもの。"
          "右の「ピックアップ」欄は現行サイトのバナー列にあたります。"),
    "a": ("案A｜白・余白・端正",
          "白地に細い罫線と大きな余白。装飾を使わず、文字組みと余白で品を出す方向。"),
    "b": ("案B｜ダーク・写真主導",
          "ほぼモノクロで組み、色は写真だけが持つ。大きな見出しで迫力を出す方向。"),
}
SWATCH = {
    "c": ["#003399", "#3584BB", "#EAF1FF", "#F6F8FB", "#1A2130"],
    "a": ["#F5F6F8", "#FFFFFF", "#0B3A6F", "#7E6224", "#0E1620"],
    "b": ["#0E1114", "#161A1F", "#EEF0F3", "#8FB3D9", "#98A2AD"],
}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wght@600;700&family=IBM+Plex+Mono:wght@400;500'
         '&family=M+PLUS+2:wght@400;500;600;700&family=Murecho:wght@500;600;700'
         '&family=Noto+Sans+JP:wght@400;500;700'
         '&family=Zen+Kaku+Gothic+New:wght@500;700;900&display=swap">')

SW_CSS = """
.demo{background:#8A5A12;color:#fff;font-size:12px;text-align:center;padding:7px 16px;line-height:1.6;
  font-family:"Noto Sans JP",system-ui,sans-serif}
.swbar{background:#12181F;color:#C9D2DE;font-size:12px;line-height:1.6;
  font-family:"Noto Sans JP",system-ui,sans-serif;
  padding:8px 16px;display:flex;gap:8px;align-items:center;justify-content:center;flex-wrap:wrap}
.swbar b{font-weight:600;color:#8A98AA;font-size:11px;letter-spacing:.08em;margin-right:4px}
.swbar a{color:#C9D2DE;text-decoration:none;border:1px solid #2C3745;border-radius:2px;
  padding:5px 12px;transition:background .15s,border-color .15s,color .15s}
.swbar a:hover{background:#1D2733;border-color:#4A5A6E;color:#fff}
.swbar a[aria-current="true"]{background:#fff;border-color:#fff;color:#12181F;font-weight:700}
"""

SWITCH = [
    ("genkou", "現行デザイン", "{root}"),
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


def data(name):
    with io.open(os.path.join(HERE, "data", name), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def shell(title, css, body, current, root):
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{title}｜{NAME}</title>
{FONTS}
<style>
{css}
{SW_CSS}
</style>
</head>
<body>
<div class="demo">{NOTE}</div>
{switcher(root, current)}
{body}
</body>
</html>
"""


# ---------------------------------------------------------------- 案C
def build_c():
    ni = "".join(
        f'<a class="mC__ni" href="#"><time>{n["date"].replace("-", ".")}</time>'
        f'<span class="mC__nt" data-k="{n["category"]}">{n["category"]}</span>'
        f'<p>{n["title"]}</p></a>' for n in data("news.csv")[:7])
    mem = "".join(
        f'<figure><img src="../../assets/img/{m["photo"] or "person-1.svg"}" alt="" width="260" height="347">'
        f'<figcaption><b>{m["name"]}</b><span>{m["role"]}<br>{m["field"]}</span></figcaption></figure>'
        for m in data("members.csv")[:5])
    pubs = "".join(
        f'<div class="mC__pub" data-t="{"paper" if p["type"] == "論文" else "award"}">'
        f'<time>{p["year"]}</time><p>{p["title"]}<em><b>{p["source"]}</b></em></p>'
        + ('<span class="mC__badge">OPEN ACCESS</span>' if p["oa"] == "yes" else "<span></span>")
        + "</div>" for p in data("publications.csv")[:5])
    figs = ["fig-grain.png", "fig-lattice.svg", "fig-layers.svg"]
    cards = "".join(f"""
        <a class="mC__card" href="#">
          <div class="mC__cardFig"><img src="../../assets/img/{f}" alt="" width="760" height="428"></div>
          <div class="mC__cardBody"><span class="mono">Theme 0{i+1}</span>
            <h3>研究テーマの見出し</h3>
            <p>ここにテーマの説明が2〜3行入ります。図版は本番で実際の写真に差し替えます。</p></div>
        </a>""" for i, f in enumerate(figs))
    return f"""
<main class="mC">
  <div class="mC__top"><div class="mC__topIn">
    <a href="#">サイトマップ</a><a href="#">問い合わせ</a><a href="#">ENGLISH</a>
  </div></div>

  <div class="mC__hd"><div class="mC__hdIn">
    <a class="mC__logo" href="#"><span class="mC__mark" aria-hidden="true">SL</span>
      <span><b>{NAME}</b><em>{SUB}</em></span></a>
    <nav class="mC__nav"><a href="#">研究内容</a><a href="#">メンバー</a><a href="#">研究業績</a>
      <a href="#">研究設備</a><a href="#">最新情報</a><a href="#">アクセス</a>
      <a href="#" class="cta">研究室訪問</a></nav>
  </div></div>

  <div class="mC__hero"><div class="mC__heroIn">
    <div>
      <span class="mono">Anisotropic Materials Science</span>
      <h1><span><mark>異方性</mark>の材料科学で、</span><span>材料の性能を引き出す。</span></h1>
      <p>ここにリード文が入ります。研究室が何を目指し、どんな手法で取り組んでいるかを3行程度で書く場所です。</p>
      <div class="mC__ctas"><a class="mC__btn" href="#">研究内容を見る</a>
        <a class="mC__btnG" href="#">研究業績を探す</a></div>
    </div>
    <figure class="mC__heroFig" style="margin:0">
      <img src="../../assets/img/fig-grain.png" alt="" width="760" height="428">
      <figcaption>図版のプレースホルダ｜本番ではここに実際の写真や図が入ります。</figcaption>
    </figure>
  </div></div>

  <div class="mC__band"><div class="mC__bandIn">
    <div class="mC__stat"><b>1,234<small>件</small></b><span>ここに実績の数字が入ります</span></div>
    <div class="mC__stat"><b>12<small>賞</small></b><span>受賞歴の件数など</span></div>
    <div class="mC__stat"><b>34<small>名</small></b><span>教員・研究員・事務スタッフ</span></div>
    <div class="mC__stat"><b>2007<small>年度〜</small></b><span>卒業生アーカイブを継続公開</span></div>
  </div></div>

  <div class="mC__main">
    <div class="mC__col">
      <section>
        <h2 class="mC__h2"><b>研究内容</b><a href="#">研究内容の一覧 →</a></h2>
        <div class="mC__cards">{cards}
        </div>
      </section>

      <section>
        <h2 class="mC__h2"><b>最新情報</b><a href="#">すべての最新情報 →</a></h2>
        <div class="mC__news">{ni}</div>
      </section>

      <section>
        <h2 class="mC__h2"><b>研究業績</b><a href="#">論文・受賞の一覧 →</a></h2>
        <div class="mC__pubBox">
          <div class="mC__filters"><span class="mono">絞り込み</span>
            <button class="mC__chip" data-f="all" aria-pressed="true">すべて</button>
            <button class="mC__chip" data-f="paper" aria-pressed="false">論文</button>
            <button class="mC__chip" data-f="award" aria-pressed="false">受賞</button>
          </div>
          <div id="mC-list">{pubs}</div>
          <div class="mC__pubFoot"><span id="mC-count">5件を表示中</span>
            <a class="mC__btnG" href="#">研究業績の全リストへ</a></div>
        </div>
      </section>

      <section>
        <h2 class="mC__h2"><b>メンバー</b><a href="#">全メンバー →</a></h2>
        <div class="mC__mem">{mem}</div>
      </section>
    </div>

    <aside class="mC__rail">
      <div class="mC__visit"><b>研究室訪問を歓迎します</b>
        <p>配属を考えている学生の方、共同研究をお考えの企業・研究機関の方。訪問希望日を明記のうえご連絡ください。</p>
        <a href="#">見学を申し込む</a></div>
      <div class="mC__box"><div class="mC__boxHd">ピックアップ</div>
        <ul class="mC__pins">
          <li><a href="#"><span class="mono">Project</span>大型プロジェクトの紹介</a></li>
          <li><a href="#"><span class="mono">Society</span>関連学会へのリンク</a></li>
          <li><a href="#"><span class="mono">Open Access</span>オープンアクセス論文の一覧</a></li>
          <li><a href="#"><span class="mono">For High School</span>高校生向けの公開講義</a></li>
        </ul></div>
      <div class="mC__box"><div class="mC__boxHd">関連リンク</div>
        <ul class="mC__pins">
          <li><a href="#">◯◯大学</a></li><li><a href="#">大学院工学研究科</a></li>
          <li><a href="#">マテリアル工学専攻</a></li><li><a href="#">科研費データベース</a></li>
        </ul></div>
    </aside>
  </div>

  <footer class="mC__ft">
    <div class="mC__ftIn">
      <div><h4>Laboratory</h4><p>{NAME}<br>{SUB}</p></div>
      <div><h4>Contact</h4><p>〒000-0000　◯◯県◯◯市◯◯1-1<br>◯◯棟◯階　◯◯◯号室<br>TEL / FAX　00-0000-0000</p></div>
      <div><h4>Access</h4><p>◯◯線 ◯◯駅から徒歩約15分<br>◯◯モノレール ◯◯駅から徒歩約15分</p></div>
      <div><h4>Links</h4><ul><li><a href="#">◯◯大学</a></li><li><a href="#">大学院工学研究科</a></li>
        <li><a href="#">マテリアル工学専攻</a></li></ul></div>
    </div>
    <div class="mC__copy">© Sample Laboratory　—　構成デモ</div>
  </footer>
</main>
<script>
(function(){{
  var chips=[].slice.call(document.querySelectorAll('.mC__chip'));
  var rows=[].slice.call(document.querySelectorAll('#mC-list .mC__pub'));
  var count=document.getElementById('mC-count');
  chips.forEach(function(c){{
    c.addEventListener('click',function(){{
      var f=c.getAttribute('data-f'),n=0;
      chips.forEach(function(x){{x.setAttribute('aria-pressed',x===c?'true':'false');}});
      rows.forEach(function(r){{
        var on=(f==='all')||(r.getAttribute('data-t')===f);
        r.hidden=!on; if(on)n++;
      }});
      if(count)count.textContent=n+'件を表示中';
    }});
  }});
}})();
</script>
"""


# ---------------------------------------------------------------- 案A
def build_a():
    ni = "".join(
        f'<div class="mA__ni"><time>{n["date"].replace("-", ".")}</time>'
        f'<span class="mA__cat">{n["category"]}</span><a href="#">{n["title"]}</a></div>'
        for n in data("news.csv")[:6])
    mem = "".join(
        f'<figure><img src="../../assets/img/{m["photo"] or "person-1.svg"}" alt="" width="260" height="347">'
        f'<figcaption><b>{m["name"]}</b><span>{m["role"]}<br>{m["field"]}</span></figcaption></figure>'
        for m in data("members.csv")[:5])
    pubs = "".join(
        f'<div class="mA__pub"><time>{p["year"]}</time><p>{p["title"]}<i>{p["source"]}</i></p>'
        + ('<span class="mA__oa">OPEN ACCESS</span>' if p["oa"] == "yes" else "<span></span>")
        + "</div>" for p in data("publications.csv")[:4])
    return f"""
<main class="mA">
  <div class="mA__hd"><div class="mA__hdIn">
    <div class="mA__logo"><b>{NAME}</b><span>{SUB}</span></div>
    <nav class="mA__nav"><a href="#">研究内容</a><a href="#">メンバー</a><a href="#">研究業績</a>
      <a href="#">研究設備</a><a href="#">問い合わせ</a><a href="#" class="en">English</a></nav>
  </div></div>

  <div class="mA__hero"><div class="mA__heroIn">
    <div class="mA__heroTx">
      <p class="mA__kicker"><i></i><span class="lbl">Sample Laboratory</span></p>
      <h1>ここに研究室の<br><em>キャッチコピー</em>が入る。</h1>
      <p>リード文が2〜3行入ります。研究室が何を目指し、どんな手法で取り組んでいるかを簡潔に書く場所です。</p>
      <div class="mA__cta"><a class="mA__btn mA__btn--fill" href="#">研究内容を見る</a>
        <a class="mA__btn" href="#">研究室訪問について</a></div>
    </div>
    <figure class="mA__heroFig" style="margin:0"><img src="../../assets/img/fig-grain.png" alt="" width="760" height="428"></figure>
  </div></div>

  <section class="mA__sec">
    <div class="mA__rail"><div class="mA__railIn"><span class="mA__railJa">研究内容</span><span class="mA__railEn">Research</span></div></div>
    <div class="mA__body">
      <h2 class="mA__h2">3つの柱</h2>
      <p class="mA__sub">ここに研究の概要が入ります。見出しの下に2〜3行、全体像がつかめる文章を置きます。</p>
      <div class="mA__pillars">
        <div class="mA__pil"><span class="lbl">Theme 01</span><h3>研究テーマの見出し</h3><p>ここにテーマの説明が3〜5行入ります。</p></div>
        <div class="mA__pil"><span class="lbl">Theme 02</span><h3>研究テーマの見出し</h3><p>ここにテーマの説明が3〜5行入ります。</p></div>
        <div class="mA__pil"><span class="lbl">Theme 03</span><h3>研究テーマの見出し</h3><p>ここにテーマの説明が3〜5行入ります。</p></div>
      </div>
    </div>
  </section>

  <section class="mA__sec">
    <div class="mA__rail"><div class="mA__railIn"><span class="mA__railJa">研究業績</span><span class="mA__railEn">Publications</span></div></div>
    <div class="mA__body">
      <h2 class="mA__h2">研究業績</h2>
      <p class="mA__sub">論文・受賞・学会発表を1つのデータから生成しています。</p>
      <div class="mA__stats">
        <div class="mA__stat"><b>1,234<sub>件</sub></b><span>ここに実績の数字が入ります</span></div>
        <div class="mA__stat"><b>12<sub>賞</sub></b><span>受賞歴の件数など</span></div>
        <div class="mA__stat"><b>34<sub>名</sub></b><span>教員・研究員・事務スタッフ</span></div>
        <div class="mA__stat"><b>2007<sub>年度〜</sub></b><span>卒業生アーカイブを継続公開</span></div>
      </div>
      <div class="mA__pubs">{pubs}</div>
    </div>
  </section>

  <section class="mA__sec">
    <div class="mA__rail"><div class="mA__railIn"><span class="mA__railJa">最新情報</span><span class="mA__railEn">News</span></div></div>
    <div class="mA__body">
      <h2 class="mA__h2">最新情報</h2>
      <p class="mA__sub">受賞・論文掲載・報道・行事などをお知らせします。</p>
      <div class="mA__news">{ni}</div>
    </div>
  </section>

  <section class="mA__sec">
    <div class="mA__rail"><div class="mA__railIn"><span class="mA__railJa">メンバー</span><span class="mA__railEn">Members</span></div></div>
    <div class="mA__body">
      <h2 class="mA__h2">メンバー</h2>
      <p class="mA__sub">教員・研究員・事務スタッフと、博士・修士・学部の学生が在籍しています。</p>
      <div class="mA__mem">{mem}</div>
    </div>
  </section>

  <footer class="mA__ft">
    <div class="mA__ftIn">
      <div><h4>{NAME}</h4><p>{SUB}</p></div>
      <div><h4>連絡先</h4><p>〒000-0000　◯◯県◯◯市◯◯1-1<br>◯◯棟◯階　◯◯◯号室<br>TEL / FAX　00-0000-0000</p></div>
      <div><h4>アクセス</h4><p>◯◯線 ◯◯駅から徒歩約15分<br>◯◯モノレール ◯◯駅から徒歩約15分</p></div>
      <div><h4>関連リンク</h4><ul><li><a href="#">◯◯大学</a></li><li><a href="#">大学院工学研究科</a></li><li><a href="#">マテリアル工学専攻</a></li></ul></div>
    </div>
    <div class="mA__copy">© Sample Laboratory</div>
  </footer>
</main>
"""


# ---------------------------------------------------------------- 案B
def build_b():
    ni = "".join(
        f'<a class="mB__ni" href="#"><time>{n["date"].replace("-", ".")}</time>'
        f'<span class="mB__tag">{n["category"]}</span><p>{n["title"]}</p></a>'
        for n in data("news.csv")[:6])
    mem = "".join(
        f'<figure><img src="../../assets/img/{m["photo"] or "person-1.svg"}" alt="" width="260" height="347">'
        f'<figcaption><b>{m["name"]}</b><span>{m["role"]}<br>{m["field"]}</span></figcaption></figure>'
        for m in data("members.csv")[:5])
    figs = ["fig-layers.svg", "fig-grain.png", "fig-lattice.svg"]
    rows = "".join(f"""
    <div class="mB__row">
      <div class="mB__rowTx"><span class="arc">Theme 0{i+1}</span>
        <h3>研究テーマの見出し</h3>
        <p>ここにテーマの説明が3〜5行入ります。図版は本番で実際の写真に差し替えます。</p>
        <a class="mB__more" href="#">詳しく見る</a></div>
      <div class="mB__rowFig"><img src="../../assets/img/{f}" alt="" width="760" height="428"></div>
    </div>""" for i, f in enumerate(figs))
    return f"""
<main class="mB">
  <section class="mB__hero">
    <img class="mB__heroImg" src="../../assets/img/fig-layers.svg" alt="">
    <div class="mB__heroVeil"></div>
    <div class="mB__hd"><div class="mB__hdIn">
      <div class="mB__logo"><b>{NAME}</b><i>Sample Lab</i></div>
      <nav class="mB__nav"><a href="#">研究内容</a><a href="#">メンバー</a><a href="#">研究業績</a>
        <a href="#">研究設備</a><a href="#">問い合わせ</a><a href="#" class="en">EN</a></nav>
    </div></div>
    <div class="mB__heroIn">
      <p class="mB__eyebrow">Sample Laboratory</p>
      <h1><span>ここに研究室の</span><br><span>キャッチコピーが入る。</span></h1>
      <p>{SUB}。リード文が2〜3行入ります。研究室が何を目指しているかを簡潔に書く場所です。</p>
      <div class="mB__ctas"><a class="mB__btn" href="#">研究内容を見る</a>
        <a class="mB__btn2" href="#">研究室訪問について</a></div>
    </div>
  </section>

  <div class="mB__band"><div class="mB__bandIn">
    <div class="mB__stat"><b>1,234<small>件</small></b><span>ここに実績の数字が入ります</span></div>
    <div class="mB__stat"><b>12<small>賞</small></b><span>受賞歴の件数など</span></div>
    <div class="mB__stat"><b>34<small>名</small></b><span>教員・研究員・事務スタッフ</span></div>
    <div class="mB__stat"><b>2007<small>年度〜</small></b><span>卒業生アーカイブを継続公開</span></div>
  </div></div>

  <section class="mB__sec"><div class="mB__wrap">
    <div class="mB__secHd"><h2>3つの柱</h2><span class="arc">Research</span></div>
    {rows}
  </div></section>

  <section class="mB__sec mB__newsSec"><div class="mB__wrap">
    <div class="mB__secHd"><h2>最新情報</h2><span class="arc">News — 一覧を見る</span></div>
    {ni}
  </div></section>

  <section class="mB__sec"><div class="mB__wrap">
    <div class="mB__secHd"><h2>メンバー</h2><span class="arc">Members</span></div>
    <div class="mB__mem">{mem}</div>
  </div></section>

  <footer class="mB__ft">
    <div class="mB__ftIn">
      <div><h4>Laboratory</h4><p>{NAME}<br>{SUB}</p></div>
      <div><h4>Contact</h4><p>〒000-0000　◯◯県◯◯市◯◯1-1<br>◯◯棟◯階　◯◯◯号室<br>TEL / FAX　00-0000-0000</p></div>
      <div><h4>Access</h4><p>◯◯線 ◯◯駅から徒歩約15分<br>◯◯モノレール ◯◯駅から徒歩約15分</p></div>
      <div><h4>Links</h4><ul><li><a href="#">◯◯大学</a></li><li><a href="#">大学院工学研究科</a></li>
        <li><a href="#">マテリアル工学専攻</a></li></ul></div>
    </div>
    <div class="mB__copy">© Sample Laboratory</div>
  </footer>
</main>
"""


BUILDERS = {"c": build_c, "a": build_a, "b": build_b}

INDEX_CSS = """
:root{--ink:#16202E;--mute:#5B6678;--line:#DCE2EC;--bg:#F6F8FB;--brand:#003399;--paper:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Noto Sans JP",system-ui,sans-serif;font-size:16px;line-height:1.85}
img{display:block;max-width:100%}
.wrap{max-width:1000px;margin:0 auto;padding:52px 26px 80px}
h1{font-family:"Murecho","Noto Sans JP",sans-serif;font-size:clamp(24px,3.4vw,34px);
  font-weight:700;margin:0 0 14px;line-height:1.45}
.lead{color:var(--mute);font-size:15px;max-width:62ch;margin:0 0 12px}
.note{color:var(--mute);font-size:13.5px;max-width:66ch;margin:0 0 36px}
.grid{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.item{background:var(--paper);border:1px solid var(--line);border-radius:3px;
  padding:22px;display:flex;flex-direction:column;gap:11px}
.item h2{font-size:18px;font-weight:700;margin:0;line-height:1.5}
.item p{font-size:13.5px;line-height:1.85;color:var(--mute);margin:0;flex:1}
.item a{align-self:flex-start;text-decoration:none;font-size:13.5px;font-weight:700;
  padding:10px 20px;border-radius:2px;background:var(--brand);color:#fff}
.item a:hover{background:#00246B}
.sw{display:flex;height:24px;border:1px solid var(--line);border-radius:2px;overflow:hidden}
.sw i{flex:1}
"""


def build():
    os.makedirs(OUT, exist_ok=True)
    for key, fn in BUILDERS.items():
        css = io.open(os.path.join(HERE, "themes", key + ".css"), encoding="utf-8").read()
        d = os.path.join(OUT, key)
        os.makedirs(d, exist_ok=True)
        with io.open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(shell(VARIANTS[key][0], css, fn(), key, "../../"))
        print("   styles/%s/index.html" % key)

    items = "".join("""
    <article class="item">
      <h2>%s</h2>
      <div class="sw" aria-hidden="true">%s</div>
      <p>%s</p>
      <a href="%s/">開く</a>
    </article>""" % (VARIANTS[k][0],
                     "".join('<i style="background:%s"></i>' % c for c in SWATCH[k]),
                     VARIANTS[k][1], k) for k in ["c", "a", "b"])
    html = f"""<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>デザイン候補｜{NAME}</title>
{FONTS}<style>{INDEX_CSS}{SW_CSS}</style></head>
<body>
<div class="demo">{NOTE}</div>
{switcher("../", "index")}
<div class="wrap">
  <h1>デザイン候補</h1>
  <p class="lead">同じ中身のまま、見た目だけを差し替えた3案です。中身（文章・写真・業績データ）は
  <b>data/</b> と <b>pages/</b> に1か所でまとめてあるので、どれを選んでも作り直しにはなりません。</p>
  <p class="note">サイト本体（現行デザインの再現）は上の「現行デザイン」から。
  いずれもCMSを使わない素のHTMLとCSSだけで動いていて、サーバー費用は0円です。</p>
  <div class="grid">{items}</div>
</div>
</body></html>
"""
    with io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("   styles/index.html")


if __name__ == "__main__":
    build()
