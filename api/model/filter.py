class DiscoverMoviesFilter(object):
    DEFAULT_MAX_PAGES_FOR_RANDOM_CHOICE = 100
    DEFAULT_MIN_RELEASE_YEAR = 2000
    DEFAULT_MIN_VOTE_COUNT = 100
    DEFAULT_MIN_VOTE_AVERAGE = 6

    def __init__(self,
                 page=1,
                 min_release_year=DEFAULT_MIN_RELEASE_YEAR,
                 min_vote_average=DEFAULT_MIN_VOTE_AVERAGE,
                 min_vote_count=DEFAULT_MIN_VOTE_COUNT):
        self.filter = {'region': 'US',
                       'sort_by': 'vote_count.desc',
                       'page': page,
                       'release_date.gte': min_release_year,
                       'vote_average.gte': min_vote_average,
                       'without_genres': '99,10402,10749,10770',
                       'vote_count.gte': min_vote_count,
                       'primary_release_date.gte': min_release_year}
