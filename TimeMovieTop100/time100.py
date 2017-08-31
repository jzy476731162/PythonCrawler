import requests
from bs4 import BeautifulSoup
import codecs

DOWNLOAD_URL = 'http://www.mtime.com/top/movie/top100/'
DOWNLOAD_URL1 = 'http://www.mtime.com/top/movie/top100_chinese/'
DOWNLOAD_URL2 = 'http://www.mtime.com/top/movie/top100_japan/'
DOWNLOAD_URL3 = 'http://www.mtime.com/top/movie/top100_south_korea/'
DOWNLOAD_URL4 = 'http://www.mtime.com/top/movie/top100_hot_top10/'

def download_url(url):
    data = requests.get(url).content
    return data

def parse_html(html, index, baseURL):
    soup = BeautifulSoup(html)

    movie_list = []

    container = soup.find('div', attrs={'class':'top_list'})
    for movie_soup in container.find_all('li'):
        movie_detail = movie_soup.find('div', attrs={'class':'mov_con'})
        title = movie_detail.find('h2',attrs={'class':"px14 pb6"}).find('a').getText()
        if not title:
            title = ''

        desc = movie_detail.find('p', attrs={'class':'mt3'})
        if desc:
            desc = desc.getText()
        if not desc:
            desc = ''

        movie_list.append({'title':title, 'desc':desc})
    if index <= 10:
        nextPage = baseURL + 'index-%d' % (index + 1) + '.html'
        # print(nextPage)
    return movie_list, nextPage, index + 1


def main():
    for url in [DOWNLOAD_URL, DOWNLOAD_URL1, DOWNLOAD_URL2, DOWNLOAD_URL3]:
        tempUrl = url
        index = 1
        fileName = 'time' + url.rsplit('/')[-2] + '.txt'
        print(fileName)
        with codecs.open(fileName, 'wb', encoding='UTF-8') as pf:
            pf.write(tempUrl + '\n')
            while index <= 10:
                html = download_url(tempUrl)
                movies, tempUrl, index = parse_html(html, index, url)
                print(tempUrl)
                for movie in movies:
                    str = "%s --- %s\n" % (movie['title'], movie['desc'])
                    pf.write(str)

if __name__ == '__main__':
    main()