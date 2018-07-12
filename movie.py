class MoviesResponse(object):
    def __init__(self, dictionary):
        self._dict = dictionary

    def get_movies(self):
        movies = []
        for item in self._dict['results']:
            movie = Movie(item)
            movies.append(movie)
        return movies


class Movie(object):
    IMAGE_BASE_URL = 'http://image.tmdb.org/t/p/w500/'
    base = 'https://www.themoviedb.org/movie/'

    def __init__(self, dictionary):
        self.id = dictionary['id']
        self.title = dictionary['title']
        self.vote_average = dictionary['vote_average']
        self.__poster_path = dictionary['poster_path']
        self.overview = dictionary['overview']
        self.__release_date = dictionary['release_date']

    @property
    def poster_url(self):
        return '{base_url}{poster_path}'.format(base_url=self.IMAGE_BASE_URL, poster_path=self.__poster_path)

    @property
    def page_url(self):
        return self.l + str(self.id)

    @property
    def release_year(self):
        return self.__release_date.split('-')[0]
