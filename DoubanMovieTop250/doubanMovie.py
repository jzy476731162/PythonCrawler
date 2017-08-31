# import requests
#
# DOWNLOAD_URL = 'http://movie.douban.com/top250'
#
# from bs4 import BeautifulSoup
# import codecs
#
# def parse_html(html):
#     soup = BeautifulSoup(html)
#     movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
#
#     movie_name_list = []
#
#     for movie_li in movie_list_soup.find_all('li'):
#         detail = movie_li.find('div', attrs={'class': 'hd'})
#         movie_name = detail.find('span', attrs={'class':'title'}).getText()
#
#         movie_name_list.append(movie_name)
#     next_page = soup.find('span', attrs={'class':'next'}).find('a')
#     if next_page:
#         return movie_name_list, DOWNLOAD_URL + next_page['href']
#     return movie_name_list, None
#
# def download_page(url):
#     data = requests.get(url).content
#     return data
#
# def main():
#     url = DOWNLOAD_URL
#
#     with codecs.open('movies', 'wb', encoding='utf-8') as fp:
#         while url:
#             html = download_page(url)
#             movies, url = parse_html(html)
#             fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))
#
# if __name__ =='__main__':
#     main()
#
#


import requests

from bs4 import BeautifulSoup
import codecs

DOWNLOAD_URL = 'https://movie.douban.com/top250'

def downLoad_page(url):
    response = requests.get(url)
    data = response.content
    headers = response.headers
    print(headers)

    return data

def parse_html(html):
    soup = BeautifulSoup(html)
    movie_list_soup = soup.find('ol', attrs={'class':'grid_view'})
    movie_name_list = []


    for movie_soup in movie_list_soup.find_all('li'):
        detail = movie_soup.find('div', attrs= {'class':'hd'})
        movie_name = detail.find('span', attrs= {'class':'title'}).getText()

        bd = movie_soup.find('div', attrs= {'class':'bd'})
        movie_director = bd.find('p').getText()
        star = bd.find('div', attrs={'class':'star'}).find('span', attrs={'class':'rating_num'}).getText()


        comment = bd.find('p', attrs={'class':'quote'})
        if comment:
            comment = comment.find('span', attrs={'class': 'ing'})

        if comment:
            comment = comment.getText()
        else:
            comment = ''

        movie_name_list.append({'name':movie_name,'director':movie_director, 'star': star, 'comment':comment})

    next_page = soup.find('span', attrs={'class':'next'}).find('a')
    if next_page:
        return movie_name_list,DOWNLOAD_URL + next_page['href']
    return movie_name_list, None

def main():
    url = DOWNLOAD_URL

    with codecs.open('moview1', 'wb', encoding='UTF-8') as fp:
        while url:
            html = downLoad_page(url)
            movies, url = parse_html(html)
            for row in movies:
                str = "%s - %s - %s - %s\n" % (row['name'],row['director'],row['star'],row['comment'])
                fp.write(str)



if __name__ == '__main__':
    main()