import requests
from bs4 import BeautifulSoup
import json

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
resp = requests.get(url, timeout=10)
resp.raise_for_status()
resp.encoding = "utf-8"  # 手動指定正確編碼
soup = BeautifulSoup(resp.text, "lxml")

# 找到所有書籍容器
bookname_articles = soup.find_all("article", class_="product_pod")

# 擷取每本書的 title 屬性
books = []
for article in bookname_articles:
    a_tag = article.h3.a #取得 <h3> 裡的 <a> 標籤
    title = a_tag.get("title", "").strip()#從 <a> 標籤裡取出 title 屬性 #strip() 去除前後空白
 

    price_tag = article.find("p", class_="price_color")#使用 BeautifulSoup 的 find 方法，在 article 這個 HTML 區塊中，尋找第一個 <p> 標籤，且它的 class 屬性包含 ""price_color"。
    price = price_tag.get_text().strip()
   

    rating_tag = article.find("p", class_="star-rating")#使用 BeautifulSoup 的 find 方法，在 article 這個 HTML 區塊中，尋找第一個 <p> 標籤，且它的 class 屬性包含 "star-rating"。
    rating_classes = rating_tag.get("class", [])  # 取得 class 屬性（是個 list）
    # 移除 "star-rating"，留下星等
    rating = next((c for c in rating_classes if c != "star-rating"), "No rating")#從 rating_classes 裡面，找出第一個 不是 "star-rating" 的 class，並把它存到 rating。["star-rating", "Three"]
    book = {
        "title": title,
        "price": price,
        "rating": rating
    }
    books.append(book)
    # 將結果存成 JSON 檔案
    data = {"book": books}
    
        # 第三步：將列表轉換成 JSON 格式，並輸出到檔案中
    try:
        with open("book&star.json", "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        print("\n成功將結果儲存至 book&star.json 檔案。")
    except (IOError, OSError) as e:
        print(f"\n錯誤：無法將結果寫入檔案。 {e}")
    
    # 列印結果
    print(json.dumps(books, ensure_ascii=False, indent=4))

# 處理網路請求或 HTTP 錯誤
except requests.exceptions.RequestException as e:
    print(f"錯誤：無法取得網頁內容。 {e}")
# 處理 HTML 解析或標籤尋找過程中的錯誤
except (AttributeError, IndexError) as e:
    print(f"錯誤：解析網頁內容時發生錯誤。可能是網頁結構已變更。 {e}")



