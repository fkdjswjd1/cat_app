from daylist.dayinfo import Daylist
from daylist.daylist_db import DaylistDao
from member.service import MemberService
import streamlit as st
import pandas as pd


# Cat_Num이 없다고 가정
class DaylistService:
    loginId = ''

    def __init__(self):
        self.dao = DaylistDao()
        self.service = MemberService()

    def addDaylist(self, Cat_Num, Date, Weight, Breakfast_Food, Lunch_Food,Dinner_Food, Breakfast_Water, Lunch_Water,Dinner_Water, Playtime, Check1, Check2, Check3,Check4,Check5, Check6,Check7, Check8, Check9, Check10,memo):
        a = Daylist(Cat_Num=Cat_Num, Date=Date, Weight=Weight, Breakfast_Food=Breakfast_Food, Lunch_Food=Lunch_Food, Dinner_Food=Dinner_Food, Breakfast_Water=Breakfast_Water, Lunch_Water=Lunch_Water, Dinner_Water=Dinner_Water, Playtime=Playtime, Check1=Check1, Check2=Check2,  Check3=Check3,Check4=Check4,Check5=Check5,Check6=Check6,Check7=Check7,Check8=Check8,Check9=Check9,Check10=Check10,memo=memo)
        self.dao.insert(a)

    def printDaylistInfo(self, Cat_Num, Date):
        a=self.dao.select(Cat_Num,Date)
        if a:
            return[a.Date, a.Weight, a.Breakfast_Food, a.Lunch_Food,a.Dinner_Food, a.Breakfast_Water, a.Lunch_Water, a.Dinner_Water, a.Playtime, a.Check1, a.Check2, a.Check3,a.Check4,a.Check5, a.Check6,a.Check7, a.Check8, a.Check9, a.Check10,a.memo]
        else:
            return

    def modifyDaylist(self,Cat_Num, Date, Weight, Breakfast_Food, Lunch_Food,Dinner_Food, Breakfast_Water, Lunch_Water,Dinner_Water, Playtime, Check1, Check2, Check3,Check4,Check5, Check6,Check7, Check8, Check9, Check10,memo):
        self.dao.update(Daylist(Cat_Num=Cat_Num, Date=Date, Weight=Weight, Breakfast_Food=Breakfast_Food, Lunch_Food=Lunch_Food,
                 Dinner_Food=Dinner_Food, Breakfast_Water=Breakfast_Water, Lunch_Water=Lunch_Water,
                 Dinner_Water=Dinner_Water, Playtime=Playtime, Check1=Check1, Check2=Check2, Check3=Check3,Check4=Check4,
                 Check5=Check5, Check6=Check6,Check7=Check7, Check8=Check8, Check9=Check9,Check10=Check10, memo=memo))

    def makedf(self,startday,Cat_Num):
        rows,columns=self.dao.selectbydate(startday,Cat_Num)
        if rows:
            df = pd.DataFrame.from_records(data=rows, columns=columns)
            return df
        else:
            return
