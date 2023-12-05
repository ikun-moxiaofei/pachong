import time
from Colleges_and_sql import AddColleges
from Majors_and_Colleges import AddMajorsAndColleges
from Majors_and_sql import AddMajors

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 "
                  "Safari/537.36 Edg/119.0.0.0"
}
url = "https://daxue.163.com/web/university/detail/"

for i in range(1, 10):

    # AddColleges返回0表示爬取大学基本出现错误，可以是因为重复或者大学不存在，即直接跳过本次循环
    flag = AddColleges(url, headers, i)
    if flag == 0:
        continue

    AddMajors(url, headers, i)

    AddMajorsAndColleges(url, headers, i)


    time.sleep(2)
