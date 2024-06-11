import requests

# Define the URL of your FastAPI endpoint
url = "http://127.0.0.1:8000/filter/"

# Define the JSON payload
payload = {
    "input": "list me a office studs for men under 12000"
}

# Send the POST request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    print(response.json())
else:
    # Print an error message
    print("Error:", response.text)
