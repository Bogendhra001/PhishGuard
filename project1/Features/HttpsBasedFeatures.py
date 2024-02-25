import pandas as pd
from urllib.parse import urlparse, urlencode
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
    if response == "":
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
