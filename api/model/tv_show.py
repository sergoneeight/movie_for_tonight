from api.model.base_multiple_response import BaseMultipleResponse


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
        self._poster_path = response_dict['poster_path']
