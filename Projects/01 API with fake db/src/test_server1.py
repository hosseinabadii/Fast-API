import os
import requests

os.system("clear")


print("\nGetting an item by id:")
print(requests.get("http://127.0.0.1:8000/items/1").json())
print("-" * 50)


print("\nGetting an item by parameter:")
print(requests.get("http://127.0.0.1:8000/items?count=20&name=Hammer").json())
print("-" * 50)


print("\nAdding an item:")
print(
    requests.post(
        "http://127.0.0.1:8000/items/",
        json={
            "name": "Screwdriver",
            "price": 3.99,
            "count": 10,
            "id": 3,
            "category": "consumables",
        },
    ).json()
)
print("-" * 20)
print("Item Details:")
print(requests.get("http://127.0.0.1:8000/items/all").json())
print("-" * 50)


print("\nUpdating an item:")
print(requests.put("http://127.0.0.1:8000/items/1?count=2023").json())
print("-" * 20)
print("Item Details:")
print(requests.get("http://127.0.0.1:8000/items/all").json())
print("-" * 50)


print("\nDeleting an item:")
print(requests.delete("http://127.0.0.1:8000/items/0").json())
print("-" * 20)
print("Item Details:")
print(requests.get("http://127.0.0.1:8000/items/all").json())
print("-" * 50)
