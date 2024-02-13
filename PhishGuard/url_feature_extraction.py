# -*- coding: utf-8 -*-
"""URL_Feature_Extraction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dbf2KaYvjz75EP7QiHBY0OiHd56Cwezy

# **Phishing Website Detection Feature Extraction**

*Final project of Machine learning & Cybersecurity Course*

# **1. Objective:**
A phishing website is a common social engineering method that mimics trustful uniform resource locators (URLs) and webpages. The objective of this notebook is to collect data & extract the selctive features form the URLs.

*This project is worked on Google Collaboratory.*
"""

from google.colab import drive
drive.mount('/content/drive')

"""## **2.1. Phishing URLs:**

The phishing URLs are collected from the PhishTank from the link provided. The csv file of phishing URLs is obtained by using wget command. After downlaoding the dataset, it is loaded into a DataFrame.
"""

#importing required packages for this module
!pip install python-whois

!pip install joblib

import pandas as pd
from urllib.parse import urlparse,urlencode
import ipaddress
import re
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
from datetime import datetime
import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime
from urllib.parse import urlparse, urljoin
import joblib

"""The above command downlaods the file of phishing URLs, *online-valid.csv* and stores in the */content/* folder."""

#loading the phishing URLs data to dataframe
s = input("Enter the URL for testing: ")
data0 = pd.DataFrame({"URLs": [s]})
# data0 = pd.read_csv("urls-phishing.csv", delimiter='\t')
# data0.columns = ['URLs']
data0.head()

data0.shape



"""So, the data has thousands of phishing URLs. But the problem here is, this data gets updated hourly. Without getting into the risk of data imbalance, I am considering a margin value of 10,000 phishing URLs & 5000 legitimate URLs.

Thereby, picking up 3000 samples from the above dataframe randomly.
"""

#Collecting 5,000 Phishing URLs randomly
phishurl = data0.sample(n = 1, random_state = 12).copy()
phishurl = phishurl.reset_index(drop=True)
phishurl.head()

phishurl.shape

"""# **3. Feature Extraction:**

In this step, features are extracted from the URLs dataset.

The extracted features are categorized into


1.   Address Bar based Features
2.   Domain based Features
3.   HTML & Javascript based Features

### **3.1. Address Bar Based Features:**

Many features can be extracted that can be consided as address bar base features. Out of them, below mentioned were considered for this project.


*   Domain of URL
*   IP Address in URL
*   "@" Symbol in URL
*   Length of URL
*   Depth of URL
*   Redirection "//" in URL
*   "http/https" in Domain name
*   Using URL Shortening Services “TinyURL”
*   Prefix or Suffix "-" in Domain

Each of these features are explained and the coded below:

#### **3.1.1. Domain of the URL**
Here, we are just extracting the domain present in the URL. This feature doesn't have much significance in the training. May even be dropped while training the model.
"""

# 1.Domain of the URL (Domain)
def getDomain(url):
  domain = urlparse(url).netloc
  if re.match(r"^www.",domain):
    domain = domain.replace("www.","")
  return domain

"""#### **3.1.2. IP Address in the URL**

Checks for the presence of IP address in the URL. URLs may have IP address instead of domain name. If an IP address is used as an alternative of the domain name in the URL, we can be sure that someone is trying to steal personal information with this URL.

If the domain part of URL has IP address, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).


"""

# 2.Checks for IP address in URL (Have_IP)
def havingIP(url):
  try:
    ipaddress.ip_address(url)
    ip = 1
  except:
    ip = 0
  return ip

"""#### **3.1.3. "@" Symbol in URL**

Checks for the presence of '@' symbol in the URL. Using “@” symbol in the URL leads the browser to ignore everything preceding the “@” symbol and the real address often follows the “@” symbol.

If the URL has '@' symbol, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""

# 3.Checks the presence of @ in URL (Have_At)
def haveAtSign(url):
  if "@" in url:
    at = 1
  else:
    at = 0
  return at

"""#### **3.1.4. Length of URL**

Computes the length of the URL. Phishers can use long URL to hide the doubtful part in the address bar. In this project, if the length of the URL is greater than or equal 54 characters then the URL classified as phishing otherwise legitimate.

If the length of URL >= 54 , the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""

# 4.Finding the length of URL and categorizing (URL_Length)
def getLength(url):
  if len(url) < 54:
    length = 0
  else:
    length = 1
  return length

"""#### **3.1.5. Depth of URL**

Computes the depth of the URL. This feature calculates the number of sub pages in the given url based on the '/'.

The value of feature is a numerical based on the URL.
"""

# 5.Gives number of '/' in URL (URL_Depth)
def getDepth(url):
  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth

"""#### **3.1.6. Redirection "//" in URL**

Checks the presence of "//" in the URL. The existence of “//” within the URL path means that the user will be redirected to another website. The location of the “//” in URL is computed. We find that if the URL starts with “HTTP”, that means the “//” should appear in the sixth position. However, if the URL employs “HTTPS” then the “//” should appear in seventh position.

If the "//" is anywhere in the URL apart from after the protocal, thee value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""

# 6.Checking for redirection '//' in the url (Redirection)
def redirection(url):
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      return 1
    else:
      return 0
  else:
    return 0

"""#### **3.1.7. "http/https" in Domain name**

Checks for the presence of "http/https" in the domain part of the URL. The phishers may add the “HTTPS” token to the domain part of a URL in order to trick users.

If the URL has "http/https" in the domain part, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""

# 7.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
def httpDomain(url):
  domain = urlparse(url).netloc
  if 'https' in domain:
    return 1
  else:
    return 0

"""#### **3.1.8. Using URL Shortening Services “TinyURL”**

URL shortening is a method on the “World Wide Web” in which a URL may be made considerably smaller in length and still lead to the required webpage. This is accomplished by means of an “HTTP Redirect” on a domain name that is short, which links to the webpage that has a long URL.

If the URL is using Shortening Services, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""

#listing shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    match=re.search(shortening_services,url)
    if match:
        return 1
    else:
        return 0

"""#### **3.1.9. Prefix or Suffix "-" in Domain**

Checking the presence of '-' in the domain part of URL. The dash symbol is rarely used in legitimate URLs. Phishers tend to add prefixes or suffixes separated by (-) to the domain name so that users feel that they are dealing with a legitimate webpage.

If the URL has '-' symbol in the domain part of the URL, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""

# 9.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            # legitimate

"""### **3.2. Domain Based Features:**

Many features can be extracted that come under this category. Out of them, below mentioned were considered for this project.

*   DNS Record
*   Website Traffic
*   Age of Domain
*   End Period of Domain

Each of these features are explained and the coded below:
"""

!pip install python-whois

# importing required packages for this section
import re
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
from datetime import datetime

import urllib.request

url = "http://sitecostumizade.com/includes/portalbb/portalbb/"
ip_address = "xxx.xxx.xxx.xxx"  # Replace with the actual IP address

try:
    response = urllib.request.urlopen(url)
    print(response.read())
except Exception as e:
    print(f"Error: {e}")

"""#### **3.2.1. DNS Record**

For phishing websites, either the claimed identity is not recognized by the WHOIS database or no records founded for the hostname.
If the DNS record is empty or not found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""

# 11.DNS Record availability (DNS_Record)
# obtained in the featureExtraction function itself

"""#### **3.2.2. Web Traffic**

This feature measures the popularity of the website by determining the number of visitors and the number of pages they visit. However, since phishing websites live for a short period of time, they may not be recognized by the Alexa database (Alexa the Web Information Company., 1996). By reviewing our dataset, we find that in worst scenarios, legitimate websites ranked among the top 100,000. Furthermore, if the domain has no traffic or is not recognized by the Alexa database, it is classified as “Phishing”.

If the rank of the domain < 100000, the vlaue of this feature is 1 (phishing) else 0 (legitimate).
"""



import re

def get_alexa_rank(domain):
    try:
        url = f"https://www.alexa.com/siteinfo/{domain}"
        response = requests.get(url)
        response.raise_for_status()

        # Using regular expression to extract numeric part
        rank_match = re.search(r'<div class="rank-global">([\d,]+)</div>', response.text)
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

"""**Favilon**

"""

def is_favicon_external(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        favicon_link = soup.find('link', {'rel': 'icon'})


        if favicon_link:
            favicon_href = favicon_link.get('href')
            parsed_favicon_url = urlparse(favicon_href)
            parsed_main_url = urlparse(url)

            # Check if the favicon domain is different from the main URL domain
            return parsed_favicon_url.netloc != parsed_main_url.netloc

    except requests.RequestException:
        pass

    return False

def favilon(url):
    if is_favicon_external(url):
        return 1  # Phishing
    else:
        return 0  # Legitimate

"""**1.1.7.Sub Domain and Multi Sub Domains **
Let us assume we have the following link: http://www.hud.ac.uk/students/. A domain name might
include the country-code top-level domains (ccTLD), which in our example is “uk”. The “ac” part is
shorthand for “academic”, the combined “ac.uk” is called a second-level domain (SLD) and “hud” is
the actual name of the domain. To produce a rule for extracting this feature, we firstly have to omit
the (www.) from the URL which is in fact a sub domain in itself. Then, we have to remove the
(ccTLD) if it exists. Finally, we count the remaining dots. If the number of dots is greater than one,
then the URL is classified as “Suspicious” since it has one sub domain. However, if the dots are
greater than two, it is classified as “Phishing” since it will have multiple sub domains. Otherwise, if
the URL has no sub domains, we will assign “Legitimate” to the feature.
Rule: IF ൝
Dots In Domain Part = 1 → Legitimate
Dots In Domain Part = 2 → Suspicious
Otherwise → Phishing

"""

from urllib.parse import urlparse

def sub_domain(url):
    # Parse the URL to get the domain part
    parsed_url = urlparse(url)
    domain_part = parsed_url.netloc.replace("www.", "")

    # Remove ccTLD if it exists
    parts = domain_part.split('.')
    if len(parts) > 1 and len(parts[-1]) <= 3:
        domain_part = '.'.join(parts[:-1])

    # Count the number of dots
    dot_count = domain_part.count('.')

    # Classification based on the number of dots
    if dot_count == 1:
        return -1
    elif dot_count == 2:
        return 0
    else:
        return 1

"""#### **3.2.3. Age of Domain**

This feature can be extracted from WHOIS database. Most phishing websites live for a short period of time. The minimum age of the legitimate domain is considered to be 12 months for this project. Age here is nothing but different between creation and expiration time.

If age of domain > 12 months, the vlaue of this feature is 1 (phishing) else 0 (legitimate).
"""

# 13.Survival time of domain: The difference between termination time and creation time (Domain_Age)
def domainAge(domain_name):
  creation_date = domain_name.creation_date
  expiration_date = domain_name.expiration_date
  if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
    try:
      creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return 1
  if ((expiration_date is None) or (creation_date is None)):
      return 1
  elif ((type(expiration_date) is list) or (type(creation_date) is list)):
      return 1
  else:
    ageofdomain = abs((expiration_date - creation_date).days)
    if ((ageofdomain/30) < 6):
      age = 1
    else:
      age = 0
  return age

"""### **1.1.8.HTTPS (Hyper Text Transfer Protocol with Secure Sockets Layer) **
The existence of HTTPS is very important in giving the impression of website legitimacy, but this is
clearly not enough. The authors in (Mohammad, Thabtah and McCluskey 2012) (Mohammad,
Thabtah and McCluskey 2013) suggest checking the certificate assigned with HTTPS including the
extent of the trust certificate issuer, and the certificate age. Certificate Authorities that are consistently
listed among the top trustworthy names include: “GeoTrust, GoDaddy, Network Solutions, Thawte,
Comodo, Doster and VeriSign”. Furthermore, by testing out our datasets, we find that the minimum
age of a reputable certificate is two years.
Rule: IFቐ
Use https and Issuer Is Trusted and Age of Certificate ≥ 1 Years → Legitimate
 Using https and Issuer Is Not Trusted → Suspicious
Otherwise → Phishing

"""

import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime

TRUSTED_ISSUERS = ["GeoTrust", "GoDaddy", "Network Solutions", "Thawte", "Comodo", "Doster", "VeriSign"]
MIN_REPUTABLE_CERT_AGE = 2  # Minimum age of a reputable certificate in years

def get_certificate_info(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        cert = response.connection.sock.getpeercert(binary_form=True)
        return x509.load_der_x509_certificate(cert, default_backend())
    except requests.RequestException:
        return None

def https(url):
    try:
        certificate = get_certificate_info(url)
        if certificate:
            issuer = certificate.issuer.common_name
            age_in_years = (datetime.now() - certificate.not_valid_before).days // 365

            if url.startswith("https://") and issuer in TRUSTED_ISSUERS and age_in_years >= MIN_REPUTABLE_CERT_AGE:
                return -1
            elif url.startswith("https://") and issuer not in TRUSTED_ISSUERS:
                return 0

    except Exception as e:
        print(f"Error: {e}")

    return 1

"""#### **3.2.4. End Period of Domain**

This feature can be extracted from WHOIS database. For this feature, the remaining domain time is calculated by finding the different between expiration time & current time. The end period considered for the legitimate domain is 6 months or less  for this project.

If end period of domain > 6 months, the vlaue of this feature is 1 (phishing) else 0 (legitimate).
"""

# 14.End time of domain: The difference between termination time and current time (Domain_End)
def domainEnd(domain_name):
  expiration_date = domain_name.expiration_date
  if isinstance(expiration_date,str):
    try:
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
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

"""# **1.1.11. Using Non-Standard Port**

This feature is useful in validating if a particular service (e.g. HTTP) is up or down on a specific
server. In the aim of controlling intrusions, it is much better to merely open ports that you need.
Several firewalls, Proxy and Network Address Translation (NAT) servers will, by default, block all or
most of the ports and only open the ones selected. If all ports are open, phishers can run almost any
service they want and as a result, user information is threatened. The most important ports and their
preferred status are shown in Table 2.
Rule: IF൜
Port # is of the Preffered Status → Phishing
Otherwise → Legitimate

"""

def Port(url):
    preferred_ports = [80, 443]  # Preferred ports
    non_preferred_ports = [21, 22, 23, 445, 1433, 1521, 3306, 3389]  # Non-preferred ports

    try:
        port = url.split(":")[-1]  # Extract port from the URL

        if port.isdigit():
            port = int(port)

            if port in preferred_ports:
                return 0
            elif port in non_preferred_ports:
                return 1

    except Exception as e:
        print(f"Error: {e}")

    return 0  # Default classification if port cannot be determined

"""## **3.3. HTML and JavaScript based Features**

Many features can be extracted that come under this category. Out of them, below mentioned were considered for this project.

*   IFrame Redirection
*   Status Bar Customization
*   Disabling Right Click
*   Website Forwarding

Each of these features are explained and the coded below:
"""



"""### **3.3.1. IFrame Redirection**

IFrame is an HTML tag used to display an additional webpage into one that is currently shown. Phishers can make use of the “iframe” tag and make it invisible i.e. without frame borders. In this regard, phishers make use of the “frameBorder” attribute which causes the browser to render a visual delineation.

If the iframe is empty or repsonse is not found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""

# 15. IFrame Redirection (iFrame)
def iframe(response):
  if response == "":
      return 1
  else:
      if re.findall(r"[<iframe>|<frameBorder>]", response.text):
          return 0
      else:
          return 1

"""### **3.3.2. Status Bar Customization**

Phishers may use JavaScript to show a fake URL in the status bar to users. To extract this feature, we must dig-out the webpage source code, particularly the “onMouseOver” event, and check if it makes any changes on the status bar

If the response is empty or onmouseover is found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).
"""

# 16.Checks the effect of mouse over on status bar (Mouse_Over)
def mouseOver(response):
  if response == "" :
    return 1
  else:
    if re.findall("<script>.+onmouseover.+</script>", response.text):
      return 1
    else:
      return 0

"""### **3.3.3. Disabling Right Click**

Phishers use JavaScript to disable the right-click function, so that users cannot view and save the webpage source code. This feature is treated exactly as “Using onMouseOver to hide the Link”. Nonetheless, for this feature, we will search for event “event.button==2” in the webpage source code and check if the right click is disabled.

If the response is empty or onmouseover is not found then, the value assigned to this feature is 1 (phishing) or else 0 (legitimate).



"""

# 17.Checks the status of the right click attribute (Right_Click)
def rightClick(response):
  if response == "":
    return 1
  else:
    if re.findall(r"event.button ?== ?2", response.text):
      return 0
    else:
      return 1

"""### **3.3.4. Website Forwarding**
The fine line that distinguishes phishing websites from legitimate ones is how many times a website has been redirected. In our dataset, we find that legitimate websites have been redirected one time max. On the other hand, phishing websites containing this feature have been redirected at least 4 times.



"""

# 18.Checks the number of forwardings (Web_Forwards)
def forwarding(response):
  if response == "":
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      return 1

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
        response = requests.get(f'https://www.prchecker.info/check_page_rank.php?url={url}')
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

"""### **1.2. Abnormal Based Features **

# **1.2.1. Request URL**
Request URL examines whether the external objects contained within a webpage such as images,
videos and sounds are loaded from another domain. In legitimate webpages, the webpage address and
most of objects embedded within the webpage are sharing the same domain.
Rule: IF ቐ
% of Request URL < 22% → Legitimate
%of Request URL ≥ 22% and 61% → Suspicious
Otherwise → feature = Phishing
"""

from urllib.parse import urlparse, urljoin

def get_external_object_percentage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        total_objects = 0
        external_objects = 0

        for tag in soup.find_all(['img', 'video', 'audio', 'script', 'link', 'iframe']):
            src = tag.get('src') or tag.get('href')  # Extract source attribute

            if src:
                absolute_url = urljoin(url, src)
                parsed_url = urlparse(absolute_url)

                if parsed_url.netloc != urlparse(url).netloc:
                    external_objects += 1

                total_objects += 1

        if total_objects > 0:
            percentage = (external_objects / total_objects) * 100
            return percentage
        else:
            return 0

    except requests.RequestException:
        return None

def request_url(url):
    percentage = get_external_object_percentage(url)

    if percentage is not None:
        if percentage < 22:
            return -1
        elif 22 <= percentage <= 61:
            return 0
        else:
            return 1
    else:
        return 1

"""# **1.2.2. URL of Anchor **
An anchor is an element defined by the <a> tag. This feature is treated exactly as “Request URL”.
However, for this feature we examine:
1. If the <a> tags and the website have different domain names. This is similar to request URL
feature.
2. If the anchor does not link to any webpage, e.g.:
A. <a href=“#”>
B. <a href=“#content”>
C. <a href=“#skip”>
D. <a href=“JavaScript ::void(0)”>
Rule: IF൝
% of URL Of Anchor < 31% → 𝐿𝑒𝑔𝑖𝑡𝑖𝑚𝑎𝑡𝑒
% of URL Of Anchor ≥ 31% And ≤ 67% → Suspicious
Otherwise → Phishing

"""

def get_anchor_url_percentage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        total_anchors = 0
        external_anchors = 0
        empty_anchors = 0

        for tag in soup.find_all('a'):
            href = tag.get('href')

            if href:
                absolute_url = urljoin(url, href)
                parsed_url = urlparse(absolute_url)

                if parsed_url.netloc != urlparse(url).netloc:
                    external_anchors += 1

                total_anchors += 1

                # Check for empty or non-webpage anchors
                if parsed_url.path in {'', '#', '#content', '#skip'} or parsed_url.scheme.lower() == 'javascript':
                    empty_anchors += 1

        if total_anchors > 0:
            external_percentage = (external_anchors / total_anchors) * 100
            empty_percentage = (empty_anchors / total_anchors) * 100

            return external_percentage, empty_percentage
        else:
            return 0, 0

    except requests.RequestException:
        return None, None

def anchor_url(url):
    external_percentage, empty_percentage = get_anchor_url_percentage(url)

    if external_percentage is not None and empty_percentage is not None:
        if empty_percentage < 31:
            return -1
        elif 31 <= empty_percentage <= 67:
            return 0
        else:
            return 1
    else:
        return 1

"""# **1.2.3. Links in <Meta>, <Script> and <Link> tags**
Given that our investigation covers all angles likely to be used in the webpage source code, we find
that it is common for legitimate websites to use <Meta> tags to offer metadata about the HTML
document; <Script> tags to create a client side script; and <Link> tags to retrieve other web resources.
It is expected that these tags are linked to the same domain of the webpage.
Rule:
IF൝
% of Links in " < Meta > ", " < Script > " and " < Link>" < 17% → Legitimate
% of Links in < Meta > ", " < Script > " and " < Link>" ≥ 17% And ≤ 81% → Suspicious
Otherwise → Phishing

"""

def get_links_in_tags_percentage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        total_links = 0
        external_links = 0

        tags_with_links = ['meta', 'script', 'link']

        for tag_name in tags_with_links:
            for tag in soup.find_all(tag_name):
                href = tag.get('href') or tag.get('src')

                if href:
                    absolute_url = urljoin(url, href)
                    parsed_url = urlparse(absolute_url)

                    if parsed_url.netloc != urlparse(url).netloc:
                        external_links += 1

                    total_links += 1

        if total_links > 0:
            percentage = (external_links / total_links) * 100
            return percentage
        else:
            return 0

    except requests.RequestException:
        return None

def links_in_tags(url):
    percentage = get_links_in_tags_percentage(url)

    if percentage is not None:
        if percentage < 17:
            return -1
        elif 17 <= percentage <= 81:
            return 0
        else:
            return 1
    else:
        return 1

"""# *1.2.4. Server Form Handler (SFH) *

SFHs that contain an empty string or “about:blank” are considered doubtful because an action should
be taken upon the submitted information. In addition, if the domain name in SFHs is different from
the domain name of the webpage, this reveals that the webpage is suspicious because the submitted
information is rarely handled by external domains.
Rule: IF൝
SFH is "about: blank" Or Is Empty → Phishing
 SFH Refers To A Different Domain → Suspicious
Otherwise → Legitimate
"""

def get_sfh_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        sfh_values = set()

        for form in soup.find_all('form'):
            action = form.get('action')

            if action:
                absolute_url = urljoin(url, action)
                sfh_values.add(absolute_url)

        return sfh_values

    except requests.RequestException:
        return None

def sfh(url):
    sfh_values = get_sfh_info(url)

    if sfh_values is not None:
        for sfh in sfh_values:
            parsed_sfh = urlparse(sfh)

            if sfh == "about:blank" or sfh == "" or parsed_sfh.netloc != urlparse(url).netloc:
                return 1

        return 0
    else:
        return 1

"""# **1.2.5. Submitting Information to Email**

Web form allows a user to submit his personal information that is directed to a server for processing.
A phisher might redirect the user’s information to his personal email. To that end, a server-side script
language might be used such as “mail()” function in PHP. One more client-side function that might be
used for this purpose is the “mailto:” function.
Rule: IF൜
Using "mail()" or "mailto:" Function to Submit User Information → Phishing
Otherwise → Legitimate

"""

def email_submission(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for form in soup.find_all('form'):
            action = form.get('action')

            if 'mailto:' in action:
                return 1

            for input_tag in form.find_all('input'):
                if 'mail()' in input_tag.get('value', '').lower():
                    return 1

        return 0

    except requests.RequestException:
        return 1

"""# **1.2.6. Abnormal URL **
This feature can be extracted from WHOIS database. For a legitimate website, identity is typically
part of its URL.
Rule: IF ൜
The Host Name Is Not Included In URL → Phishing
Otherwise → Legitimate

"""

def get_hostname_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname

def hostname(url):
    try:
        hostname = get_hostname_from_url(url)
        if not hostname:
            return 1

        domain_info = whois.whois(hostname)
        if not domain_info.domain_name:
            return 1

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return False

"""## **4. Computing URL Features**

Create a list and a function that calls the other functions and stores all the features of the URL in the list. We will extract the features of each URL and append to this list.
"""

#Function to extract features
def featureExtraction(url,label):

  features = []
  #Address bar based features (10)
  features.append(getDomain(url))
  features.append(havingIP(url))
  features.append(haveAtSign(url))
  features.append(getLength(url))
  features.append(getDepth(url))
  features.append(redirection(url))
  features.append(httpDomain(url))
  features.append(tinyURL(url))
  features.append(prefixSuffix(url))
  features.append(request_url(url))
  features.append(anchor_url(url))
  features.append(links_in_tags(url))
  features.append(sfh(url))
  features.append(email_submission(url))
  features.append(hostname(url))

  #Domain based features (4)
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1

  features.append(dns)
  features.append(Web_traffic(url))
  features.append(favilon(url))
  features.append(sub_domain(url))
  features.append(https(url))
  features.append(1 if dns == 1 else domainAge(domain_name))
  features.append(1 if dns == 1 else domainEnd(domain_name))
  features.append(Port(url))

  # HTML & Javascript based features (4)
  try:
    response = requests.get(url)
  except:
    response = ""
  features.append(iframe(response))
  features.append(mouseOver(response))
  features.append(rightClick(response))
  features.append(forwarding(response))
  features.append(page_rank(url))
  features.append(google_index(url))
  features.append(links_to_page(url))
  # features.append(popup(url))
  # features.append(label)


  return features

"""### **4.2. Phishing URLs:**

Now, feature extraction is performed on phishing URLs.
"""

phishurl.shape

phishurl.head()

#Extracting the feautres & storing them in a list
phish_features = []
label = 1
for i in range(1):
  url = phishurl['URLs'][i]
  print(i,end=" ")
  phish_features.append(featureExtraction(url,label))

#converting the list to dataframe
feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth','Redirection',
                      'https_Domain', 'TinyURL', 'Prefix/Suffix','request_url','Anchor_url','Links_in_tags','sfh','email_submission','hostname', 'DNS_Record', 'Web_Traffic','Favilon','Sub_domain','https',
                      'Domain_Age', 'Domain_End','Port', 'iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards','Page_rank','google_index', 'Links_to_pages']
phishing = pd.DataFrame(phish_features, columns= feature_names)

phishing=phishing.drop('Domain',axis=1)
phishing=phishing.drop('Have_At',axis=1)
phishing.head()

# Load the model from the file
loaded_model = joblib.load('/content/drive/MyDrive/Project Phase-1/Code/Url analysis/model/ensemble_model.joblib')

y=loaded_model.predict(phishing)

y

# # Storing the extracted legitimate URLs fatures to csv file
# phishing.to_csv('phishing.csv', index= False)