from game_map.area.point import Point


def test_point():
    first_point = Point(2, 2)
    second_point = Point(1, 1)
    sum_point = first_point + second_point
    sub_point = first_point - second_point

    assert sum_point == Point(3, 3), 'Sum'
    assert sub_point == second_point, 'Sub'
    assert second_point * 2 == first_point, 'Mul'
    assert first_point / 2 == second_point, 'Div'
