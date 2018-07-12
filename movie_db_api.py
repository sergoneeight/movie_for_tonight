from pprint import pprint

import requests

from movie import MoviesResponse

API_KEY = ''
BASE_URL = 'https://api.themoviedb.org/3/'
ENDPOINT = '{base_url}discover/movie?api_key={api_key}&sort_by=popularity.desc&page=1'.format(base_url=BASE_URL,
                                                                                              api_key=API_KEY)
poster_url = 'http://image.tmdb.org/t/p/w500/c9XxwwhPHdaImA2f1WEfEsbhaFB.jpg'
IMAGE_BASE_URL = 'http://image.tmdb.org/t/p/w500/'


def main():
    res = get_popular_movies()
    print(len(res.get_movies()))
    print(res.get_movies()[1].title)
    print(res.get_movies()[2].overview)
    print(res.get_movies()[3].release_date)
    print(res.get_movies()[4].vote_average)
    print(res.get_movies()[5].poster_url)


def get_popular_movies():
    response = requests.get('').json()
    return MoviesResponse(response)


if __name__ == '__main__':
    main()
