def first_letter_upper_case(text: str) -> str:
    '''
    :param text: Text in lower case.
        Example: 'найди мне козлова дениса юрьевича'.
    :return: The name of the lecturer in upper case.
        Example: 'Найди Мне Козлова Дениса Юрьевича'.
    '''

    split_text = text.split()

    return ' '.join([value[0].upper() + value[1:] if len(value) > 1 else value for value in split_text])
