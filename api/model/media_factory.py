from api.model.media_type import MediaType
from api.model.movie import Movie
from api.model.person import Person
from api.model.tv_show import TVShow


class MediaTypeFactory(object):

    @staticmethod
    def instance(response_dict, media_type=None):
        if media_type == MediaType.MOVIE:
            return Movie(response_dict)
        elif media_type == MediaType.TV_SHOW:
            return TVShow(response_dict)
        elif media_type == MediaType.PERSON:
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
