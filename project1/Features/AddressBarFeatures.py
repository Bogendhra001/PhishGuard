def getDomain(url):
    domain = urlparse(url).netloc
    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")
    return domain


def havingIP(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0
    return ip


def haveAtSign(url):
    if "@" in url:
        at = 1
    else:
        at = 0
    return at


def getLength(url):
    if len(url) < 54:
        length = 0
    else:
        length = 1
    return length


# 5.Gives number of '/' in URL (URL_Depth)
def getDepth(url):
    s = urlparse(url).path.split('/')
    depth = 0
    for j in range(len(s)):
        if len(s[j]) != 0:
            depth = depth+1
    return depth


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


# 7.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
def httpDomain(url):
    domain = urlparse(url).netloc
    if 'https' in domain:
        return 1
    else:
        return 0


# listing shortening services
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
    match = re.search(shortening_services, url)
    if match:
        return 1
    else:
        return 0


def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            # legitimate


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


def favicon(url):
    if is_favicon_external(url):
        return 1  # Phishing
    else:
        return 0  # Legitimate


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
            age_in_years = (datetime.now() -
                            certificate.not_valid_before).days // 365

            if url.startswith("https://") and issuer in TRUSTED_ISSUERS and age_in_years >= MIN_REPUTABLE_CERT_AGE:
                return -1
            elif url.startswith("https://") and issuer not in TRUSTED_ISSUERS:
                return 0

    except Exception as e:
        print(f"Error: {e}")

    return 1


def DomainRegistrationLength(domain_name):
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


"""#### **3.2.3. Age of Domain**

This feature can be extracted from WHOIS database. Most phishing websites live for a short period of time. The minimum age of the legitimate domain is considered to be 12 months for this project. Age here is nothing but different between creation and expiration time.

If age of domain > 12 months, the vlaue of this feature is 1 (phishing) else 0 (legitimate).
"""

# 13.Survival time of domain: The difference between termination time and creation time (Domain_Age)


def domainRegistrationLength(domain_name):
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date
    if (isinstance(creation_date, str) or isinstance(expiration_date, str)):
        try:
            creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if ((expiration_date is None) or (creation_date is None)):
        return 1
    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
        return 1
    else:
        ageofdomain = abs((expiration_date - creation_date).days)
        if ((ageofdomain/30) < 12):
            age = 1
        else:
            age = 0
    return age


def Port(url):
    preferred_ports = [80, 443]  # Preferred ports
    non_preferred_ports = [21, 22, 23, 445, 1433,
                           1521, 3306, 3389]  # Non-preferred ports

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
