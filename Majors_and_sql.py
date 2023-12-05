from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
import json
from models import MajorsCategory, TagMajors, Majors


# engine = create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口号/数据库?编码...", 其它参数)
# engine = create_engine("mysql+pymysql://root:123456@localhost:3306/collegesandmajors",echo=True)

def AddMajors(url, headers, i):
    engine = create_engine("mysql+pymysql://root:123456@localhost:3306/collegesandmajors", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    response = requests.get(url + str(i), headers=headers)
    if response.ok:
        content = response.text
        soup = BeautifulSoup(content, "html.parser")

        # 创建实例化对象
        # MajorsCategory = MajorsCategory()
        # TagMajors = TagMajors()
        # Majors = Majors()
        """
        **特色专业标签（TagMajors）**
        - **ID**：主键，唯一标识每个特色专业标签
        - **TagMajorsName**：特色专业名称  （国家级特色专业，国家重点学科等），非空，不相同
        """
        TagMajorsName_div_s = soup.findAll("div", attrs={"class": "tags_AcZ9h tag-color_ptDUz"})
        if TagMajorsName_div_s is not None:
            for TagMajorsName_div in TagMajorsName_div_s:
                TagMajorsName_div_span = TagMajorsName_div.find("span")
                print(TagMajorsName_div_span.string)
                tagMajors = TagMajors()
                tagMajors.TagMajorsName = TagMajorsName_div_span.string

                if session.query(TagMajors).filter_by(TagMajorsName=tagMajors.TagMajorsName).first() is None:
                    session.add(tagMajors)
                    session.commit()

                tagMajors.text()

            # print(TagMajorsName_div)
        """
        **专业类别表（MajorsCategory）**
        - **ID**：主键，唯一标识每个专业类别
        - **MajorsCategoryName**：专业类别的名称 （ 经济学类(本科) ），非空，不相同
        """
        MajorsCategory_div_s = soup.findAll("div", attrs={"class": "name_hhFBi"})
        if MajorsCategory_div_s is not None:
            for MajorsCategory_div in MajorsCategory_div_s:
                if MajorsCategory_div.string=="类别":
                    continue
                majorsCategory = MajorsCategory()
                majorsCategory.MajorsCategoryName = MajorsCategory_div.string
                print(majorsCategory.MajorsCategoryName)
                if session.query(MajorsCategory).filter_by(MajorsCategoryName=majorsCategory.MajorsCategoryName).first() is None:
                    session.add(majorsCategory)
                    session.commit()

                majorsCategory.text()

    else:
        with open('wrong_majors.txt', 'a') as file:
            file.write(url + str(i) + "专业类型信息错误")
            file.write('\n')
        return 0

    return 1
