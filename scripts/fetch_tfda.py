scripts/fetch_tfda.pyimport json,re,urllib.request
URL="https://data.fda.gov.tw/data/opendata/export/52/json"
def pick(x,*ks):
 for k in ks:
  if x.get(k) not in (None,""): return x[k]
 return ""
def region(s):
 s=s or ""
 if re.search(r"基隆|台北|新北|桃園|新竹|宜蘭",s): return "北部"
 if re.search(r"苗栗|台中|彰化|南投|雲林",s): return "中部"
 if re.search(r"嘉義|台南|高雄|屏東",s): return "南部"
 if re.search(r"花蓮|台東",s): return "東部"
 if re.search(r"澎湖|金門|連江",s): return "離島"
 return "未判定"
def typ(s):
 for n,p in [("農藥殘留",r"農藥|pesticide"),("動物用藥",r"動物用藥|抗生素|獸藥"),("微生物",r"腸桿菌|大腸桿菌|沙門氏菌|李斯特菌|菌落|微生物"),("食品添加物",r"防腐劑|甜味劑|色素|添加物|二氧化硫"),("重金屬",r"鉛|鎘|汞|砷|重金屬"),("真菌毒素",r"黃麴毒素|赭麴毒素|真菌毒素"),("容器／包裝",r"容器|器具|溶出"),("標示",r"標示|標籤|營養標示")]:
  if re.search(p,s,re.I): return n
 return "其他"
def batch(s):
 m=re.search(r"(?:LOT|Lot|批號|Batch)\s*[:：#]?\s*([A-Za-z0-9._/-]+)",s)
 return m.group(1) if m else "—"
with urllib.request.urlopen(URL,timeout=60) as r: raw=json.load(r)
if isinstance(raw,dict):
 for k in ("result","data","records","rows"):
  if isinstance(raw.get(k),list): raw=raw[k];break
out=[]
for x in raw:
 a=pick(x,"進口商地址"); d=pick(x,"不合格原因暨檢出量詳細說明","原因","主旨"); s=pick(x,"主旨","產品名稱")
 out.append({"發布日期":str(pick(x,"發布日期","報驗受理日期"))[:10],"地區":region(a),"主旨":s,"進口商名稱":pick(x,"進口商名稱"),"進口商地址":a,"產地":pick(x,"產地"),"不合格類型":typ(s+" "+d),"可能批號":batch(s+" "+d),"原因":d,"貨品分類號列":pick(x,"貨品分類號列"),"檢驗方法":pick(x,"檢驗方法"),"法規限量標準":pick(x,"法規限量標準"),"製造廠或出口商名稱":pick(x,"製造廠或出口商名稱"),"製造商代碼":pick(x,"製造商代碼"),"牌名":pick(x,"牌名"),"重量":pick(x,"重量"),"處置情形":pick(x,"處置情形"),"附圖":pick(x,"附圖")})
out.sort(key=lambda x:x["發布日期"],reverse=True)
open("data.json","w",encoding="utf-8").write(json.dumps(out,ensure_ascii=False,separators=(",",":")))
print("records:",len(out))
