from telebot.types import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto

from api.model.media_type import MediaType
from bot.utils import markup_util


def inline_search_results(search_results):
    results = []
    if search_results:
        for item_num, search_item in enumerate(search_results):

            if search_item.media_type == MediaType.PERSON:
                replay_markup = markup_util.get_person_inline_search_result_markup(search_item)
            else:
                replay_markup = markup_util.get_inline_general_search_result_markup(search_item)

            item = InlineQueryResultArticle(
                id=search_item.id,
                title=search_item.shorten_title,
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
        item = InlineQueryResultArticle(
            id=item_num,
            title=search_item.name,
            description=search_item.type,
            input_message_content=InputTextMessageContent(
                message_text=search_item.caption,
                parse_mode='HTML'
            ),
            thumb_url=search_item.thumbnail
        )
        results.append(item)
    return results


def generate_inline_images_results(images_results):
    results = []
    for item_num, image in enumerate(images_results):
        item = InlineQueryResultPhoto(
            id=item_num,
            photo_url=image.url,
            thumb_url=image.url
        )
        results.append(item)
    return results
