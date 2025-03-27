import requests
sid = "9902"
res = requests.get(
    "http://norway.twsthr.info/StockHolders.aspx?stock=" + sid + "&fbclid=IwAR0Hq4oVDTnoj8d-jFlomkoLIPiGFM6HiioDDaWeb-KREDwhmXZiuRCtMdk")

# res = requests.get("你的目標網址")
with open("debug.html", "w", encoding='utf-8') as f:
    f.write(res.text)
