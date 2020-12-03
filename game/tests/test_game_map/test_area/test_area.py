from game_map.area.area import Area, Point


def test_area():

    left_bottom = Point(0, 0)
    right_top = Point(10, 8)

    area = Area(left_bottom, right_top)

    assert area.center == Point(5, 4)
    assert area.size_x == 8
    assert area.size_y == 10
