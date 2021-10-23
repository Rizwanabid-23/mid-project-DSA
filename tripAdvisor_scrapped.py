from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow,QApplication,QComboBox,QHBoxLayout

class hotel:
    def __init__(self,name,price,reviews,rating,city,services,ranking):
        self.name=name
        self.price=price
        self.reviews=reviews
        self.rating=rating
        self.city=city
        self.services=services
        self.ranking=ranking

driver = webdriver.Chrome(executable_path='C:\\Users\\rizwa\\Downloads\\chromedriver_win32\\chromedriver.exe')
driver.get("https://www.tripadvisor.com/Hotels")
content = driver.page_source
soup = BeautifulSoup(content)
categories = []
categories_2 = []
categories_3 = []
array_list=[]
i = soup.find('div',attrs={'class':'ppr_rup ppr_priv_popular_hotels'})    
j = i.find('ul',attrs={'class':'flexCols'})
for k in j.findAll('li',attrs={'class':'item'}):
    get_category = k.find('a',attrs={'class':'ui_link'})
    if (get_category):
        get_href = get_category.get('href').replace("/Hotels-","")
        get_href_1 = get_href.rsplit("-",2)[0] 
        get_href = get_href.replace(get_href_1,"")
        get_href_2 = get_category.get('href').replace("/Hotels-","")
        get_href_2 = get_href_2.replace(get_href_1,"")
        get_href_2 = get_href_2.replace("-Hotels.html","")
        get_href_2 = get_href_2.replace("-","")   
        categories.append(get_href_1)
        categories_2.append(get_href)
        categories_3.append(get_href_2)
        
for j in range(0,len(categories)-52):
    k = 0
    for i in range(1,2):
        driver.get("https://www.tripadvisor.com/Hotels-"+ str(categories[j]) + "-oa"+ str(k) +str(categories_2[j]))
        k += 30
        city = categories_3[j]
        content = driver.page_source
        soup = BeautifulSoup(content)
        for a in soup.findAll('div',attrs={'class':'ui_column is-8 main_col allowEllipsis'}):
            name=a.find('a' ,attrs={'class':'property_title prominent'})
            price=a.find('div',attrs={'class':'price __resizeWatch'})

            if price==None:
                    price="PKR 22,000"
            reviews=a.find('a',attrs={'class':'review_count'})   
            if reviews==None:
                reviews="0"
            rating=a.find('a',attrs={'class':'ui_bubble_rating bubble_50'})
            if rating==None:
                rating=a.find('a',attrs={'class':'ui_bubble_rating bubble_45'})
                if rating==None:
                    rating=a.find('a',attrs={'class':'ui_bubble_rating bubble_40'})
                    if rating==None:
                        rating=a.find('a',attrs={'class':'ui_bubble_rating bubble_35'})
                        if rating==None:
                            rating=a.find('a',attrs={'class':'ui_bubble_rating bubble_30'})
                            if rating==None:
                                rating=a.find('a',attrs={'class':'ui_bubble_rating bubble_25'})
                                if rating==None:
                                    rating=a.find('a',attrs={'class':'ui_bubble_rating bubble_20'})
                                    if rating==None:
                                        rating=a.find('a',attrs={'class':'ui_bubble_rating bubble_15'})
                                        if rating==None:
                                            rating=a.find('a',attrs={'class':'ui_bubble_rating bubble_10'})
            if rating==None:
                rating="0"
            else:
                rating=rating["alt"]
                rating=rating.replace(' of 5 bubbles','')
            
            ranking=a.find('div',attrs={'class':'popindex'})
            if ranking==None:
                    ranking="Not available"
            services=a.find('div',attrs={'class':'label'})
            if services==None:
                services="Not available"
            
            if hasattr(price,'text'):
                price=price.text
            
            if hasattr(services,'text'):
                services=services.text
            
            if hasattr(ranking,'text'):
                ranking=ranking.text

            h=hotel(*name,price,city,rating,reviews.text,services,ranking)
            array_list.append(h)
            
header = ['Name', 'Price', 'City','Rating','Reviews','Services','Ranking']
with open("hotels.csv", "w", newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(header)
for i in array_list:
    data=[i.name,i.price,i.reviews,i.rating,i.city,i.services,i.ranking]
    with open("hotels.csv", "a", newline='',encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(data)
        
class sortwindow(QMainWindow):
    def __init__(self):
        super(sortWindow,self).__init__()
        
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("tripAdvisor.ui",self)
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(6,250)
        data_array=self.getdata()
        self.loaddata(data_array)
        
    def getdata(self):  
        data_array=[]
        with open("C:\\Users\\rizwa\\Documents\\GitHub\\CS261F21PID20\\hotels.csv","r") as file:
            reader=csv.reader(file)
            for row in reader:
                data_array.append(row)
        return data_array
        
    def loaddata(self,data_array):
        row=0
        for i in data_array:
            data=[{"Name":i[0],"Price":i[1],"Reviews":i[2],"Rating":i[3],"City":i[4],"Services":i[5],"Ranking":i[6]}]
            self.tableWidget.setRowCount(len(data_array))
            for person in data:
                self.tableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(person["Name"]))
                self.tableWidget.setItem(row,1,QtWidgets.QTableWidgetItem(person["Price"]))
                self.tableWidget.setItem(row,2,QtWidgets.QTableWidgetItem(person["Reviews"]))
                self.tableWidget.setItem(row,3,QtWidgets.QTableWidgetItem(person["Rating"]))
                self.tableWidget.setItem(row,4,QtWidgets.QTableWidgetItem(person["City"]))
                self.tableWidget.setItem(row,5,QtWidgets.QTableWidgetItem(person["Services"]))
                self.tableWidget.setItem(row,6,QtWidgets.QTableWidgetItem(person["Ranking"]))
            row+=1
    
if QApplication.instance():
    app = QApplication.instance()
else:
    app = QApplication(sys.argv)
# app=QApplication(sys.argv)
mainwindow=MainWindow()
# widget=QMainWindow()
mainwindow.show()
app.exec_()

