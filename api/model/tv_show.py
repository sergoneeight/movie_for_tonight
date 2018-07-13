from api.model.base_multiple_response import BaseMultipleResponse
from api.model.genres import Genre
from api.model.image import Image


class TVShowsResponse(BaseMultipleResponse):
    def __init__(self, response_dict):
        super().__init__(response_dict)

    def get_tv_shows(self):
        tv_shows = []
        for item in self.results:
            tv_show = TVShow(item)
            tv_shows.append(tv_show)
        return tv_shows


class TVShow(object):
    def __init__(self, response_dict):
        self.id = response_dict['id']
        self.name = response_dict['name']
        self.overview = response_dict['overview']
        self.vote_average = response_dict['vote_average']
        self.vote_count = response_dict['vote_count']
        self.first_air_date = response_dict['first_air_date']
        self._poster_path = response_dict['poster_path']
        self._backdrop_path = response_dict['backdrop_path']
        self._genre_ids = response_dict['genre_ids']

    @property
    def genres(self):
        return [Genre.title(genre_id) for genre_id in self._genre_ids]

    @property
    def poster_url(self):
        return Image.BASE_URL + Image.PosterSize.MEDIUM.value + self._poster_path

    @property
    def backdrop_url(self):
        return Image.BASE_URL + Image.BackdropSize.MEDIUM.value + self._backdrop_path
