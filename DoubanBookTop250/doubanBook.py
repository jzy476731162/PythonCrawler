import requests

from bs4 import BeautifulSoup
import codecs

DOWNLOAD_URL = 'https://book.douban.com/top250'

def download_url(url):
    data = requests.get(url).content

    return data

def parse_html(html):
    soup = BeautifulSoup(html)

    book_list =[]
    content = soup.find('div', attrs={'class':'article'})
    for book_soup in content.find_all('table'):
        title = book_soup.find('tr', attrs={'class':'item'}).find('div', attrs={'class':'pl2'}).find('a').getText()
        title = title.strip()
        title = title.replace('\n', '')
        book_list.append(title)

    nextPage = content.find('span', attrs= {'class':'next'}).find('a')
    if nextPage:
        return book_list, nextPage['href']
    return book_list, None

def main():

    url = DOWNLOAD_URL

    with codecs.open('bookRank.txt', 'wb', encoding='UTF-8') as fp:
        while url:
            html = download_url(url)
            books, url = parse_html(html)
            fp.write(u'{books}\n'.format(books='\n'.join(books)))


if __name__ == '__main__':
    main()