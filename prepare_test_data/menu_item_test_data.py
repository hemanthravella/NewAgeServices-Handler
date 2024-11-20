import requests
from faker import Faker
import random
from datetime import datetime

# Create an instance of the Faker class
fake = Faker()

# API endpoint and token
url = "http://localhost:8000/api/menu/v1/createItem"
headers = {
    "Authorization": "Token 0200afb75f14344416c0586e326da81b49cbc09d",
    "Content-Type": "application/json",
}

# List of possible values for fields
item_types = ["Snack", "Beverage", "Dessert", "Main Course", "Appetizer"]
menu_types = ["FullDay", "Breakfast", "Lunch", "Dinner", "Snack"]
descriptions = [
    "A tasty snack perfect for a quick bite.",
    "A refreshing drink to quench your thirst.",
    "A sweet and indulgent dessert to satisfy your cravings.",
    "A hearty meal to keep you full and satisfied.",
    "A light dish for a quick and healthy bite."
]

def generate_random_data():
    # Generate random data for the PATCH request
    item_data = {
        "item_name": fake.word().capitalize(),  # Random item name
        "item_type": random.choice(item_types),  # Random item type
        "menu_type": random.choice(menu_types),  # Random menu type
        "item_cost": round(random.uniform(1.0, 20.0), 2),  # Random cost between 1 and 20
        "item_description": random.choice(descriptions),  # Random description
        "is_allergic": random.choice([True, False]),  # Random allergy status
        "is_vegetarian": random.choice([True, False]),  # Random vegetarian status
        "is_available": random.choice([True, False]),  # Random availability status
        "item_upd_usr_email": fake.email(),  # Random user email
        "item_last_upd_ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    }

    return item_data

def send_patch_request(data):
    # Send POST request
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("Request successful")
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

def main():
    for _ in range(500):  # Send 500 PATCH requests
        random_data = generate_random_data()
        send_patch_request(random_data)

if __name__ == "__main__":
    main()
