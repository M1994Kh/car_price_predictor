
import mysql.connector
import random
import pandas as pd
from sklearn import linear_model
cnx = mysql.connector.connect(user='root' , password='',
                              host='127.0.0.1' ,
                              )
cursor=cnx.cursor()
models=list()
years=list()
mileages=list()
prices=list()
years1=list()
mileages1=list()
prices1=list()
x=0
cursor.execute('USE Advanced;')

def cint(std):
    num=['0','1','2','3','4','5','6','7','8','9']
    s=0
    st=str(std)
    tu=len(st)
    for i2 in range (tu):
        if st[i2] in num:
            s=s*10+int(st[i2])
    return(s)
cursor.execute('SELECT * FROM dataset;')
res=cursor.fetchall()
count=0
cou=0
for item in res:
    y1=cint(item[1])
    m1=cint(item[2])
    p1=cint(item[3])
    if y1>0 and m1>0 and p1>0:
        count+=1
        models.append(item[0])
print('There is %i results in our directory.' %(count))
mod=random.choice(models)
print('Please enter the car model:(example:%s)'%(mod))
model=input()
if model not in models:
    print('The car model that you entered is not found.Try again:')
    model =input()
for item in res:
    y1=cint(item[1])
    m1=cint(item[2])
    p1=cint(item[3])
    years1.append(y1)
    mileages1.append(m1)
    prices1.append(p1)
    if item[0]==model and y1>0 and m1>0 and p1>0:
        cou+=1
        years.append(y1)
        mileages.append(m1)
        prices.append(p1)
print('We found %i results same as your car model.'%(cou))
print('Please enter date of production:')
while x==0:
    year=int(input())
    x=1
    if year>max(years1) or year<min(years1):
        print('Please enter a valid date of production.It must be between %i to %i'%(min(years1),max(years1)))
        x=0
z=0
print('Please enter mileage:')
while z==0:
    mileage=int(input())
    z=1
    if mileage>max(mileages1) or mileage<min(mileages1):
        print('Please enter a valid date of production.It must be between %i to %i miles'%(min(mileages1),max(mileages1)))
        z=0
cnx.close()
if cou>2 :
    car_model={'years' : years ,
      'mileages' : mileages ,
      'prices' : prices
      }
    df = pd.DataFrame (car_model,columns=['years','mileages','prices'])
    X = df[['years','mileages']]
    Y = df['prices']
    regr = linear_model.LinearRegression()
    regr.fit(X, Y)
    pp =regr.predict([[year ,mileage]])
    if pp>1000:
        print ('Predicted Price for your car is:  $', "%.2f" % pp)
    else:
        print ('Sorry! Your car is a rare one. we are not able to predict a price for it')
else:
    car_model={'years' : years1 ,
      'mileages' : mileages1 ,
      'prices' : prices1
      }
    df = pd.DataFrame (car_model,columns=['years','mileages','prices'])
    X = df[['years','mileages']]
    Y = df['prices']
    regr = linear_model.LinearRegression()
    regr.fit(X, Y)
    pp =regr.predict([[year ,mileage]])
    if pp>1000:
        print ('Predicted Price for your car is:  $', "%.2f" % pp)
    else:
        print ('Sorry! Your car is a rare one. we are not able to predict a price for it')
