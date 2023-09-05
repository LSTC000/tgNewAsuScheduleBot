from data.config import BUILDINGS_LOCATION_DICT


def find_building_location(room: str) -> str:
    """
    :param room: Room name.
        Example: '401 Л'.
    :return: Room name with building location url.
        Example: '<a href="{housing_location_url}" title="корпус"><b>401 Л</b></a>.'.
    """

    lower_room = room.lower()

    if 'сок' in lower_room:
        return f'<a href="{BUILDINGS_LOCATION_DICT["сок"]}" title="корпус"><b>{room}</b></a>'

    if 'лыж' in lower_room:
        return f'<a href="{BUILDINGS_LOCATION_DICT["лыж.база"]}" title="корпус"><b>{room}</b></a>'

    split_lower_room = lower_room.split()

    for key in list(BUILDINGS_LOCATION_DICT.keys())[:-2]:
        if key in split_lower_room:
            return f'<a href="{BUILDINGS_LOCATION_DICT[key]}" title="корпус"><b>{room}</b></a>'

    return room
