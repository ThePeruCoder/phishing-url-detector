import re
from urllib.parse import urlparse
import math

#Returns total characters in the URL
def url_length(url):
    return len(str(url)) if url else 0

#Counts dots
def num_dots(url):
    return str(url).count('.')

#Check for "@" symbol
def has_at_symbol(url):
    return 1 if '@' in str(url) else 0

#Detects redirection 
def has_double_slash_redirect(url):
    # After http(s):// 
    url_str=str(url)
    if url_str.startswith(('http://','https://')):
        return 1 if '//' in url_str[7:] else 0
    return 1 if '//' in url_str[7:] else 0

#Check if URL starts with https 
def has_https(url):
    return 1 if str(url).startswith('https') else 0


def has_ip_address(url):
    #regex to detect IP like 192.168.1.1
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    return 1 if re.search(ip_pattern, str(url)) else 0

def num_subdomains(url):
    #count dots in domain part
    domain = urlparse(str(url)).netloc
    return domain.count('.') if domain else 0

def is_shortened_url(url):
    #check for bit.ly, tinyurl, t.co, goo.gl, etc.
    shortened = ['bit.ly', 'tinyurl', 't.co', 'goo.gl', 'ow.ly', 'is.gd','buff.ly','rebrand.ly','shorturl.at']
    url_str=str(url).lower()
    return 1 if any(s in url_str for s in shortened) else 0

def count_suspicious_words(url):
    #count words like login, bank, secure, account, update, etc.
    suspicious = ['login', 'bank', 'secure', 'account', 'update', 'verify', 'paypal', 'ebay','password','amazon','apple','microsoft','confirm','wallet','crypto','support']
    url_str=str(url).lower()
    return sum(1 for word in suspicious if word in url_str)

def domain_length(url):
    #Returns length of domain
    domain = urlparse(str(url)).netloc
    return len(domain) if domain else 0

def num_special_chars(url):
    #Counts no. of special characters in URL
    url_str=str(url)
    special = re.findall(r'[-_?=%#&]', url_str)
    return len(special)

def url_entropy(url):
    #Shannon entropy 
    #Higher the value of shannon entropy, it mathematically proves that the URL lacks predictable structure
    url_str=str(url)
    if not url_str:
        return 0
    freq = {}
    for char in url_str:
        freq[char] = freq.get(char, 0) + 1
    entropy = 0
    length=len(url_str)
    for count in freq.values():
        p = count / len(url)
        entropy -= p * math.log2(p)
    return round(entropy, 4)

# Main function
def extract_features(url):
    features = {
        'url_length': url_length(url),
        'num_dots': num_dots(url),
        'has_at': has_at_symbol(url),
        'has_double_slash': has_double_slash_redirect(url),
        'has_https': has_https(url),
        'has_ip': has_ip_address(url),
        'num_subdomains': num_subdomains(url),
        'is_shortened': is_shortened_url(url),
        'suspicious_words': count_suspicious_words(url),
        'domain_length': domain_length(url),
        'num_special_chars': num_special_chars(url),
        'url_entropy': url_entropy(url)
    }
    return features