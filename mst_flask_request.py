import requests
import time


# API endpoint
URL = "http://127.0.0.1:5000/start_story"

# Defining a dictionary for the JSON payload to be sent to the API
payload = {
    "narrative": "shrek",
    "learning_topic": "spanish colors",
    "number_of_parts": "3"
}

# Sending POST request with JSON payload
r = requests.post(url=URL, json=payload)

# Print the response status code
print(r)

# Check if the response was successful
if r.status_code == 200:
    # Extracting data in JSON format
    data = r.json()
    print(data)
else:
    print(f"Error: {r.status_code} - {r.text}")

print("\nSLEEP")
time.sleep(5)

# API endpoint
URL = "http://127.0.0.1:5000/continue_story"

# Defining a dictionary for the JSON payload to be sent to the API
payload = {
    "story_id": data['story_id']
}

# Sending POST request with JSON payload
r = requests.post(url=URL, json=payload)

# Print the response status code
print(r)

# Check if the response was successful
if r.status_code == 200:
    # Extracting data in JSON format
    data = r.json()
    print(data)
else:
    print(f"Error: {r.status_code} - {r.text}")