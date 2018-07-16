from enum import Enum


class Genre(Enum):
    ACTION = 28
    ADVENTURE = 12
    ANIMATION = 16
    COMEDY = 35
    CRIME = 80
    DOCUMENTARY = 99
    DRAMA = 18
    FAMILY = 10751
    FANTASY = 14
    HISTORY = 36
    HORROR = 27
    MUSIC = 10402
    MYSTERY = 9648
    ROMANCE = 10749
    SCIENCE_FICTION = 878
    TV_MOVIE = 10770
    THRILLER = 53
    WAR = 10752
    WESTERN = 37

    @classmethod
    def title(cls, genre_id):
        genre = Genre(genre_id).name
        splitted = genre.split('_')
        if len(splitted) == 2:
            return splitted[0].capitalize() + ' ' + splitted[1].capitalize()
        return genre.capitalize()
