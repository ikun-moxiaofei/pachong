import time
from Colleges_and_sql import AddColleges

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 "
                  "Safari/537.36 Edg/119.0.0.0"
}
url = "https://daxue.163.com/web/university/detail/"

for i in range(1, 20):

    AddColleges(url, headers, i)


    time.sleep(2)
