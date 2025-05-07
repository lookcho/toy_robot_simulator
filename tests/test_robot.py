from ..exec import off_the_table, Robot, Direction


# I am not going to implement conftest as it seems useless at this scale
# those tests will only work with the hardcoded bbox

def test_off_the_table():
    positions = {(0, 0): False, (4,4): False, (6,5): True, (-1, 0): True}
    for position, answer in positions.items():
        assert off_the_table(position) == answer

def test_is_fresh():
    robot = Robot(None, Direction.WEST)
    assert robot.is_fresh is True
    robot = Robot((1, 1), None)
    assert robot.is_fresh is True
    robot = Robot((1, 1), Direction.WEST)
    assert robot.is_fresh is False

def test_turning():
    robot = Robot((1, 1), Direction.WEST)
    robot.left()
    assert robot.position == (1, 1) and robot.direction == 2
    robot.left()
    robot.left()
    assert robot.direction == 0
    robot.right()
    assert robot.direction == 3

def test_moving():
    robot = Robot((1, 1), Direction.WEST)
    robot.forward()
    assert robot.direction == 1 and robot.position == (0, 1)
    robot.forward()
    assert robot.position == (0, 1)
    robot = Robot((3, 3), Direction.NORTH)
    robot.forward()
    assert robot.direction == 0 and robot.position == (3, 4)
    robot.forward()
    assert robot.position == (3, 4)

def test_placing():
    robot = Robot()
    robot.place("6", "7", Direction.NORTH.name)
    assert robot.is_fresh is True
    robot.place("2", "2", Direction.NORTH.name)
    assert robot.direction == 0 and robot.position == (2, 2)
    robot.place("1", "1", Direction.WEST.name)
    assert robot.direction == 1 and robot.position == (1, 1)

def test_inputs():
    robot = Robot()
    robot.parse_inputs("")
    assert robot.direction == None and robot.position == None
    robot.parse_inputs("MOVE")
    assert robot.direction == None and robot.position == None
    robot.parse_inputs("LEFT")
    assert robot.direction == None and robot.position == None
    robot.parse_inputs("RIGHT")
    assert robot.direction == None and robot.position == None
    robot.parse_inputs("PLACE 1,1,EAST")
    assert robot.direction == 3 and robot.position == (1, 1)
    robot.parse_inputs("MOVE")
    assert robot.direction == 3 and robot.position == (2, 1)
