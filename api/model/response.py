from api.model.image import Image
from api.model.media_factory import MediaTypeFactory
from api.model.media_type import MediaType
from api.model.video import Video


class PagedResponse(object):

    def __init__(self, response_dict, media_type=None):
        self._results = response_dict['results']
        self.total_pages = response_dict['total_pages']
        self.page = response_dict['page']
        self.total_results = response_dict['total_results']
        self.media_type = media_type

    @property
    def results(self):
        results = []
        for item in self._results:
            item = MediaTypeFactory.instance(response_dict=item, media_type=self.media_type)
            results.append(item)
        return results


class CreditsResponse(object):
    def __init__(self, response_dict, default_media_type=None):
        self._cast_results = response_dict['cast']
        self._crew_results = response_dict['crew']
        self._default_media_type = default_media_type

    @property
    def cast(self):
        results = []
        for item in self._cast_results:
            item = MediaTypeFactory.instance(response_dict=item, media_type=self._default_media_type)
            results.append(item)
        return results

    @property
    def crew(self):
        results = []
        for item in self._crew_results:
            item = MediaTypeFactory.instance(response_dict=item, media_type=self._default_media_type)
            results.append(item)
        return results


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


class ProfileImagesResponse(object):
    def __init__(self, response_dict):
        self._profiles = response_dict['profiles']

    @property
    def images(self):
        results = []
        for item in self._profiles:
            image = Image(item)
            results.append(image)
        return results
