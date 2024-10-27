import requests,os
#list_of_dir = os.listdir('D:\Programs\Python\Projects\API\static')
#for dir in list_of_dir:
  #  print('D:\\Programs\\Python\\Projects\\API\\static\\'+dir)
   # request = requests.put('http://127.0.0.1:5000/image/1',json={'img':'D:\\Programs\\Python\\Projects\\API\\static\\'+dir})
request = requests.delete('http://127.0.0.1:5000/image/90')
print(request.json())