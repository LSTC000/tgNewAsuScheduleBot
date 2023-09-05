import difflib

from typing import Union

import json

from loader import voice_cache

from ner.lecturers.nouns_and_nominative_case import nouns_and_nominative_case
from ner.lecturers.first_letter_upper_case import first_letter_upper_case
from ner.lecturers.processing_lecturer_name import processing_lecturer_name

from natasha import (
    Segmenter,
    MorphVocab,
    PER,
    NamesExtractor,
    NewsNERTagger,
    NewsEmbedding,
    Doc
)


async def find_lecturer_in_text(text: str, only_last_name: bool) -> Union[None, str]:
    """
    :param text: The user voice request converted to text.
        Example: 'найди мне козлова дениса юрьевича'.
    :param only_last_name: If True then we find the most similar lecturer from the LECTURERS_NAMES, else we follow
        the algorithm for searching for the lecturer last name, first name and patronymic.
    :return:
    Str - The correct name of the lecturer for the request.
        Example: 'Козлов Д.Ю.'.
    None - If the user did not enter the lecturer last name.
    """

    key_cache = text

    # Checking for a request in the voice_cache.
    if key_cache in voice_cache:
        return voice_cache[key_cache]

    with open('lecturers_names.json', 'r', encoding='utf-8') as file:
        lecturers_names = json.load(file)
        lecturers_names = lecturers_names['lecturers_names']

    if only_last_name:
        closest_match = difflib.get_close_matches(text, lecturers_names)

        if len(closest_match):
            last_name = closest_match[0].split()[0]
            voice_cache[key_cache] = last_name
            return last_name

        voice_cache[key_cache] = text
        return text

    # Translate the text into the nominative case.
    text = nouns_and_nominative_case(text=text)

    if text is None:
        voice_cache[key_cache] = None
        return None

    # Translate the text into the upper case.
    text = first_letter_upper_case(text=text)

    segmenter = Segmenter()
    morph_vocab = MorphVocab()

    emb = NewsEmbedding()
    ner_tagger = NewsNERTagger(emb)
    names_extractor = NamesExtractor(morph_vocab)

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_ner(ner_tagger)

    for span in doc.spans:
        span.normalize(morph_vocab)

    lecturer_name_keys = []

    for span in doc.spans:
        if span.type == PER:
            lecturer_name_keys.append(span.normal)
            span.extract_fact(names_extractor)
    # The keys in the fact_dict are the elements from the lecturer_name_keys.
    fact_dict = {_.normal: _.fact.as_dict for _ in doc.spans if _.fact}
    # The user can enter several lecturers but only the first one will be taken.
    if len(lecturer_name_keys):
        for key in lecturer_name_keys:
            if 'last' in fact_dict[key]:
                if 'first' in fact_dict[key]:
                    if 'middle' in fact_dict[key]:
                        last_name = fact_dict[key]['last']
                        lecturer_name = last_name + ' ' + fact_dict[key]['first'] + ' ' + fact_dict[key]['middle']
                        lecturer_name = processing_lecturer_name(lecturer_name=lecturer_name)

                        closest_match = difflib.get_close_matches(lecturer_name, lecturers_names)

                        if len(closest_match):
                            voice_cache[key_cache] = closest_match[0]
                            return closest_match[0]

                        voice_cache[key_cache] = None
                        return None
                    else:
                        last_name = fact_dict[key]['last']
                        lecturer_name = last_name + ' ' + fact_dict[key]['first']
                        lecturer_name = processing_lecturer_name(lecturer_name=lecturer_name)

                        closest_match = difflib.get_close_matches(lecturer_name, lecturers_names)

                        if len(closest_match):
                            voice_cache[key_cache] = closest_match[0]
                            return closest_match[0]

                        voice_cache[key_cache] = None
                        return None
                else:
                    last_name = fact_dict[key]['last']

                    closest_match = difflib.get_close_matches(last_name, lecturers_names)

                    if len(closest_match):
                        voice_cache[key_cache] = closest_match[0]
                        return closest_match[0]

                    voice_cache[key_cache] = None
                    return None

    voice_cache[key_cache] = None
    return None
