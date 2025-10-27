import requests
from bs4 import BeautifulSoup
import json

url = "https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30"
resp = requests.get(url, timeout=10)
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "lxml")

# 找到所有書籍容器
book_items = soup.find_all("li", class_="item")

books = []
for li in book_items:#book_items 包含多個 <li> HTML 元素的清單，每個 <li> 代表一本書。
    # 書名
    title_tag = li.find("h4")#在 <li> 裡面找 <h4> 標籤
    title = title_tag.a.get_text(strip=True) if title_tag else "N/A"#再透過.a.get_text(strip=True) 取得 <a> 標籤內的文字

    # 價格
    price_tag = li.find("li", class_="price_a")#在 <li> 裡面找一個 <li class="price_a">
    b_tags = price_tag.find_all("b") if price_tag else []#find_all("b") 會抓出裡面所有 <b> 標籤。
    price = b_tags[1].get_text(strip=True) if len(b_tags) > 1 else "N/A"

    # 排名
    rank_tag = li.find("strong", class_="no"))#在 <li> 裡面找一個 <li class="strong">
    rank = rank_tag.get_text(strip=True) if rank_tag else "N/A"

    book = {
        "title": title,
        "price": f"NT${price}",
        "rank": rank
    }
    books.append(book)

# 美美地印出來

print(json.dumps(books, indent=2, ensure_ascii=False))
