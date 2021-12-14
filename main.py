#美团美食
# -*- coding:UTF-8 -*-
import requests
import time
from bs4
import json
import csv
import random
with open(r'C:\Users\Hanju\Desktop\美团西安美食.csv',"w", newline='',encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['网站名','品类','商家名称','地址'])
    target = 'http://xa.meituan.com/meishi/'
    ClassList=[393, 11, 17, 40, 36, 28, 35, 395, 54, 20003, 55, 56, 20004, 57, 400, 58, 41, 59, 60, 62, 63, 217, 227, 228, 229, 232, 233, 24]
    AreaList=[113, 6835, 7137, 900, 8976, 897, 898, 899, 908, 7402, 7404, 8974, 8975, 9012, 15634, 15639, 15642, 15643, 15664, 15667, 15784, 15785, 116, 907, 910, 1099, 4763, 6836, 7403, 8977, 8978, 8979, 8984, 15630, 15632, 15635, 15640, 15641, 119, 8980, 8983, 8991, 15629, 15631, 15633, 15636, 15637, 15638, 15646, 15647, 115, 8981, 903, 7479, 7405, 904, 905, 906, 6839, 7408, 7480, 8982, 14024, 14025, 117, 909, 7407, 7478, 7477, 7406, 8950, 7140, 8951, 8952, 7141, 7138, 9309, 9477, 13026, 25592, 37367, 114, 7476, 7142, 901, 6838, 902, 7143, 8985, 14026, 18674, 36710, 37380, 4251, 7398, 7399, 7400, 7401, 14199, 16010, 16013, 25659, 4253, 8986, 8987, 8989, 8990, 17228, 235, 7145, 7146, 7147, 7148, 15644, 15645, 15665, 15666, 15668, 4257, 16938, 25170, 25171, 7149, 25713, 25715, 25717, 25719, 25721, 4254, 23761, 23762, 23763, 4255, 22410, 22416, 118, 4256, 22405, 22408, 26289, 26295, 33947]
    for class_ in ClassList:
        for area in AreaList:
            for i in range(1,51):
                url=target+'c'+str(class_)+'b'+str(area)+'/pn'+str(i)+'/'
                head={}
                head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                head['authorization']='client-id'(cookie倒数第三个参数）
                req = requests.get(url=url,headers=head)
                html=req.text
                bf=BeautifulSoup(html,'lxml')
                tag=bf.find_all('script')[14]
                data=json.loads(str(tag)[27:-10])
                print(data)
                result=data['poiLists']['poiInfos']
                if result:
                    print(url)
                    for item in result:
                        Info_List=[]
                        Info_List.append('美团')
                        Info_List.append('美食')
                        Info_List.append(item['title'])
                        Info_List.append(item['address'])
                        writer.writerow(Info_List)
                    time.sleep(random.choice(range(2,5)))
                else:
                    break（如果该页没有商家列表，跳出循环）
print('Done')