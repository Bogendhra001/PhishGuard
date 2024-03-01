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
from Features.AddressBarFeatures import *
from Features.AbnormalFeatures import *
from Features.DomainBasedFeatures import *
from Features.HttpsBasedFeatures import *


"""## **4. Computing URL Features**

Create a list and a function that calls the other functions and stores all the features of the URL in the list. We will extract the features of each URL and append to this list.
"""

# Function to extract features


def featureExtraction(url):

    features = []
    # Address bar based features (10)
    features.append(getDomain(url))
    print(features)
    features.append(havingIP(url))
    print(features)
    features.append(haveAtSign(url))
    print(features)
    features.append(getLength(url))
    print(features)
    features.append(getDepth(url))
    print(features)
    features.append(redirection(url))
    print(features)
    features.append(httpDomain(url))
    print(features)
    features.append(tinyURL(url))
    print(features)
    features.append(prefixSuffix(url))
    print(features)
    features.append(request_url(url))
    print(features)
    features.append(anchor_url(url))
    print(features)
    features.append(links_in_tags(url))
    print(features)
    features.append(sfh(url))
    print(features)
    features.append(email_submission(url))
    print(features)
    features.append(hostname(url))
    print(features)
    print("Done address")

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

    # this feature is giving the error that http socket is not present that comsumming lot of time
    # features.append(https(url))
    features.append(1)

    features.append(1 if dns == 1 else domainRegistrationLength(domain_name))
    features.append(1 if dns == 1 else AgeofDomain(domain_name))
    features.append(Port(url))
    print('Done dns')
    # HTML & Javascript based features (4)
    try:
        response = requests.get(url)
    except:
        response = ""
    features.append(iframe(response))
    features.append(mouseOver(response))
    features.append(rightClick(response))
    features.append(forwarding(response))
    # features.append(page_rank(url))
    features.append(1)
    features.append(google_index(url))
    # consumming lot of time
    features.append(links_to_page(url))
    # features.append(popup(url))
    # features.append(label)
    print("done html and js")

    return features


# phishurl = (input("Enter the URL : "))

"""### **4.2. Phishing URLs:**

Now, feature extraction is performed on phishing URLs.
"""


def Predict(data):
    loaded_model = joblib.load(
        'model\ensemble_model.joblib')
    y = loaded_model.predict(data)
    return (y)


def extract(phishurl):

    # Extracting the feautres & storing them in a list
    phish_features = []
    for i in range(1):
        url = phishurl
        # print(i, end=" ")
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

    y = Predict(phishing)
    if y[0] == 1:
        y = "Phishing Website"
    else:
        y = "Legistimate Website"

    return (y)


url = input("Enter the url")
print(extract(url))
