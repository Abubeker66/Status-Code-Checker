import requests
import json
import logging
from concurrent.futures import ThreadPoolExecutor

# ----- Logging setup ----- #
logging.basicConfig(
    filename="status_checker.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ----- Function to check a single website ----- #
def check_website_status(website_url):
    """
    Sends an HTTP GET request to a website and returns its status.
    Logs the result to a file.
    """
    try:
        response = requests.get(website_url, timeout=5)  # send GET request
        status = response.status_code                      # get HTTP status
        logging.info(website_url + " - " + str(status))   # log to file
        return {"url": website_url, "status_code": status}
    except requests.RequestException:
        # if request fails (timeout, connection error, etc.)
        logging.error("Failed to reach " + website_url)
        return {"url": website_url, "status": "Failed"}

# ----- List of websites to check ----- #
websites_to_check = [
    "https://google.com",
    "https://github.com",
    "https://nonexistent.xyz"
]

# ----- Use ThreadPoolExecutor for concurrent checks ----- #
max_threads = 5  # number of parallel workers
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    # run check_website_status for each URL concurrently
    website_results = list(executor.map(check_website_status, websites_to_check))

# ----- Save results to JSON file ----- #
output_file = "status_results.json"
with open(output_file, "w") as json_file:
    json.dump(website_results, json_file, indent=4)

print("Website status results saved to " + output_file)
