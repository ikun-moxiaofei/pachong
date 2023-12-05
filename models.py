from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, JSON, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Colleges(Base):
    __tablename__ = 'colleges'
    ID = Column(Integer, primary_key=True)
    CollegeName = Column(String(255), nullable=False)
    FoundedYear = Column(Integer)
    Label = Column(JSON)
    SchoolBadge = Column(String(255))
    State = Column(String(255), nullable=False)
    City = Column(String(255), nullable=False)
    Website = Column(Text)
    ContactPhone = Column(JSON)
    ContactEmail = Column(Text)
    ScientificResearch = Column(JSON)
    ResearchInstitutes = Column(JSON)
    Faculty = Column(Text)
    Introduction = Column(Text)

    def text(self):
        print(self.CollegeName)
        print(self.State)
        print(self.City)
        print(self.FoundedYear)
        print(self.SchoolBadge)
        print(self.Label)
        print(self.Website)
        print(self.ContactPhone)
        print(self.ContactEmail)
        print(self.ScientificResearch)
        print(self.ResearchInstitutes)
        print(self.Faculty)
        print(self.Introduction)

class MajorsCategory(Base):
    __tablename__ = 'majors_category'
    ID = Column(Integer, primary_key=True)
    MajorsCategoryName = Column(String(255), nullable=False, unique=True)

    def text(self):
        print(self.MajorsCategoryName)

class TagMajors(Base):
    __tablename__ = 'tag_majors'
    ID = Column(Integer, primary_key=True)
    TagMajorsName = Column(String(255), nullable=False, unique=True)

    def text(self):
        print(self.TagMajorsName)

class Majors(Base):
    __tablename__ = 'majors'
    ID = Column(Integer, primary_key=True)
    MajorName = Column(String(255), nullable=False, unique=True)

    def text(self):
        print(self.MajorName)

class CollegesMajors(Base):
    __tablename__ = 'colleges_majors'
    ID = Column(Integer, primary_key=True)
    CollegesID = Column(Integer, ForeignKey('colleges.ID'), nullable=False)
    MajorsID = Column(Integer, ForeignKey('majors.ID'), nullable=False)
    MajorsCategoryID = Column(Integer, ForeignKey('majors_category.ID'))
    TagMajorsID = Column(Integer, ForeignKey('tag_majors.ID'))



engine = create_engine("mysql+pymysql://root:123456@localhost:3306/collegesandmajors",echo=True)
Base.metadata.create_all(engine)


# def text(self):
#     print(self.CollegeName)
#     print(self.State)
#     print(self.City)
#     print(self.FoundedYear)
#     print(self.SchoolBadge)
#     print(self.Label)
#     print(self.Website)
#     print(self.ContactPhone)
#     print(self.ContactEmail)
#     print(self.ScientificResearch)
#     print(self.ResearchInstitutes)
#     print(self.Faculty)
#     print(self.Introduction)