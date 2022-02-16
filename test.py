import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"name":"Flask rest API with richard K", 'views':8363, "likes":38656357},
    {"name":"deep learning with richard", 'views':834363, "likes":38656343357},
    {"name":"machine learing with richard", 'views':836723, "likes":386462656357}
]

for i in range(len(data)):
    resp = requests.patch(BASE + 'video/' + str(i), data[i])
    print(resp.json())
 
input()   
resp = requests.get(BASE + 'video/0')
print(resp.json())