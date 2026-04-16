import requests

# Connect to the open-source Useless Facts API (as specified in the query)
url = "https://uselessfacts.jsph.pl/random.json?language=en"

try:
    # Fetch one random fact
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an error if the request failed
    
    # Parse the JSON response
    data = response.json()
    
    # Extract and display the fact
    fact = data.get("text", "No fact available")
    print("Here's a useless fact for you:")
    print(fact)

except requests.exceptions.RequestException as e:
    print(f"Error connecting to the API: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
