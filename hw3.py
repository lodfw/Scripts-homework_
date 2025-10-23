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
for li in book_items:
    # 書名
    title_tag = li.find("h4")
    title = title_tag.a.get_text(strip=True) if title_tag else "N/A"

    # 價格
    price_tag = li.find("li", class_="price_a")
    b_tags = price_tag.find_all("b") if price_tag else []
    price = b_tags[1].get_text(strip=True) if len(b_tags) > 1 else "N/A"

    # 排名
    rank_tag = li.find("strong", class_="no")
    rank = rank_tag.get_text(strip=True) if rank_tag else "N/A"

    book = {
        "title": title,
        "price": f"NT${price}",
        "rank": rank
    }
    books.append(book)

# 美美地印出來
print(json.dumps(books, indent=2, ensure_ascii=False))