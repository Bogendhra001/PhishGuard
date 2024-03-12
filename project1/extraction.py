import pandas as pd
from urllib.parse import urlparse, urlencode
import ipaddress
import asyncio
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
import multiprocessing
import time



class Features:

    def __init__(self, url):
        self.url = url
        self.address = []
        self.domian = []
        self.https = []
    # async def async_method(self):
    #     print("Async method starts")
    #     await asyncio.sleep(4)

    def get_address(self, queue):
        # print("address")
        dns = 0
        try:
            domain_name = whois.whois(urlparse(self.url).netloc)
        except:
            dns = 1
        features = []
        # features.append(getDomain(self.url))
        features.append(havingIP(self.url))
        features.append(getLength(self.url))
        features.append(tinyURL(self.url))
        # features.append(getDepth(self.url))
        features.append(haveAtSign(self.url))
        features.append(redirection(self.url))
        features.append(prefixSuffix(self.url))
        features.append(sub_domain(self.url))
        # this feature is giving the error that http socket is not present that comsumming lot of time
        # features.append(https(self.url))
        features.append(1)
        features.append(
            1 if dns == 1 else domainRegistrationLength(domain_name))
        features.append(favicon(self.url))
        features.append(Port(self.url))
        features.append(httpDomain(self.url))
        queue.put(features)

    def get_domain(self, queue):
        # print("dns")
        # Domain based features (4)
        features = []
        dns = 0
        try:
            domain_name = whois.whois(urlparse(self.url).netloc)
        except:
            dns = 1
        features.append(1 if dns == 1 else AgeofDomain(domain_name))
        features.append(dns)
        features.append(Web_traffic(self.url))
        features.append(google_index(self.url))
        # # features.append(page_rank(self.url))
        # features.append(1)

        # consumming lot of time
        features.append(links_to_page(self.url))

        queue.put(features)

    def get_http(self, queue):
        # print("https")
        features = []
        try:
            response = requests.get(self.url)
        except:
            response = ""
        features.append(request_url(self.url))
        features.append(anchor_url(self.url))
        features.append(links_in_tags(self.url))
        features.append(sfh(self.url))
        features.append(email_submission(self.url))
        features.append(hostname(self.url))
        features.append(forwarding(response))
        features.append(mouseOver(response))
        features.append(rightClick(response))
        features.append(iframe(response))

        # features.append(popup(self.url))
        # features.append(label)
        queue.put(features)

    def Predict(self, data):
        loaded_model = joblib.load(
            'model/ensemble_model_updated.joblib')
        y = loaded_model.predict(data)
        return (y)

    def extract(self):
        queue = multiprocessing.Queue()
        processes = []

        p1 = multiprocessing.Process(target=self.get_address, args=(queue,))
        p2 = multiprocessing.Process(target=self.get_domain, args=(queue,))
        p3 = multiprocessing.Process(target=self.get_http, args=(queue,))

        processes.extend([p1, p3, p2])

        for p in processes:
            p.start()
        # await self.async_method()
        time.sleep(5)  
        for p in processes:
            p.join()

        while not queue.empty():
            feature = queue.get()
            if feature:
                if len(feature) == 12:
                    self.address = feature
                elif len(feature) == 5:
                    self.domain = feature
                elif len(feature)==10:
                    self.https = feature

        # print("job is done")
        print(self.address ,"address")
        print(self.domain, "domain")
        print(self.https, "https")
        l = []
        l.extend(self.address)
        l.extend(self.https)
        l.extend(self.domain)

        # print(l)
        
        # Extracting the feautres & storing them in a list
        phish_features = [l]
        # converting the list to dataframe
        feature_names = ['UsingIP', 'LongURL', 'ShortURL', 'Symbol@', 'Redirecting//',
                         'PrefixSuffix-', 'SubDomains', 'HTTPS', 'DomainRegLen', 'Favicon',
                         'NonStdPort', 'HTTPSDomainURL', 'RequestURL', 'AnchorURL',
                         'LinksInScriptTags', 'ServerFormHandler', 'InfoEmail', 'AbnormalURL',
                         'WebsiteForwarding', 'StatusBarCust', 'DisableRightClick',
                         'IframeRedirection', 'AgeofDomain', 'DNSRecording', 'WebsiteTraffic',
                         'GoogleIndex', 'LinksPointingToPage']
        phishing = pd.DataFrame(phish_features, columns=feature_names)

        # print(phishing)
        y = self.Predict(phishing)
        if y[0] == 1:
            y = "Phishing Website"
        else:
            y = "Legistimate Website"

        return ([phishing,y])


if __name__ == "__main__":
    n = input("enter the url")
    ob = Features(n)
    print(ob.extract())


def main(url):
    ob = Features(url)
    result = ob.extract()
    print(result)
    return (result)
