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
from Features import *
from AddressBarFeatures import *
from AbnormalFeatures import *
from DomainBasedFeatures import *
from HttpsBasedFeatures import *


"""## **4. Computing URL Features**

Create a list and a function that calls the other functions and stores all the features of the URL in the list. We will extract the features of each URL and append to this list.
"""

# Function to extract features


def featureExtraction(url):

    features = []
    # Address bar based features (10)
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

    # Domain based features (4)
    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dns = 1

    features.append(dns)
    features.append(Web_traffic(url))
    features.append(favicon(url))
    features.append(sub_domain(url))
    features.append(https(url))
    features.append(1 if dns == 1 else domainRegistrationLength(domain_name))
    features.append(1 if dns == 1 else AgeofDomain(domain_name))
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


phishurl = (input("Enter the URL : "))

"""### **4.2. Phishing URLs:**

Now, feature extraction is performed on phishing URLs.
"""


# Extracting the feautres & storing them in a list
phish_features = []
for i in range(1):
    url = phishurl
    print(i, end=" ")
    phish_features.append(featureExtraction(url))

# converting the list to dataframe
feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
                 'https_Domain', 'TinyURL', 'Prefix/Suffix', 'request_url', 'Anchor_url', 'Links_in_tags', 'sfh', 'email_submission', 'hostname', 'DNS_Record', 'Web_Traffic', 'Favilon', 'Sub_domain', 'https',
                 'Domain_Age', 'Domain_End', 'Port', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards', 'Page_rank', 'google_index', 'Links_to_pages']
phishing = pd.DataFrame(phish_features, columns=feature_names)

phishing = phishing.drop('Domain', axis=1)
phishing = phishing.drop('Have_At', axis=1)
print(phishing)

# Load the model from the file
loaded_model = joblib.load(
    '/content/drive/MyDrive/Project Phase-1/Code/Url analysis/model/ensemble_model.joblib')

y = loaded_model.predict(phishing)

print(y)

# # Storing the extracted legitimate URLs fatures to csv file
# phishing.to_csv('phishing.csv', index= False)
