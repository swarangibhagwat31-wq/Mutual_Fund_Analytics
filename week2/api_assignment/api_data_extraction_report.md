# API Data Extraction Assignment

## 1. Objective
To fetch data from a public REST API, understand its JSON response, and convert the extracted data into a CSV file using Python.

## 2. API Details
- **API Name:** JSONPlaceholder
- **Endpoint:** https://jsonplaceholder.typicode.com/posts
- **HTTP Method:** GET
- **Authentication:** Not required
- **Response Format:** JSON
- **HTTP Status Code:** 200 (OK)
- **Records Retrieved:** 100

## 3. JSON Response Structure
Each post contains the following fields:
- `userId`: ID of the user who created the post
- `id`: Unique ID of the post
- `title`: Title of the post
- `body`: Content of the post

## 4. Tools and Libraries
- Python
- Requests: Sends the HTTP request and retrieves the API response
- Pandas: Converts JSON data into a tabular DataFrame and exports it to CSV
- Visual Studio Code: Used to write and execute the Python script

## 5. Procedure
1. Opened the public API endpoint in a web browser.
2. Created a Python script named `fetch_api_data.py`.
3. Sent a GET request using the Requests library.
4. Checked the HTTP response for errors.
5. Converted the JSON response into a Pandas DataFrame.
6. Displayed the response status, record count, and first five records.
7. Exported the extracted data to `posts.csv`.

## 6. Output Files
- `fetch_api_data.py` — Python script used for data extraction.
- `posts.csv` — Extracted API data in CSV format.

## 7. Conclusion
Successfully retrieved JSON data from a public REST API and converted it into a CSV file. This assignment demonstrated the basic API data extraction workflow used in data analytics.

## 8. Learning Outcomes
- Understood REST API endpoints and GET requests.
- Learned how to inspect JSON responses.
- Used Python libraries to retrieve and transform API data.
- Exported structured data into CSV format for further analysis.