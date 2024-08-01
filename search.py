from bs4 import BeautifulSoup
import requests

def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except:
        return ""

def get_all_links(page):
    soup = BeautifulSoup(page, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            links.append(href)
    return links

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword]=[url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def add_page_to_index(index, url, content):
    if content:
        keywords = content.split()
        for keyword in keywords:
            add_to_index(index, keyword, url)

def lucky_search(index,ranks,keyword):
    pages = lookup(index,keyword)
    if not pages:
        return None
    best_page=pages[0]
    for candidate in pages:
        if ranks[candidate]>ranks[best_page]:
            best_page=candidate
    return best_page


def hash_string(keyword, buckets):
    h = 0
    for c in keyword:
        h = (h * 31 + ord(c)) % buckets
    return h

def make_hashtable(buckets):
    table = []
    for i in range(buckets):
        table.append([])
    return table

def hashtable_get_bucket(htable, key):
    return htable[hash_string(key, len(htable))]

def hashtable_add(htable, key, value):
    bucket = hashtable_get_bucket(htable, key)
    bucket.append([key, value])

def hashtable_lookup(htable, key):
    bucket = hashtable_get_bucket(htable, key)
    for entry in bucket:
        if entry[0] == key:
            return entry[1]
    return None
