from api.model.media_type import MediaType
from bot.adapters import ResultsAdapter
from bot.callbacks import SearchCallback, MarkupButtonCallback
from bot.utils import inline_query_util


class InlineResultsProvider(object):
    def __init__(self, movie_db_service):
        self._service = movie_db_service
        self._result_adapter = None

    def get_search_results(self, query, offset):
        results = []
        item_id = None
        media_type = None

        if len(query) == 0:
            return results
        if offset == 0:
            return results

        query_data = query.split('-')
        if len(query_data) > 2:
            item_id = query_data[2]
            media_type = query_data[1]

        if MarkupButtonCallback.VIDEOS.value in query:
            if MediaType.from_name(media_type) == MediaType.TV:
                results = inline_query_util.generate_inline_videos_results(
                    self._service.get_tv_shows_videos(item_id))
            else:
                results = inline_query_util.generate_inline_videos_results(self._service.get_movie_videos(item_id))

        elif MarkupButtonCallback.CAST.value in query:
            if MediaType.from_name(media_type) == MediaType.TV:
                cast_results = inline_query_util.inline_search_results(self._service.get_tv_credits(item_id))
            else:
                cast_results = inline_query_util.inline_search_results(self._service.get_movie_credits(item_id))

            if offset == 1:
                self._result_adapter = ResultsAdapter(cast_results)
                results = self._result_adapter.next_chunk()
            elif offset > 1:
                results = self._result_adapter.next_chunk()

        elif MarkupButtonCallback.RECOMMENDATIONS.value in query:
            if MediaType.from_name(media_type) == MediaType.TV:
                results = inline_query_util.inline_search_results(
                    self._service.get_tv_show_recommendations(tv_show_id=item_id, page=offset))
            else:
                results = inline_query_util.inline_search_results(
                    self._service.get_movie_recommendations(movie_id=item_id, page=offset))

        elif MarkupButtonCallback.ACTING.value in query:
            if offset == 1:
                cast_results = inline_query_util.inline_search_results(
                    self._service.get_combined_cast(person_id=query.split('-')[1]))
                self._result_adapter = ResultsAdapter(cast_results)
                results = self._result_adapter.next_chunk()
            elif offset > 1:
                results = self._result_adapter.next_chunk()

        elif SearchCallback.POPULAR_MOVIES.value == query:
            results = inline_query_util.inline_search_results(self._service.get_popular_movies(page=offset))

        elif SearchCallback.TV_ON_THE_AIR.value == query:
            results = inline_query_util.inline_search_results(self._service.get_tv_on_the_air(page=offset))

        elif SearchCallback.POPULAR_TV_SHOWS.value == query:
            results = inline_query_util.inline_search_results(self._service.get_popular_tv_shows(page=offset))

        elif SearchCallback.POPULAR_PEOPLE.value == query:
            results = inline_query_util.inline_search_results(self._service.get_popular_people(page=offset))

        elif SearchCallback.TOP_RATED_MOVIES.value == query:
            results = inline_query_util.inline_search_results(self._service.get_top_rated_movies(page=offset))

        elif SearchCallback.TOP_RATED_TV_SHOWS.value == query:
            results = inline_query_util.inline_search_results(self._service.get_top_rated_tv_shows(page=offset))

        elif SearchCallback.MOVIES_IN_THEATERS.value == query:
            results = inline_query_util.inline_search_results(self._service.get_movies_in_theatres(page=offset))

        else:
            results = inline_query_util.inline_search_results(self._service.multi_search(query=query, page=offset))

        if results is None:
            results = []

        return results
