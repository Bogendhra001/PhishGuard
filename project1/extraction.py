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
import multiprocessing


class Features:

    def __init__(self, url):
        self.url = url
        self.address = []
        self.domian = []
        self.https = []

    def get_address(self, queue):
        # print("address")
        features = []
        features.append(getDomain(self.url))
        features.append(havingIP(self.url))
        features.append(haveAtSign(self.url))
        features.append(getLength(self.url))
        features.append(getDepth(self.url))
        features.append(redirection(self.url))
        features.append(httpDomain(self.url))
        features.append(tinyURL(self.url))
        features.append(prefixSuffix(self.url))
        features.append(request_url(self.url))
        features.append(anchor_url(self.url))
        features.append(links_in_tags(self.url))
        features.append(sfh(self.url))
        features.append(email_submission(self.url))
        features.append(hostname(self.url))
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

        features.append(dns)
        features.append(Web_traffic(self.url))
        features.append(favicon(self.url))
        features.append(sub_domain(self.url))

        # this feature is giving the error that http socket is not present that comsumming lot of time
        # features.append(https(self.url))
        features.append(1)

        features.append(
            1 if dns == 1 else domainRegistrationLength(domain_name))
        features.append(1 if dns == 1 else AgeofDomain(domain_name))
        features.append(Port(self.url))
        queue.put(features)

    def get_http(self, queue):
        # print("https")
        features = []
        try:
            response = requests.get(self.url)
        except:
            response = ""
        features.append(iframe(response))
        features.append(mouseOver(response))
        features.append(rightClick(response))
        features.append(forwarding(response))
        # features.append(page_rank(self.url))
        features.append(1)
        features.append(google_index(self.url))
        # consumming lot of time
        features.append(links_to_page(self.url))
        # features.append(popup(self.url))
        # features.append(label)
        queue.put(features)

    def Predict(self, data):
        loaded_model = joblib.load(
            'model\ensemble_model.joblib')
        y = loaded_model.predict(data)
        return (y)

    # def extract(self):
    #     l = self.address + self.Domian + self.https
    #     # Extracting the features & storing them in a list
    #     print(l)
    #     # phish_features = [l]
    #     # # converting the list to dataframe
    #     # feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
    #     #                 'https_Domain', 'TinyURL', 'Prefix/Suffix', 'request_url', 'Anchor_url', 'Links_in_tags', 'sfh', 'email_submission', 'hostname', 'DNS_Record', 'Web_Traffic', 'Favilon', 'Sub_domain', 'https',
    #     #                 'Domain_Age', 'Domain_End', 'Port', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards', 'Page_rank', 'google_index', 'Links_to_pages']
    #     # phishing = pd.DataFrame(phish_features, columns=feature_names)

    #     # phishing = phishing.drop('Domain', axis=1)
    #     # phishing = phishing.drop('Have_At', axis=1)
    #     # print(phishing)
    #     # y = self.Predict(phishing)
    #     # if y[0] == 1:
    #     #     y = "Phishing Website"
    #     # else:
    #     #     y = "Legistimate Website"

    #     return ("done")

    # def extract(self):
        # l = self.address+self.Domian+self.https
        # # Extracting the feautres & storing them in a list
        # phish_features = [l]
        # # converting the list to dataframe
        # feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
        #                  'https_Domain', 'TinyURL', 'Prefix/Suffix', 'request_url', 'Anchor_url', 'Links_in_tags', 'sfh', 'email_submission', 'hostname', 'DNS_Record', 'Web_Traffic', 'Favilon', 'Sub_domain', 'https',
        #                  'Domain_Age', 'Domain_End', 'Port', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards', 'Page_rank', 'google_index', 'Links_to_pages']
        # phishing = pd.DataFrame(phish_features, columns=feature_names)

        # phishing = phishing.drop('Domain', axis=1)
        # phishing = phishing.drop('Have_At', axis=1)
        # print(phishing)
        # # y = self.Predict(phishing)
        # # if y[0] == 1:
        # #     y = "Phishing Website"
        # # else:
        # #     y = "Legistimate Website"

        # return ("done")


# if __name__ == "__main__":
#     n = input("enter the url")
#     ob = Features(n)
#     process1 = multiprocessing.Process(target=ob.get_address)
#     process1.start()
#     process2 = multiprocessing.Process(target=ob.get_domain)
#     process2.start()
#     process3 = multiprocessing.Process(target=ob.get_http)
#     process3.start()
#     # Start processes

#     # Wait for processes to finish
#     # print(ob.abnormal)
#     # print(ob.Domian)
#     # print(ob.address)
#     process1.join()
#     process2.join()
#     process3.join()
#     print("job is done")
#     print(ob.extract())


    def extract(self):
        queue = multiprocessing.Queue()
        processes = []

        p1 = multiprocessing.Process(target=self.get_address, args=(queue,))
        p2 = multiprocessing.Process(target=self.get_domain, args=(queue,))
        p3 = multiprocessing.Process(target=self.get_http, args=(queue,))

        processes.extend([p1, p2, p3])

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        while not queue.empty():
            feature = queue.get()
            if feature:
                if len(feature) == 15:
                    self.address = feature
                elif len(feature) == 8:
                    self.domain = feature
                else:
                    self.https = feature

        # print("job is done")
        # print(self.address)
        # print(self.domain)
        # print(self.https)
        l = []
        l.extend(self.address)
        l.extend(self.domain)
        l.extend(self.https)
        # print(l)
        # print(len(l) == 30)
        # Extracting the feautres & storing them in a list
        phish_features = [l]
        # converting the list to dataframe
        feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
                         'https_Domain', 'TinyURL', 'Prefix/Suffix', 'request_url', 'Anchor_url', 'Links_in_tags', 'sfh', 'email_submission', 'hostname', 'DNS_Record', 'Web_Traffic', 'Favilon', 'Sub_domain', 'https',
                         'Domain_Age', 'Domain_End', 'Port', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards', 'Page_rank', 'google_index', 'Links_to_pages']
        phishing = pd.DataFrame(phish_features, columns=feature_names)

        phishing = phishing.drop('Domain', axis=1)
        phishing = phishing.drop('Have_At', axis=1)
        # print(phishing)
        y = self.Predict(phishing)
        if y[0] == 1:
            y = "Phishing Website"
        else:
            y = "Legistimate Website"

        return (y)


if __name__ == "__main__":
    n = input("enter the url")
    ob = Features(n)
    print(ob.extract())


def main(url):
    ob = Features(url)
    result = ob.extract()
    print(result)
    return (result)
