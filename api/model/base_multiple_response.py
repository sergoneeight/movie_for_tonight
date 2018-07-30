from enum import Enum

from api.model.media_type import MediaType
from api.model.movie import Movie
from api.model.person import Person
from api.model.tv_show import TVShow
from api.model.video import Video


class MultipleResponse(object):

    def __init__(self, response_dict, response_type):
        self._results = response_dict['results']
        self.total_pages = response_dict['total_pages']
        self.page = response_dict['page']
        self.total_results = response_dict['total_results']
        self.response_type = response_type

    @property
    def results(self):
        results = []
        for item in self._results:
            item = self.__create_specific_media_type_object(item)
            results.append(item)
        return results

    def __create_specific_media_type_object(self, response_dict):
        if self.response_type == ResponseType.MOVIE:
            return Movie(response_dict)
        elif self.response_type == ResponseType.TV_SHOW:
            return TVShow(response_dict)
        elif self.response_type == ResponseType.PERSON:
            return Person(response_dict)
        else:
            if 'media_type' in response_dict:
                item_media_type = response_dict['media_type']
                if item_media_type == MediaType.MOVIE.value:
                    return Movie(response_dict)
                elif item_media_type == MediaType.TV_SHOW.value:
                    return TVShow(response_dict)
                elif item_media_type == MediaType.PERSON.value:
                    return Person(response_dict)


class VideosResponse(object):
    def __init__(self, response_dict):
        self.id = response_dict['id']
        self._results = response_dict['results']

    @property
    def videos(self):
        results = []
        for item in self._results:
            item = Video(item)
            results.append(item)
        return results


class ResponseType(Enum):
    MOVIE = 'movie'
    TV_SHOW = 'tv'
    PERSON = 'person'
    MULTI_SEARCH = 'multi_search'
