# -*- coding: big5 -*-

#中華民國政府行政機關辦公日曆表 https://data.gov.tw/dataset/14718

# 產生日曆字典，一次載入2年
FOLDER_NAME = "calendar"
YEAR_RANGE = 4
import datetime
import csv
import os

# 當前.py檔案的路徑
current_path = os.path.dirname(os.path.abspath(__file__))
# 新資料夾的路徑
FOLDER_PATH = os.path.join(current_path, FOLDER_NAME)
# 如果資料夾不存在，則創建它
if not os.path.exists(FOLDER_PATH): os.makedirs(FOLDER_PATH)
    
#取得民國年的日曆
def getCalendar(year, FOLDER_PATH = FOLDER_PATH):
    def checkCSV(filename):
        with open(filename, "r") as f:    
            if len(f.read().split("\n")) > 20: return True        
            f.close()
        return False

    import requests
    from bs4 import BeautifulSoup
    from os import remove
    # 設定搜尋條件
    search_text = year
    search_class = "download-item"

    # 發送 GET 請求並解析 HTML
    url = "https://data.gov.tw/dataset/14718"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到所有符合條件的 div 元素
    divs = soup.find_all("div", {"class": search_class, "text": search_text})
    divs = soup.find_all("div", {"class": search_class, })
    print(f"找到 {len(divs)} 個符合條件的元素")

    # 遍歷所有符合條件的 div 元素，查找 href 屬性
    for div in divs:
        if search_text not in div.text or "Google" in div.text: continue
        a = div.find("a")
        if a is not None and "href" in a.attrs:
            href = a["href"]
            print(f"找到 href: {href}")
            filename = "{:}{:}.csv".format(FOLDER_PATH, search_text)
            response = requests.get(href)
            with open(filename, "wb") as f:
                f.write(response.content)
            if checkCSV(filename): 
                print("順利下載 {:} 成功".format(filename))
                return True
            else: 
                remove(filename)
                print("下載 {:} 失敗".format(filename))
        else:
            print("未找到 href 屬性")
    return False


thisYear = datetime.date.today().year - 1911 #民國年轉換
taiwanHoliday = {}
for i in range(YEAR_RANGE):
    filename = "{:}{:}.csv".format(FOLDER_PATH, thisYear-i)
    if not os.path.exists(filename): getCalendar(str(thisYear-i))
    with open(filename, "r") as f:    
        # 西元日期	星期	是否放假(0 上班, 2放假)	備註
        #content = f.read().split("\n")
        content = csv.reader(f)        
        #for each in content[1:]:
        for each in content:
            #print(each)
            taiwanHoliday[each[0]] = True if each[2] == "0" else False
        f.close()


def isTaiwanWorkday(date):
    # YYYYmmdd格式，支援datetime與str兩種方式
    dateStr = ""
    if type(date) == datetime.datetime:
        dateStr = date.strftime("%Y%m%d")
    elif type(date) == str:
        dateStr = date
    else:
        print("請輸入正確日期，類別(datetime)或是(str)")
        return None
    return taiwanHoliday[dateStr]
