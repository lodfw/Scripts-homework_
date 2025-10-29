import requests
from bs4 import BeautifulSoup
import json

url = "https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30"
headers = {  # 自訂標頭
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}
# 找到所有書籍容器
try:
    response = requests.get(url, headers=headers, timeout=10)  # 使用自訂標頭
    response.raise_for_status()  # 如果請求失敗 (狀態碼不是 2xx)，則拋出例外
    soup = BeautifulSoup(response.text, "lxml")
    book_items = soup.select("div.mod_a li.item")
    if not book_items:
        print("警告：找不到任何書籍項目。可能是網頁結構已變更。")


    book_items = book_items[:20]  # 只取前 20 筆資料
    
    


    books = []
    for li in book_items:#book_items 包含多個 <li> HTML 元素的清單，每個 <li> 代表一本書。
        # 書名
        title_tag = li.find("h4")#在 <li> 裡面找 <h4> 標籤
        title = title_tag.a.get_text(strip=True)#再透過.a.get_text(strip=True) 取得 <a> 標籤內的文字
        # 價格
        price_tag = li.find("li", class_="price_a")#在 <li> 裡面找一個 <li class="price_a">
        b_tags = price_tag.find_all("b") if price_tag else []#find_all("b") 會抓出裡面所有 <b> 標籤。
        price = b_tags[1].get_text(strip=True)
        # 排名
        rank_tag = li.find("strong", class_="no")#在 <li> 裡面找一個 <li class="strong">
        rank = rank_tag.get_text(strip=True)

        book = {
            "title": title,
            "price": f"NT${price}",
            "rank": rank
        }
        books.append(book)
    # 輸出為 JSON 格式
    # 將結果存成 JSON 檔案

        with open("book&rank.json", "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        print(json.dumps(books, ensure_ascii=False, indent=4))
    # 處理網路請求或 HTTP 錯誤
except requests.exceptions.RequestException as e:
    print(f"錯誤：無法取得網頁內容。 {e}")
# 處理 HTML 解析或標籤尋找過程中的錯誤
except (AttributeError, IndexError) as e:
    print(f"錯誤：解析網頁內容時發生錯誤。可能是網頁結構已變更。 {e}")

