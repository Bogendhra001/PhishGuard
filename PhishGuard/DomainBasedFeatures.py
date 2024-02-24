"""#### **3.2.4. End Period of Domain**

This feature can be extracted from WHOIS database. For this feature, the remaining domain time is calculated by finding the different between expiration time & current time. The end period considered for the legitimate domain is 6 months or less  for this project.

If end period of domain > 6 months, the vlaue of this feature is 1 (phishing) else 0 (legitimate).
"""

# 14.End time of domain: The difference between termination time and current time (Domain_End)


def domainEnd(domain_name):
    expiration_date = domain_name.expiration_date
    if isinstance(expiration_date, str):
        try:
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if (expiration_date is None):
        return 1
    elif (type(expiration_date) is list):
        return 1
    else:
        today = datetime.now()
        end = abs((expiration_date - today).days)
        if ((end/30) < 6):
            end = 0
        else:
            end = 1
    return end


def get_alexa_rank(domain):
    try:
        url = f"https://www.alexa.com/siteinfo/{domain}"
        response = requests.get(url)
        response.raise_for_status()

        # Using regular expression to extract numeric part
        rank_match = re.search(
            r'<div class="rank-global">([\d,]+)</div>', response.text)
        if rank_match:
            rank_text = rank_match.group(1).replace(',', '')
            rank = int(rank_text)
            return rank
        else:
            return None
    except requests.RequestException:
        return None


def Web_traffic(domain):
    rank = get_alexa_rank(domain)
    if rank is not None and rank < 100000:
        return 1  # Phishing
    else:
        return 0  # Legitimate(domain):
    rank = get_alexa_rank(domain)
    if rank is not None and rank < 100000:
        return 1  # Phishing
    else:
        return 0  # Legitimate


"""## **1.3.4. Using Pop-up Window **


It is unusual to find a legitimate website asking users to submit their personal information through a
pop-up window. On the other hand, this feature has been used in some legitimate websites and its
main goal is to warn users about fraudulent activities or broadcast a welcome announcement, though
no personal information was asked to be filled in through these pop-up windows.
Rule: IF ൜
Popoup Window Contains Text Fields → Phishing
Otherwise → Legitimate

"""

# !pip install selenium

# from selenium import webdriver
# from selenium.webdriver.common.by import By

# def popup(url):
#     try:
#         # Use a WebDriver for Chrome (you can choose another browser)
#         driver = webdriver.Chrome()
#         driver.get(url)

#         # Find elements that open pop-up windows
#         popup_links = driver.find_elements(By.XPATH, '//*[@target="_blank" or @target="_new"]')

#         for link in popup_links:
#             # Open the link in a new window
#             original_window_handle = driver.current_window_handle
#             link.click()

#             # Switch to the new window
#             for window_handle in driver.window_handles:
#                 if window_handle != original_window_handle:
#                     driver.switch_to.window(window_handle)
#                     break

#             # Check if the new window contains text fields
#             text_fields = driver.find_elements(By.TAG_NAME, 'input[type="text"]')
#             if text_fields:
#                 return 1

#             # Close the new window
#             driver.close()

#             # Switch back to the original window
#             driver.switch_to.window(original_window_handle)

#         return 0

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         driver.quit()

#     return 0  # Default classification if there's an error

"""# **1.4.4. PageRank **

PageRank is a value ranging from “0” to “1”. PageRank aims to measure how important a webpage is
on the Internet. The greater the PageRank value the more important the webpage. In our datasets, we
find that about 95% of phishing webpages have no PageRank. Moreover, we find that the remaining
5% of phishing webpages may reach a PageRank value up to “0.2”.

"""


def get_page_rank(url):
    try:
        response = requests.get(
            f'https://www.prchecker.info/check_page_rank.php?url={url}')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract PageRank value if found
        pagerank_element = soup.select_one('.bigpr b')

        if pagerank_element:
            pagerank_value = pagerank_element.text.strip()
            return float(pagerank_value)
        else:
            # Handle the case where the element is not found
            print("PageRank element not found on the page.")
            return None

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def page_rank(url):
    pagerank_value = get_page_rank(url)

    if pagerank_value is not None:
        if pagerank_value == 0 or (0 < pagerank_value <= 0.2):
            return 1
        else:
            return 0
    else:
        return 1


"""# **1.4.5. Google Index**
This feature examines whether a website is in Google’s index or not. When a site is indexed by
Google, it is displayed on search results (Webmaster resources, 2014). Usually, phishing webpages
are merely accessible for a short period and as a result, many phishing webpages may not be found on
the Google index.
Rule: IF൜
Webpage Indexed by Google → Legitimate
Otherwise → Phishing
"""


def is_indexed_by_google(url):
    try:
        response = requests.get(f'https://www.google.com/search?q=site:{url}')
        response.raise_for_status()

        # Check if the website is mentioned in the search results
        return url.lower() in response.text.lower()

    except requests.RequestException as e:
        print(f"Error: {e}")
        return False


def google_index(url):
    if is_indexed_by_google(url):
        return 0
    else:
        return 1


"""# **1.4.6. Number of Links Pointing to Page **

The number of links pointing to the webpage indicates its legitimacy level, even if some links are of
the same domain (Dean, 2014). In our datasets and due to its short life span, we find that 98% of
phishing dataset items have no links pointing to them. On the other hand, legitimate websites have at
least 2 external links pointing to them.
Rule: IFቐ
Of Link Pointing to The Webpage = 0 → Phishing
Of Link Pointing to The Webpage > 0 and ≤ 2 → Suspicious
Otherwise → Legitimate
"""


def get_number_of_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Count the number of anchor tags
        num_links = len(soup.find_all('a'))

        return num_links

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def links_to_page(url):
    num_links = get_number_of_links(url)

    if num_links is not None:
        if num_links == 0:
            return 1
        elif 0 < num_links <= 2:
            return 0
        else:
            return -1
    else:
        return 1
