from telebot.types import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultVideo

from api.model.media_type import MediaType
from bot.utils import markup_util


def generate_inline_search_results(search_results):
    results = []
    if search_results:
        for item_num, search_item in enumerate(search_results):
            if search_item.media_type == MediaType.PERSON.value:
                replay_markup = markup_util.get_person_inline_search_result_markup(search_item)
            else:
                replay_markup = markup_util.get_inline_search_result_markup(search_item)

            item = InlineQueryResultArticle(
                id=item_num,
                title=search_item.formatted_title,
                description=search_item.description,
                reply_markup=replay_markup,
                input_message_content=InputTextMessageContent(
                    message_text=search_item.caption,
                    parse_mode='HTML'
                ),
                thumb_url=search_item.poster_url
            )
            results.append(item)
    return results


def generate_inline_videos_results(search_results):
    results = []
    for item_num, search_item in enumerate(search_results):
        # item = InlineQueryResultVideo(id=item_num, video_url=search_item.url, title=search_item.name, mime_type='video/mp4',
        #                               thumb_url=search_item.thumbnail,
        #                               input_message_content=InputTextMessageContent(
        #                                   message_text='<b>{title}</b><a href="{url}">&#160</a>'.format(title=search_item.name,
        #                                                                                                 url=search_item.url),
        #                                   parse_mode='HTML'
        #                               ))
        item = InlineQueryResultArticle(
            id=item_num,
            title=search_item.name,
            input_message_content=InputTextMessageContent(
                message_text='<b>{title}</b><a href="{url}">&#160</a>'.format(title=search_item.name, url=search_item.url),
                parse_mode='HTML'
            ),
            thumb_url=search_item.thumbnail
        )
        results.append(item)
    return results
