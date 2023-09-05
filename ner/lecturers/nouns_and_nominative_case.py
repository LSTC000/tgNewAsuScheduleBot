from typing import Union

import pymorphy3


def nouns_and_nominative_case(text: str) -> Union[str, None]:
    '''
    :param text: Some text.
        Example: 'найди мне козлова дениса юрьевича'.
    :return:
    Str - Nouns in the text.
        Example: 'козлова дениса юрьевича', 'masc'.
    None - If there are no nouns in the text.
    '''

    morph = pymorphy3.MorphAnalyzer()

    nouns_list = []

    for word in text.split():
        morph_word = morph.parse(word)[0]
        if 'NOUN' in morph_word.tag.POS:
            gender = morph_word.tag.gender

            if gender == 'masc':
                if word[-1] == 'в':
                    nouns_list.append(word)
                else:
                    nouns_list.append(morph_word.inflect({'nomn'}).word)

            if gender == 'femn':
                if word[-1] == 'a':
                    nouns_list.append(word)
                else:
                    nouns_list.append(morph_word.inflect({'nomn'}).word)

    return ' '.join(nouns_list) if len(nouns_list) else None
