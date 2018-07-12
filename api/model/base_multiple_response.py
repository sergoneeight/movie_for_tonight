from abc import ABC, abstractmethod


class BaseMultipleResponse(ABC):
    """Abstract class represents base multiple results response from API"""

    @abstractmethod
    def __init__(self, response_dict):
        self.results = response_dict['results']
        self.total_pages = response_dict['total_pages']
        self.page = response_dict['page']
        self.total_results = response_dict['total_results']
