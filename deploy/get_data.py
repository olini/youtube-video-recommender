import requests as rq
import bs4 as bs4
import re
import time

def download_search_page(keyword, page):
    url = 'https://www.youtube.com/results?search_query={query}&sp=CAI%253D&p={page}'.format(query=keyword, page=page)
    response = rq.get(url)
    
    return response.text

def parse_search_page(page_html):
    video_list = []
    
    parsed = bs4.BeautifulSoup(page_html, features="html.parser")
    tags = parsed.findAll('a')
    for tag in tags:
        if tag.has_attr('aria-describedby'):
            link = tag['href']
            title = tag['title']
            data = {'link': link, 'title': title}
            video_list.append(data)
    
    return video_list

def download_video_page(link):
    url = 'https://www.youtube.com{}'.format(link)
    response = rq.get(url)
    
    return response.text

def parse_video_page(page_html):
    parsed = bs4.BeautifulSoup(page_html, features="html.parser")
    
    class_watch = parsed.find_all(attrs={'class':re.compile(r'watch')})
    id_watch = parsed.find_all(attrs={'id':re.compile(r'watch')})
    channel = parsed.find_all('a', attrs={'href':re.compile(r'channel')})
    meta = parsed.find_all('meta')
    
    data = dict()
    
    for occurrence in class_watch:
        colname = '_'.join(occurrence['class'])
        if 'clearfix' in colname:
            continue
        data[colname] = occurrence.text.strip()
        
    for occurrence in id_watch:
        colname = occurrence['id']
        data[colname] = occurrence.text.strip()
        
    for occurrence in meta:
        colname = occurrence.get('property')
        if colname is not None:
            data[colname] = occurrence['content']
            
    for link_num, occurrence in enumerate(channel):
        data['channel_link_{}'.format(link_num)] = occurrence['href']
        
    return data