import requests

url = "http://0.0.0.0:1112/llm"

data = {
    "InputText": "Tôi cần máy giặt nào có khối lượng giặt 8kg",
    "IdRequest": "2082024",
    "NameBot": "ChatBot",
    "User": "20496",
    "GoodsCode": "",
    "ProvinceCode": "",
    "ObjectSearch": "",
    "PriceSearch": "",
    "DescribeSearch": "",
}

response = requests.post(url, data=data)
print(response.json())
