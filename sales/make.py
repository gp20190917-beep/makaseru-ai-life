# -*- coding: utf-8 -*-
"""架空のオンラインショップ売上サンプルを生成 → 分析 → 図を作る（すべてサンプルデータ）"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import json, io, os

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONTB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
fm.fontManager.addfont(FONT); fm.fontManager.addfont(FONTB)
plt.rcParams["font.family"] = "Noto Sans CJK JP"
plt.rcParams["axes.unicode_minus"] = False

INK="#1A1D23"; SUB="#5B6172"; IND="#4C4AE4"; INDD="#34329E"; SPARK="#F5A623"; LINE="#E4E5EA"; PAPER="#F7F7F4"

rng = np.random.default_rng(20260927)

# 商品（価格・季節の形）= すべて架空
PROD = {
 "冷感タオル":        (1980, [0,0,0,0,1,4,7,6,2,0,0,0]),
 "折りたたみ日傘":    (2980, [0,0,1,4,6,5,2,1,1,0,0,0]),
 "ステンレスタンブラー":(2480, [1,1,2,3,4,5,5,4,3,2,2,1]),
 "ハンドクリーム":    (1200, [5,4,3,2,1,0,0,0,1,3,5,6]),
 "あったかブランケット":(4200, [6,5,3,1,0,0,0,0,0,2,5,7]),
 "母の日ギフトセット": (4800, [0,0,1,7,9,2,0,0,0,0,0,0]),
 "お歳暮セット":      (3900, [0,0,0,0,0,0,0,0,0,2,6,9]),
 "収納ボックス":      (1600, [5,4,4,3,2,2,2,2,3,3,4,4]),
}
REEL_START = "2025-06"   # Instagram リールを始めた月（＝本人の実データの前提に合わせた仮定）

rows=[]
for name,(price,shape) in PROD.items():
    for y in (2024,2025,2026):
        for m in range(1,13):
            if y==2026 and m>9: continue
            base = 26 if name in ("ステンレスタンブラー","収納ボックス") else 14
            u = base*shape[m-1]*(1+rng.normal(0,.16))
            u = max(0, u)
            # 2025年ぶんの年成長（+6%）
            if y==2025: u*=1.06
            if y==2026: u*=1.12
            # リール開始後（2025-06以降）の底上げ。商品で効き方が違う、という仮定
            if (y,m) >= (2025,6):
                boost = {"冷感タオル":1.34,"折りたたみ日傘":1.22,"ハンドクリーム":1.18,
                         "収納ボックス":1.15,"ステンレスタンブラー":1.10,
                         "あったかブランケット":1.05,"母の日ギフトセット":1.04,"お歳暮セット":1.02}[name]
                u*=boost
            rows.append({"日付":f"{y}-{m:02d}-01","年":y,"月":m,"商品名":name,
                         "単価":price,"販売個数":int(round(u)),"売上":int(round(u))*price})
df=pd.DataFrame(rows); df.to_csv("sales/sales_sample.csv",index=False,encoding="utf-8-sig")

# ---- 分析 ----
full = df.groupby("年")["売上"].sum()
same = df[df["月"]<=9].groupby("年")["売上"].sum()          # 1〜9月の同期比較
monthly = df.pivot_table(index="月",columns="年",values="売上",aggfunc="sum")
byprod_year = df.pivot_table(index="商品名",columns="年",values="売上",aggfunc="sum")
prod_month = df.pivot_table(index="商品名",columns="月",values="売上",aggfunc="sum")
# 商品ごとの「一番売れる月」「一番売れない月」
top_bottom={n:(int(prod_month.loc[n].idxmax()),int(prod_month.loc[n].idxmin())) for n in prod_month.index}
# リール開始の前後（2025-01〜05 と 2025-06〜2026-09 の月平均、同一商品構成）
before = df[(df["年"]==2025)&(df["月"]<=5)]["売上"].sum()/5
after  = df[((df["年"]==2025)&(df["月"]>=6))|(df["年"]==2026)]["売上"].sum()/16
# 季節の偏り（商品別に、上位3か月で年間の何%を占めるか）
conc={}
for n in prod_month.index:
    s=prod_month.loc[n].sort_values(ascending=False)
    conc[n]=round(float(s.head(3).sum()/s.sum()*100),1)

res={"full_year":{int(k):int(v) for k,v in full.items()},
     "same_period_1_9":{int(k):int(v) for k,v in same.items()},
     "monthly":{int(c):{int(i):int(v) for i,v in monthly[c].dropna().items()} for c in monthly.columns},
     "by_prod_year":{n:{int(c):int(v) for c,v in byprod_year.loc[n].items()} for n in byprod_year.index},
     "top_month":{n:top_bottom[n][0] for n in top_bottom},
     "bottom_month":{n:top_bottom[n][1] for n in top_bottom},
     "top3_share_pct":conc,
     "reel_before_monthly_avg":int(before),"reel_after_monthly_avg":int(after),
     "reel_ratio":round(after/before,2),
     "total":int(df["売上"].sum()),"units":int(df["販売個数"].sum())}
io.open("sales/result.json","w",encoding="utf-8").write(json.dumps(res,ensure_ascii=False,indent=1))

# ---- 図 ----
def style(ax):
    ax.set_facecolor(PAPER)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_color(LINE)
    ax.tick_params(colors=SUB,labelsize=10); ax.grid(axis="y",color=LINE,lw=.8)

# 図1 月別推移（3年）
fig,ax=plt.subplots(figsize=(9.6,4.6),dpi=160)
fig.patch.set_facecolor(PAPER); style(ax)
x=np.arange(1,13)
for y,c,ls in ((2024,"#9AA0B4","--"),(2025,IND,"-"),(2026,SPARK,"-")):
    v=[monthly.loc[m,y]/10000 if y in monthly.columns and not np.isnan(monthly.loc[m,y]) else np.nan for m in x]
    ax.plot(x,v,ls,color=c,lw=2.4 if y!=2024 else 1.8,marker="o",ms=4,label=f"{y}年")
ax.axvline(6,color=INDD,lw=1.2,alpha=.4,ls=":")
ax.text(6.15,ax.get_ylim()[1]*.94,"2025年6月\nリール開始",fontsize=9,color=INDD,va="top")
ax.set_xticks(x); ax.set_xticklabels([f"{m}月" for m in x])
ax.set_ylabel("売上（万円）",color=SUB,fontsize=10)
ax.set_title("月別の売上推移（2024〜2026年）",fontsize=14,color=INK,fontweight="bold",pad=14,loc="left")
ax.legend(frameon=False,fontsize=10,labelcolor=SUB)
fig.tight_layout(); fig.savefig("sales/fig1_monthly.png",facecolor=PAPER); plt.close(fig)

# 図2 年次（1〜9月の同期比較）
fig,ax=plt.subplots(figsize=(6.6,4.2),dpi=160)
fig.patch.set_facecolor(PAPER); style(ax)
ys=[2024,2025,2026]; vs=[same[y]/10000 for y in ys]
b=ax.bar([str(y) for y in ys],vs,color=["#9AA0B4",IND,SPARK],width=.58)
for r,v in zip(b,vs): ax.text(r.get_x()+r.get_width()/2,v+max(vs)*.02,f"{v:.0f}万円",ha="center",fontsize=11,color=INK,fontweight="bold")
ax.set_ylim(0,max(vs)*1.18); ax.set_ylabel("売上（万円）",color=SUB,fontsize=10)
ax.set_title("同じ1〜9月で比べる（途中の年は比較しない）",fontsize=13,color=INK,fontweight="bold",pad=14,loc="left")
fig.tight_layout(); fig.savefig("sales/fig2_year.png",facecolor=PAPER); plt.close(fig)

# 図3 商品×月 ヒートマップ（各商品の年間=100とした構成比）
fig,ax=plt.subplots(figsize=(9.8,5.0),dpi=160)
fig.patch.set_facecolor(PAPER)
share=prod_month.div(prod_month.sum(axis=1),axis=0)*100
im=ax.imshow(share.values,cmap="YlGnBu",aspect="auto")
ax.set_xticks(range(12)); ax.set_xticklabels([f"{m}" for m in range(1,13)],color=SUB,fontsize=10)
ax.set_yticks(range(len(share))); ax.set_yticklabels(share.index,color=INK,fontsize=10)
for i in range(share.shape[0]):
    for j in range(12):
        v=share.values[i,j]
        if v>=4: ax.text(j,i,f"{v:.0f}",ha="center",va="center",fontsize=8.5,color="#0B2E4F" if v<14 else "#fff")
ax.set_xlabel("月",color=SUB,fontsize=10)
ax.set_title("商品ごとに「売れる月」が違う（各商品の3年合計を100とした割合 %）",fontsize=13,color=INK,fontweight="bold",pad=14,loc="left")
fig.tight_layout(); fig.savefig("sales/fig3_season.png",facecolor=PAPER); plt.close(fig)

# 図4 リール開始の前後
fig,ax=plt.subplots(figsize=(6.6,4.2),dpi=160)
fig.patch.set_facecolor(PAPER); style(ax)
vals=[before/10000,after/10000]
b=ax.bar(["開始前\n(2025年1〜5月)","開始後\n(2025年6月〜2026年9月)"],vals,color=["#9AA0B4",IND],width=.5)
for r,v in zip(b,vals): ax.text(r.get_x()+r.get_width()/2,v+max(vals)*.02,f"{v:.0f}万円",ha="center",fontsize=11,color=INK,fontweight="bold")
ax.set_ylim(0,max(vals)*1.18); ax.set_ylabel("1か月あたりの売上（万円）",color=SUB,fontsize=10)
ax.set_title("リールを始めた前後で、月あたりの売上はどう変わったか",fontsize=13,color=INK,fontweight="bold",pad=14,loc="left")
fig.tight_layout(); fig.savefig("sales/fig4_reel.png",facecolor=PAPER); plt.close(fig)

print("OK total=%d units=%d" % (res["total"],res["units"]))
print("same1-9:", res["same_period_1_9"])
print("reel before/after:", res["reel_before_monthly_avg"], res["reel_after_monthly_avg"], res["reel_ratio"])
print("top3 share:", res["top3_share_pct"])
