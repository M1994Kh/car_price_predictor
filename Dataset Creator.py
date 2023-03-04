import re
import os
import requests
import mysql.connector
cnx = mysql.connector.connect(user='root' , password='',
                              host='127.0.0.1' ,
                              )
from bs4 import BeautifulSoup
html='html.parser'
cursor=cnx.cursor()
cursor.execute('CREATE DATABASE Advanced')
cursor.execute('USE Advanced;')
cursor.execute('CREATE TABLE dataset(BRAND_MODEL VARCHAR(50),YEAR INT, MILEAGE VARCHAR(10), PRICE VARCHAR(10))')
adre= os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'dataset.txt')
adr=os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'history.txt')
f=open(adre, "w")
f.close()
f=open(adr, "w")
f.close()
r=requests.get('https://www.truecar.com/used-cars-for-sale/listings')
soup= BeautifulSoup(r.text,html)
res1=soup.find_all('a')
print('page 1 scanned')
def txt_f(st,fi):
    flag = 0
    for line in fi:   
        if st in line:  
            flag = 1
            break 
    if flag == 0: 
        return (False) 
    else: 
        return (True)
for i in range (200):
    url='https://www.truecar.com/used-cars-for-sale/listings'+'/?page='+str(i+2)
    r=requests.get(url)
    soup= BeautifulSoup(r.text,html)
    res=soup.find_all('a')
    for item in res:
        res1.append(item)
    print('page %i scanned'%(i+2))
total=0
for item in res1:
    href=re.findall(r'href="(\/used-cars-for-sale.+)"><\/a>',str(item))
    href.append('')
    if '/used-cars-for-sale' in href[0]:
        total+=1
count=0
for item in res1:
    href=re.findall(r'href="(\/used-cars-for-sale.+)"><\/a>',str(item))
    href.append('')
    if '/used-cars-for-sale' in href[0]:
        href='https://www.truecar.com'+ href[0]
        o=open(adr,'a')
        o2=open(adr,'r')
        if txt_f(href,o2)==False: 
            r=requests.get(href)
            hre=href+'\n'
            o.write(hre)
            soup= BeautifulSoup(r.text,html)
            src=soup.find_all('p')
            year=(re.findall(r'listing\/.+\/(....)-',href))[0]
            brand_model=(re.findall(r'listing\/.+\/....-(.+)\/',href))[0]
            for item in src:
                if 'margin-top-1' in str(item):
                    mileage=(re.findall(r'margin-top-1">(.+)<',str(item)))[0]
            sou=str(soup)
            sl=sou.find('Price')+7
            sn=sl+12
            price=''
            pri=sou[sl:sn]
            dig=['$',',','0','1','2','3','4','5','6','7','8','9']
            for i in range (12):
                if pri[i] in dig:
                    price=price+pri[i]
            f=open(adre,'a')
            l=open(adre,'r')
            car=brand_model+' '+year+'  Mileage:'+mileage+'    Price:'+price
            count+=1
            cu=car+'\n'
            print('result %i out of %i'%(count,total))
            print(car)
            if txt_f(car,l)==False :
                f.write(cu)
                cursor.execute('INSERT INTO dataset VALUES(\'%s\',\'%s\',\'%s\',\'%s\')'%(brand_model,year,mileage,price))
                cnx.commit()          
o.close()
o2.close()
f.close()
l.close()
cnx.close()
        