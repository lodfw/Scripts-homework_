import requests
import re
import json

# 發送 GET 請求並取得 HTML 原始碼（字串）
response = requests.get("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")

# 檢查請求是否成功
try:
    response.raise_for_status()  # 若狀態碼非 200，則拋出異常
    print("Request 成功")
except requests.exceptions.HTTPError as err:
    print(f"請求失敗: {err}")
    exit(1)

html = response.text  # 取得 HTML 原始碼（字串）

# 正規表示式樣板
pattern = r"£\d+\.\d{2}"  # £ + 數字 + . + 兩位小數

# 使用 re.findall() 找出符合價格格式的字串
prices = re.findall(pattern, html)

print(f"共找到 {len(prices)} 個價格：")
for p in prices:
    print(p)

# 將結果存成 JSON 檔案
data = {"prices": prices}

with open("prices.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("已將結果存成 prices.json")

