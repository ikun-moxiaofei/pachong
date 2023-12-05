from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re
import requests
from bs4 import BeautifulSoup
import json
from models import Colleges


# engine = create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口号/数据库?编码...", 其它参数)
# engine = create_engine("mysql+pymysql://root:123456@localhost:3306/collegesandmajors",echo=True)

def AddColleges(url, headers, i):
    engine = create_engine("mysql+pymysql://root:123456@localhost:3306/collegesandmajors", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    global colleges
    response = requests.get(url + str(i), headers=headers)
    if response.ok:
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        # 创建实例化对象
        colleges = Colleges()

        """
        获取**CollegeName**：学校名称，非空
        """
        CollegeName_div = soup.find("div", attrs={"class": "color-222 font-24 font-bold flex col-center"})
        # 有的大学已经下线了？？？例如https://daxue.163.com/web/university/detail/902
        if (CollegeName_div == None):
            return 0

        CollegeName = CollegeName_div.find("span")
        colleges.CollegeName = CollegeName.string

        if (session.query(Colleges).filter_by(CollegeName=colleges.CollegeName).first() is not None):
            return 0

        """
        **State**: 存储学校所省，非空
        **City**: 存储学校所在城市，非空
        **FoundedYear**: 存储学校成立的年份
        """
        div = soup.find("div", attrs={"class": "location_OhFXc"})
        all_span = div.findAll("span")
        # 有的学校没有创立时间
        if len(all_span) == 1:
            # 浙江·台州市
            str_ = all_span[0].string
            parts = str_.split("·")
            State = parts[0]
            City = parts[1]
            colleges.State = State
            colleges.City = City
        if len(all_span) == 2:
            # 浙江·台州市
            str_ = all_span[0].string
            parts = str_.split("·")
            State = parts[0]
            City = parts[1]
            colleges.State = State
            colleges.City = City
            # 提取年份
            FoundedYear = re.findall(r'\d+', all_span[1].string)
            colleges.FoundedYear = FoundedYear[0]

        """
        **SchoolBadge**：校徽（地址）
        """
        SchoolBadge_div = soup.find("div", attrs={"class": "flex-c-c logo_3oi3R"})
        SchoolBadge = SchoolBadge_div.find("img")
        colleges.SchoolBadge = SchoolBadge.get("src")

        """
        **Label**：学校标签（综合，985，双一流），多个
        """
        Label_div_s = soup.findAll("div", attrs={"class": "m-b-8 tags_AcZ9h"})
        Label_span_arr = {}
        index = 1
        for Label_div in Label_div_s:
            Label_span = Label_div.find("span")
            Label_span_arr[index] = Label_span.string
            index += 1

        Label = json.dumps(Label_span_arr, ensure_ascii=False)
        colleges.Label = Label

        """
        **Website**: 存储学校官网地址
        **ContactPhone**: 存储学校官方电话 ，多个
        **ContactEmail**: 存储学校电子邮箱
        """
        WCC_div_s = soup.findAll("div", attrs={"class": "contact_NVBwm"})
        for WCC_div in WCC_div_s:
            try:
                Website = WCC_div.find("a").get("href")
                colleges.Website = Website
            except:
                try:
                    phone_pattern = r'\d+-\d+'
                    matches = re.findall(phone_pattern, WCC_div.string)
                    if matches != []:
                        ContactPhone_arr = {}
                        index = 1
                        for match in matches:
                            ContactPhone_arr[index] = match
                            index += 1
                        ContactPhone = json.dumps(ContactPhone_arr, ensure_ascii=False)
                        colleges.ContactPhone = ContactPhone
                    else:
                        ContactEmail = re.search(r'\b\w+\@\w+\.\w+', WCC_div.string).group()
                        colleges.ContactEmail = ContactEmail
                except:
                    print(print("请求失败,url为" + url + str(i)))

        # WCC_div_s = soup.findAll("div", attrs={"class": "contact_NVBwm"})
        # # 学校官网: https://www.pku.edu.cn//
        # Website = WCC_div_s[0].find("a").get("href")
        # colleges.Website = Website
        # # 官方电话: 010-62751407,010-62554332
        # phone_pattern = r'\d+-\d+'
        # matches = re.findall(phone_pattern, WCC_div_s[1].string)
        # ContactPhone_arr = {}
        # index = 1
        # for match in matches:
        #     ContactPhone_arr[index] = match
        #     index += 1
        # ContactPhone = json.dumps(ContactPhone_arr, ensure_ascii=False)
        # colleges.ContactPhone = ContactPhone
        # # 电子邮箱: bdzsb@pku.edu.cn
        # ContactEmail = re.search(r'\b\w+\@\w+\.\w+', WCC_div_s[2].string).group()
        # colleges.ContactEmail = ContactEmail

        """
        **ScientificResearch**：科研实力（博士学位授权一级学科数等）
        (科研学位名称：开设个数)
        """
        ScientificResearch_div_s = soup.findAll("div", attrs={"class": "science-tab_-Y8go"})
        ScientificResearch_arr = {}
        for ScientificResearch_div in ScientificResearch_div_s:
            ScientificResearch_div_num = ScientificResearch_div.find("div", attrs={"class": "num_Tg+Y-"})
            ScientificResearch_div_num_i = ScientificResearch_div_num.find("i")
            ScientificResearch_div_name = ScientificResearch_div.find("div", attrs={"class": "desc_LBlX8"})
            ScientificResearch_arr[ScientificResearch_div_name.string] = ScientificResearch_div_num_i.string
        ScientificResearch = json.dumps(ScientificResearch_arr, ensure_ascii=False)
        colleges.ScientificResearch = ScientificResearch

        """
        **ResearchInstitutes**：研究机构 ，多个
        (实验室名称：实验室介绍)
        """
        ResearchInstitutes_div_s = soup.findAll("div", attrs={"class": "m-t-10"})
        ResearchInstitutes_arr = {}
        for ResearchInstitutes_div in ResearchInstitutes_div_s:
            ResearchInstitutes_div_name_span = ResearchInstitutes_div.find("div", attrs={
                "class": "tags_AcZ9h tag-color_BjjHA"})
            ResearchInstitutes_div_name = ResearchInstitutes_div_name_span.find("span")
            ResearchInstitutes_div_span_s = ResearchInstitutes_div.findAll("span")
            ResearchInstitutes_div_span_arr = ""
            for ResearchInstitutes_div_span in ResearchInstitutes_div_span_s:
                if ResearchInstitutes_div_span.string == ResearchInstitutes_div_name.string: continue
                if ResearchInstitutes_div_span.string is None:
                    ResearchInstitutes_div_span_text = ResearchInstitutes_div_span.text
                    ResearchInstitutes_div_span_string_string = ResearchInstitutes_div_span_text.replace('\n',
                                                                                                         '').replace(
                        ' ', '')
                else:
                    ResearchInstitutes_div_span_string = ResearchInstitutes_div_span.string
                    ResearchInstitutes_div_span_string_string = ResearchInstitutes_div_span_string.replace('\n',
                                                                                                           '').replace(
                        ' ', '')
                ResearchInstitutes_div_span_arr += ResearchInstitutes_div_span_string_string
            ResearchInstitutes_arr[ResearchInstitutes_div_name.string] = ResearchInstitutes_div_span_arr
        ResearchInstitutes = json.dumps(ResearchInstitutes_arr, ensure_ascii=False)
        colleges.ResearchInstitutes = ResearchInstitutes

        """
        **Faculty**：师资力量
        """
        Faculty_div = soup.find("div", attrs={"class": "content_TYLq3"})
        if Faculty_div is not None:
            Faculty = Faculty_div.find("span").string
            colleges.Faculty = Faculty

        """
        **Introduction**：学校简介
        """
        Introduction_div = soup.find("div", attrs={"class": "show_uDsiS line-9"})
        if Introduction_div is not None:
            Introduction = Introduction_div.text
            colleges.Introduction = Introduction

        colleges.text()

        session.add(colleges)
        session.commit()

    else:
        with open('wrong_colleges.txt', 'a') as file:
            file.write(url + str(i) + "学校基本信息错误")
            file.write('\n')
        return 0

    return 1
