def processing_lecturer_name(lecturer_name: str) -> str:
    '''
    :param lecturer_name: The name of the lecturer.
        Example: 'Козлов Денис Юрьевич'.
    :return: The correct name of the lecturer for the request.
        Example: 'Козлов Д.Ю.'.
    '''

    split_lecturer_name = lecturer_name.split()

    if len(split_lecturer_name) == 1:
        return split_lecturer_name[0]
    else:
        return split_lecturer_name[0] + ' ' + '.'.join(list(map(lambda x: x[0], split_lecturer_name[1:]))) + '.'
