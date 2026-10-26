
import requests
import pandas as pd

# API endpoint
url = "https://jsonplaceholder.typicode.com/posts"

# Send a GET request
response = requests.get(url, timeout=30)

# Check for errors
response.raise_for_status()

# Convert JSON response into Python data
data = response.json()

# Convert data into a DataFrame
df = pd.DataFrame(data)

# Display results
print("Status Code:", response.status_code)
print("Total Records:", len(df))
print("\nFirst 5 Records:")
print(df.head())

# Save the data as CSV
df.to_csv("posts.csv", index=False, encoding="utf-8")

print("\nData successfully saved to posts.csv")
