import logging
from typing import Optional
from dataclasses import dataclass
from enum import IntEnum


# XXX: Note regarding the type ignoring -
# Normally I'll annotate them and/or then raise error to remove the uncertainty
# However, in this case we want to mute the errors and continue with new attempt of execution

# XXX: Note regarding the design pattern -
# In normal circumstances I'd do this as Commands, to allow backtracking the path traveled
# In this case though the time is too short and it is not in the requirements

# XXX: This should probably be turned into some sort of a setting
TABLE_BBOX = (0, 0, 5, 5)


DIRECTIONS = (
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
)


def off_the_table(position: tuple[int, int]) -> bool:
    if TABLE_BBOX[0] <= position[0] < TABLE_BBOX[2] and TABLE_BBOX[1] <= position[1] < TABLE_BBOX[3]:
        return False
    return True


class Direction(IntEnum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


@dataclass
class Robot:
    # XXX: position should be a Point class of its own
    position: Optional[tuple[int, int]] = None
    direction: Optional[Direction] = None
    exit: bool = False

    @property
    def is_fresh(self):
        if fresh := (self.position is None or self.direction is None):
            logging.warning('The first command should be of type "PLACE X,Y,F"')
        return fresh

    def left(self):
        if not self.is_fresh:
            self.direction = Direction((self.direction + 1) % 4)  # type: ignore

    def right(self):
        if not self.is_fresh:
            self.direction = Direction((self.direction - 1) % 4)  # type: ignore

    def forward(self):
        if not self.is_fresh:
            new_position: tuple[int, int] = tuple(a + b for a, b in zip(self.position, DIRECTIONS[self.direction]))  # type: ignore
            if off_the_table(new_position):
                logging.warning("The robot will fall of the table. Please try with another command!")
                return
            self.position = new_position

    def place(self, x: str, y: str, f: str):
        try:
            if not off_the_table(position := (int(x), int(y))):
                self.position = position
            else:
                logging.warning(f"Provided position is off the table: x={x}, y={y}")
        except TypeError:
            # Will not raise the error because we want to continue with the execution
            logging.error(f"Some of the provided positional values are not integer: x={x}, y={y}")

        try:
            self.direction = Direction[f]
        except ValueError:
            logging.error(f"The provided direction is not acceptable: {f}, try NORTH, WEST, SOUTH or EAST")

    def report(self):
        if not self.is_fresh:
            logging.info(f"Output: {self.position[0]}, {self.position[1]}, {Direction(self.direction % 4).name}")  # type: ignore

    def parse_inputs(self, input: str):
        # XXX: This will not handle multiple commands in one request ...
        match input.strip().upper():
            case "LEFT":
                self.left()
            case "RIGHT":
                self.right()
            case t if "PLACE" in t:
                try:
                    x, y, f = input.split(" ")[1].split(",")
                    self.place(x, y, f)
                except ValueError:
                    logging.error("Please provide x and y values that are integers.")
                except KeyError:
                    logging.error("The direction value can be only one of NORTH, WEST, SOUTH, EAST")
            case "MOVE":
                self.forward()
            case "REPORT":
                self.report()
            case "EXIT":
                self.exit = True
            case _:
                logging.warning("Unexpected command, please try one of LEFT, RIGHT, MOVE, PLACE x,y,f, EXIT")


def main():
    robot = Robot()
    logging.info(
        """
            Please type a command to start the simulation.
            The first command should be PLACE, after that order them at your discretion.

            PLACE X,Y,F (where X and Y are integers and F is one of: NORTH, EAST, SOUTH, WEST)
                            i.e. PLACE 2,3,NORTH
            MOVE
            LEFT
            RIGHT
            REPORT
            EXIT
            Press enter after each command.
            Use the Up and Down arrows to repeat commands that you have already used.
        """
    )
    while not robot.exit:
        robot.parse_inputs(input())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    # XXX: may have been worth adding some args to enable loading the commands from file
    main()
