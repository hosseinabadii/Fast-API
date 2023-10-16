import os
import requests

os.system("clear")

print("Updating an item:")
print("\nexample with a negative item_id:")
print(requests.put("http://127.0.0.1:8000/items/-1?count=-1").json())

print("\nexample with a short name:")
print(requests.put("http://127.0.0.1:8000/items/1?name=").json())

print("\nexample with a long name:")
print(requests.put("http://127.0.0.1:8000/items/1?name=SuperDuperHammer").json())

print("\nexample with a negative price:")
print(requests.put("http://127.0.0.1:8000/items/1?price=-100.00").json())