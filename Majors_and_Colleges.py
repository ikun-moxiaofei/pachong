from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from models import MajorsCategory, TagMajors, Majors, Colleges, CollegesMajors


# engine = create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口号/数据库?编码...", 其它参数)
# engine = create_engine("mysql+pymysql://root:123456@localhost:3306/collegesandmajors",echo=True)

def AddMajorsAndColleges(url, headers, i):
    engine = create_engine("mysql+pymysql://root:123456@localhost:3306/collegesandmajors", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    response = requests.get(url + str(i), headers=headers)
    if response.ok:
        content = response.text
        soup = BeautifulSoup(content, "html.parser")


        CollegeName_div = soup.find("div", attrs={"class": "color-222 font-24 font-bold flex col-center"})
        College_Name = CollegeName_div.find("span")
        CollegeName = College_Name.string
        college = session.query(Colleges).filter_by(CollegeName=CollegeName).first()
        # print(CollegeName)
        # print(college.ID)
        CollegeID = college.ID


        # 创建实例化对象
        # Majors = Majors()
        """
        **院校专业表（CollegesMajors）**
        - **ID**：主键
        - **CollegesID**：对应学校主键，非空
        - **MajorsID**：对应专业主键，非空
        - **MajorsCategoryID**：对应专业类别主键，多个
        - **TagMajorsID**：对应特色专业标签主键，多个
        """
        # 国家级特色专业
        TagMajorsID = ''
        MajorsID = ''
        MajorsCategoryID = ''
        TagMajorsName_div_s = soup.findAll("div", attrs={"class": "tags_AcZ9h tag-color_ptDUz"})
        if TagMajorsName_div_s is not None:
            if len(TagMajorsName_div_s) == 2:
                TagMajorsName_div_span = TagMajorsName_div_s[0].find("span")
                TagMajorsName = TagMajorsName_div_span.string
                TagMajorsID = session.query(TagMajors).filter_by(TagMajorsName=TagMajorsName).first().ID
                # print(TagMajorsID)


                Majors_div_s_1 = soup.find("div", attrs={"class": "m-b-20"})
                Majors_span_s_1 = Majors_div_s_1.findAll("span")
                if Majors_span_s_1 is not None:
                    for Majors_span_1 in Majors_span_s_1:
                        Majors_span_1 = Majors_span_1.text.replace('\n','').replace(' ', '').replace('、', '')
                        print(Majors_span_1)
                        majors = Majors()
                        majors.MajorName = Majors_span_1
                        if session.query(Majors).filter_by(MajorName=majors.MajorName).first() is None:
                            session.add(majors)
                            session.commit()

                        # majors.text()
                        MajorsID = session.query(Majors).filter_by(MajorName=majors.MajorName).first().ID
                        collegesMajors = CollegesMajors()
                        collegesMajors.MajorsID = MajorsID
                        collegesMajors.CollegesID = CollegeID
                        collegesMajors.TagMajorsID = TagMajorsID

                        session.add(collegesMajors)
                        session.commit()



                TagMajorsName_div_span = TagMajorsName_div_s[1].find("span")
                TagMajorsName = TagMajorsName_div_span.string
                TagMajorsID = session.query(TagMajors).filter_by(TagMajorsName=TagMajorsName).first().ID
                # print(TagMajorsID)

                Majors_div_s_1 = soup.find("div", attrs={"class": "m-b-32"})
                Majors_span_s_1 = Majors_div_s_1.findAll("span")
                if Majors_span_s_1 is not None:
                    for Majors_span_1 in Majors_span_s_1:
                        Majors_span_1 = Majors_span_1.text.replace('\n', '').replace(' ', '').replace('、', '')
                        print(Majors_span_1)
                        majors = Majors()
                        majors.MajorName = Majors_span_1
                        if session.query(Majors).filter_by(MajorName=majors.MajorName).first() is None:
                            session.add(majors)
                            session.commit()

                        # majors.text()
                        MajorsID = session.query(Majors).filter_by(MajorName=majors.MajorName).first().ID
                        collegesMajors = CollegesMajors()
                        collegesMajors.MajorsID = MajorsID
                        collegesMajors.CollegesID = CollegeID
                        collegesMajors.TagMajorsID = TagMajorsID

                        session.add(collegesMajors)
                        session.commit()

            elif len(TagMajorsName_div_s) == 1:
                TagMajorsName_div_span = TagMajorsName_div_s[0].find("span")
                TagMajorsName = TagMajorsName_div_span.string
                TagMajorsID = session.query(TagMajors).filter_by(TagMajorsName=TagMajorsName).first().ID

                Majors_div_s_1 = soup.find("div", attrs={"class": "m-b-20"})
                if Majors_div_s_1 is None:
                    Majors_div_s_1 = soup.find("div", attrs={"class": "m-b-32"})
                Majors_span_s_1 = Majors_div_s_1.findAll("span")
                if Majors_span_s_1 is not None:
                    for Majors_span_1 in Majors_span_s_1:
                        Majors_span_1 = Majors_span_1.text.replace('\n', '').replace(' ', '').replace('、', '')
                        print(Majors_span_1)
                        majors = Majors()
                        majors.MajorName = Majors_span_1
                        if session.query(Majors).filter_by(MajorName=majors.MajorName).first() is None:
                            session.add(majors)
                            session.commit()

                        # majors.text()
                        MajorsID = session.query(Majors).filter_by(MajorName=majors.MajorName).first().ID
                        collegesMajors = CollegesMajors()
                        collegesMajors.MajorsID = MajorsID
                        collegesMajors.CollegesID = CollegeID
                        collegesMajors.TagMajorsID = TagMajorsID

                        session.add(collegesMajors)
                        session.commit()


        li_div_s = soup.find("div", attrs={"class": "major-table_vLrLP"})
        if li_div_s is not None:
            li_s = li_div_s.findAll("li")
            if li_s is not None:
                for li in li_s:
                    MajorsCategoryName = li.find("div", attrs={"class": "name_hhFBi"})
                    MajorsName = li.find("div", attrs={"class": "list_tVfW2"})
                    if MajorsCategoryName.string == '类别':
                        continue
                    MajorsCategoryID = session.query(MajorsCategory).filter_by(MajorsCategoryName=MajorsCategoryName.string).first().ID
                    MajorsName_a_s = MajorsName.findAll("a")
                    for MajorsName_a in MajorsName_a_s:
                        # print(MajorsName_a.string)
                        MajorsName_ = MajorsName_a.text.replace('\n', '').replace(' ', '').replace('、', '')
                        print(MajorsName_)
                        majors = Majors()
                        majors.MajorName = MajorsName_
                        if session.query(Majors).filter_by(MajorName=majors.MajorName).first() is None:
                            session.add(majors)
                            session.commit()
                        MajorsID = session.query(Majors).filter_by(MajorName=majors.MajorName).first().ID
                        collegesMajors = CollegesMajors()
                        collegesMajors.MajorsID = MajorsID
                        collegesMajors.CollegesID = CollegeID
                        collegesMajors.MajorsCategoryID = MajorsCategoryID

                        session.add(collegesMajors)
                        session.commit()

    else:
        with open('wrong_majors_colleges.txt', 'a') as file:
            file.write(url + str(i) + "院校专业对应信息错误")
            file.write('\n')
        return 0

    return 1
