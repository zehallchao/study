import openpyxl
import random
#随机
def creat():
    eight = ''
    for i in range(8):
        eight=eight+str(random.randint(0,9))
    return "135{}".format(eight)

pwd='123456'
list=[]
user_list=[]
for i in range(1000):
    list=[creat(),pwd]
    user_list.append(list)

book=openpyxl.Workbook()
sheet1=book.active
a=['username','password']
sheet1.append(a)
for i in range(len(user_list)):
    sheet1.append(user_list[i])
book.save('./user.xlsx')
