from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import time
from loguru import logger
import typer
import sys
import os

driver_path = "./chromedriver"
base_url = "http://tonkiang.us/hotellist.html"
php_url = "http://tonkiang.us/hoteliptv.php"

config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{level} {time} - {message}", "level": "INFO"},
        {
            "sink": f"{os.path.expanduser('~')}/refresh_aptv.log",
            "format": "{level} {time} - {message}",
            "level": "DEBUG",
        },
    ],
}
logger.configure(**config)
app = typer.Typer()

VERSION = "0.1"


def get_webpage_text_selenium(
    url,
    filename,
    click_link_2=False,
    click_link_3=False,        
    search_regex_pattern="http[s]?://",
    max_retries=10,
):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    search_regex = re.compile(search_regex_pattern)
    # Setup WebDriver
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    text = ""
    try:
        retries = 0
        while retries < max_retries:
            time.sleep(10)
            # Navigate to the URL
            driver.get(url)

            # Wait for the page to load completely, adjust the timeout as necessary
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Extract text
            text = driver.find_element(By.TAG_NAME, "body").text
            # Check if the text contains any http links
            if re.search(search_regex, text):
                if click_link_2:
                    link_text = "2"  # This is the text inside the <a> tag
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, link_text))
                    )
                    # Click the link
                    link = driver.find_element(By.LINK_TEXT, link_text)
                    link.click()
                    # Wait for a specific element to ensure the page has loaded/updated
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.TAG_NAME, "body"))
                    )
                    # Extract and return the content of the page
                    page_2 = driver.find_element(By.TAG_NAME, "body").text
                    text = text + "\n" + page_2
                if click_link_3:
                    link_text = "3"  # This is the text inside the <a> tag
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, link_text))
                    )
                    # Click the link
                    link = driver.find_element(By.LINK_TEXT, link_text)
                    link.click()
                    # Wait for a specific element to ensure the page has loaded/updated
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.TAG_NAME, "body"))
                    )
                    # Extract and return the content of the page
                    page_3 = driver.find_element(By.TAG_NAME, "body").text
                    text = text + "\n" + page_3
                    
                # Save the text to a file if URLs are found
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(text)
                logger.info(f"Text with URLs saved to {filename}")
                return text
            else:
                # Increment the retry counter if no URLs are found
                logger.info(f"url: {url}, text: {text}")                
                logger.info(f"No URLs found on retry {retries + 1}. Retrying...")
                retries += 1

        logger.info("Maximum retries reached without finding URLs.")
    except TimeoutException:
        print(f"{url} was not available, skip it")
    finally:
        # Clean up: close the browser window
        driver.quit()
    return ""


def clean_raw(raw_txt):
    # Regex pattern to find channel names followed by URLs
    pattern = r"(\w+-?\w*\s*\w*\s*\w*)\n(http://.*)\n"
    # Use re.findall to extract all matches
    cleaned_txt = ""
    matches = re.findall(pattern, raw_txt)
    for name, url in matches:
        if " " not in url:
            cleaned_txt += f"{name},{url}\n"
    return cleaned_txt


def convert_input_to_m3u(input_text):
    lines = input_text.strip().split("\n")
    output_lines = ["#EXTM3U"]
    for line in lines:
        if len(line) > 0:
            items = line.split(",")
            name = items[0]
            url = items[1]
            output_lines.append(f"#EXTINF:-1,{name}")
            output_lines.append(url)
    return "\n".join(output_lines)


def gen_output_file(ip_port, output_file):
    items = ip_port.split(":")
    ip = items[0]
    port = items[1]
    url = f"{base_url}?s={ip}%3A{port}&Submit=+"
    filename = f"{ip}_webpage_text.txt"
    logger.info(f"url: {url}")
    raw_txt = get_webpage_text_selenium(url, filename, True, True)
    if len(raw_txt) == 0:
        return
    else:
        cleaned_txt = clean_raw(raw_txt)
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(cleaned_txt)
        logger.info(f"{output_file} created")


#         mcast_txt = convert_input_to_mcast(cleaned_txt)
#         # logger.info(m3u_txt)
#         with open(output_file, "w", encoding="utf-8") as file:
#             file.write(m3u_txt)
#         logger.info(f"{output_file} created")
#


def extract_hotel_iptv_ips(text):
    # Define a regular expression pattern to find the line starting with "Hotel IPTV"
    pattern = r"Hotel IPTV\n([\d\.\s]+)"

    # Search for the pattern in the input text
    match = re.search(pattern, text, re.MULTILINE)

    if match:
        # Extract the group containing the IPs
        ip_block = match.group(1)
        # Split the block into individual IPs and remove any extra whitespace
        ips = ip_block.split()
        return ips
    else:
        # Return an empty list if no matching line is found
        return []


def extract_mcast_ips(text):
    # Define a regular expression pattern to find the line starting with "Hotel IPTV"
    pattern = r"Multicast IP\n([\d\.\s]+)"

    # Search for the pattern in the input text
    match = re.search(pattern, text, re.MULTILINE)

    if match:
        # Extract the group containing the IPs
        ip_block = match.group(1)
        # Split the block into individual IPs and remove any extra whitespace
        ips = ip_block.split()
        return ips
    else:
        # Return an empty list if no matching line is found
        return []


def extract_ip_port(text):
    # Define a regular expression pattern to find the line starting with "Hotel IPTV"
    pattern = r"About \d results\n([\d\.]+:\d+)"

    # Search for the pattern in the input text
    match = re.search(pattern, text, re.MULTILINE)

    if match:
        # Extract the group containing the IPs
        ip_port = match.group(1)
        return ip_port
    else:
        # Return an empty list if no matching line is found
        return ""


def get_ip_port(ip):
    url = f"{php_url}?s={ip}"
    raw_txt = get_webpage_text_selenium(url, "tmp.txt", False, False, "About \d results")
    ip_port = extract_ip_port(raw_txt)
    return ip_port


@app.command()
def hotel():
    filename = "homepage_webpage.txt"
    raw_txt = get_webpage_text_selenium(php_url, filename, False, False, "Hotel IPTV")
    hotel_ips = extract_hotel_iptv_ips(raw_txt)
    logger.info(hotel_ips)
    if len(hotel_ips) == 0:
        logger.info(f"Not found host IP, please check {filename}")
    for idx, hotel_ip in enumerate(hotel_ips, start=1):
        output_file = f"hotel_{idx}.txt"
        ip_port = get_ip_port(hotel_ip)
        if len(ip_port) > 0:
            gen_output_file(ip_port, output_file)


@app.command()
def mcast():
    filename = "homepage_webpage.txt"
    raw_txt = get_webpage_text_selenium(php_url, filename, False, False, "Multicast IP")
    mcast_ips = extract_mcast_ips(raw_txt)
    logger.info(mcast_ips)
    if len(mcast_ips) == 0:
        logger.info(f"Not found mcast IP, please check {filename}")
    for idx, ip in enumerate(mcast_ips, start=1):
        output_file = f"mcast_{idx}.txt"
        ip_port = get_ip_port(ip)
        if len(ip_port) > 0:
            gen_output_file(ip_port, output_file)


@app.command()
def all():
    hotel()
    mcast()


@app.command()
def version():
    """Show current version"""
    print(VERSION)


if __name__ == "__main__":
    app()
