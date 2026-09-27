# -*- coding: utf-8 -*-
slides = [
("cover", "50代に効く", "Gensparkの使い方", "7つ", "むずかしい用語は使っていません", None, None),
("1", "メールの返事を", "下書きしてもらえる", None, "かたい文面も、やわらかく直してくれます。",
 "そのまま送る前に、自分の言葉に直すだけ。", "01"),
("2", "テーマを言うだけで", "資料一式ができる", None, "パワーポイント形式でも保存できます。",
 "完成品を見ながら「ここだけ直して」と頼めます。", "02"),
("3", "会議に自動で参加して", "議事録ができる", None, "Zoom・Teams・Google Meet に対応。",
 "録音の長さに制限がなく、終われば議事録が残ります。", "03"),
("4", "出典つきで", "調べてくれる", None, "「どこから持ってきた情報か」まで付けてくれます。",
 "最後に1〜2件、自分の目で開くのがコツです。", "04"),
("5", "チラシ・ポスターの", "1枚が作れる", None, "言葉だけで、SNS用の1枚ができます。",
 "作った画像は、商売にも使えます。", "05"),
("6", "「あれ、どこだっけ」を", "探し出してくれる", None, "メール・カレンダー・チャットを1つにまとめて記憶。",
 "毎回おなじ説明をしなくて済みます。", "06"),
("7", "毎朝のニュースを", "自動でまとめてくれる", None, "寝ている間も、決めた仕事を進めておいてくれます。",
 "詳しくはサイトで ▶ @makaseru.ai50", "07"),
]

TPL = '''<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@500;700;900&family=Noto+Sans+JP:wght@400;500;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{background:#F7F7F4;color:#1A1D23;font-family:"Noto Sans JP",sans-serif;
 position:relative;display:flex;flex-direction:column;padding:96px 88px}}
.bar{{position:absolute;left:0;top:0;width:100%;height:14px;background:#4C4AE4}}
.bar2{{position:absolute;left:0;top:14px;width:280px;height:14px;background:#F5A623}}
.no{{font-family:"Space Grotesk",sans-serif;font-size:34px;font-weight:700;letter-spacing:.2em;color:#4C4AE4}}
h1{{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;font-size:104px;line-height:1.24;letter-spacing:.01em;margin-top:28px}}
h1 .hl{{color:#4C4AE4;background:linear-gradient(transparent 64%,rgba(245,166,35,.5) 64%)}}
.sub{{margin-top:44px;font-size:40px;line-height:1.62;color:#5B6172;font-weight:500}}
.note{{margin-top:auto;font-size:32px;line-height:1.6;color:#5B6172;border-left:5px solid #F5A623;padding-left:26px}}
.foot{{margin-top:40px;display:flex;align-items:center;justify-content:space-between;
 font-size:26px;color:#5B6172;font-weight:700}}
.brand{{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;font-size:30px;color:#1A1D23;display:flex;align-items:center;gap:14px}}
.dot{{width:20px;height:20px;border-radius:50%;background:#F5A623}}
.un{{font-family:"Space Grotesk",sans-serif;font-size:20px;font-weight:700;letter-spacing:.1em;background:#1A1D23;color:#fff;border-radius:8px;padding:4px 12px}}
/* cover */
.cover h1{{font-size:126px;margin-top:36px}}
.cover .big{{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;font-size:230px;line-height:1;color:#4C4AE4;margin-top:14px}}
.cover .tag{{display:inline-block;font-size:30px;font-weight:700;background:#EEF0FF;color:#34329E;
 border-radius:999px;padding:12px 30px;margin-top:44px}}
</style></head><body class="{cls}">
<div class="bar"></div><div class="bar2"></div>
{body}
<div class="foot">
  <div class="brand"><span class="dot"></span>まかせるAI生活<span class="un">非公認</span></div>
  <div>@makaseru.ai50</div>
</div>
</body></html>'''

out = []
for s in slides:
    if s[0] == "cover":
        cls, t1, t2, t3, lead = "cover", s[1], s[2], s[3], s[4]
        body = ('<p class="no">What Genspark can do</p>'
                f'<h1>{t1}<br>{t2}</h1>'
                f'<p class="big">{t3}</p>'
                f'<span class="tag">{lead}</span>')
        fname = "slide-1.html"
    else:
        cls, t1, t2, lead, note, num = "item", s[1], s[2], s[4], s[5], s[6]
        body = (f'<p class="no">{num}</p>'
                f'<h1>{t1}<br><span class="hl">{t2}</span></h1>'
                f'<p class="sub">{lead}</p>')
        body += f'<p class="note">{note}</p>'
        fname = f"slide-{int(num)+1}.html"
    open(fname, "w", encoding="utf-8").write(TPL.format(cls=cls, body=body))
    out.append(fname)
print("\n".join(out))
