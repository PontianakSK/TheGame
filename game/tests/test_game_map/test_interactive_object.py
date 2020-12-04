from game_map.interactive_object import InteractiveObject


def test_add_remove_object():

    outer_object = InteractiveObject()
    inner_object = InteractiveObject()
    assert inner_object not in outer_object.container
    outer_object.add_object(inner_object)
    assert inner_object in outer_object.container
    outer_object.remove_object(inner_object)
    assert inner_object not in outer_object.container


def test_move_object():

    first_location = InteractiveObject()
    second_location = InteractiveObject()
    inter_object = InteractiveObject()

    assert inter_object.location is None
    inter_object.move(first_location)
    assert inter_object.location is first_location
    assert inter_object in first_location.container
    inter_object.move(second_location)
    assert inter_object.location is second_location
    assert inter_object in second_location.container
    assert inter_object not in first_location.container
