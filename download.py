import requests

def download_html(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Return the HTML content
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
url = "https://guide.michelin.com/hk/zh_HK/restaurants/all-starred"
html_content = download_html(url)

if html_content:
    # Print the first 500 characters as a preview
    print(html_content[:500])
    
    # Optionally, save to a file
    with open("webpage.html", "w", encoding="utf-8") as f:
        f.write(html_content)