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
