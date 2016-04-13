from random import randrange
from libs.enum import Enum


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


class Move(Enum):
    LEFT = 1
    FORWARD = 2
    RIGHT = 3
    STAND_STILL = 4


class Flatland:

    food = 1
    poison = 2
    agent = 3
    food_prob = 0.33
    poison_prob = 0.33

    def __init__(self, length, agent_start):
        # Grid length
        self.length = length

        # Agent position
        self.agent_start = agent_start
        self.agent_y = agent_start[0]
        self.agent_x = agent_start[1]
        self.agent_direction = agent_start[2]

        # Generate empty grid with respect to grid length
        self.grid = [[0 for _ in xrange(self.length)] for _ in xrange(self.length)]

        # Add agent starting position to grid
        self.grid[self.agent_y][self.agent_x] = Flatland.agent

        # Stochastic placement of food given food poison distribution
        cls = self.__class__
        self.place_food(int(length*length*cls.food_prob))
        self.place_poison(int(length*length*cls.poison_prob))

    # Stochastic placement of food
    def place_food(self, total_foods):
        while total_foods != 0:
            x, y = randrange(0, self.length), randrange(0, self.length)
            cell = self.grid[y][x]
            while cell != 0:
                x, y = randrange(0, self.length), randrange(0, self.length)
                cell = self.grid[y][x]

            self.grid[y][x] = Flatland.food
            total_foods -= 1

    # Stochastic placement of poison
    def place_poison(self, total_poisons):
        while total_poisons != 0:
            x, y = randrange(0, self.length), randrange(0, self.length)
            cell = self.grid[y][x]
            while cell != 0:
                x, y = randrange(0, self.length), randrange(0, self.length)
                cell = self.grid[y][x]

            self.grid[y][x] = Flatland.poison
            total_poisons -= 1

    # Updates agent direction based on move direction
    def calculate_agent_direction(self, move_direction):
        if self.agent_direction == Direction.NORTH:

            if move_direction == Move.LEFT:
                self.agent_direction = Direction.WEST

            elif move_direction == Move.RIGHT:
                self.agent_direction = Direction.EAST

        elif self.agent_direction == Direction.EAST:

            if move_direction == Move.LEFT:
                self.agent_direction = Direction.NORTH

            elif move_direction == Move.RIGHT:
                self.agent_direction = Direction.SOUTH

        elif self.agent_direction == Direction.SOUTH:

            if move_direction == Move.LEFT:
                self.agent_direction = Direction.EAST

            elif move_direction == Move.RIGHT:
                self.agent_direction = Direction.WEST

        elif self.agent_direction == Direction.WEST:

            if move_direction == Move.LEFT:
                self.agent_direction = Direction.SOUTH

            elif move_direction == Move.RIGHT:
                self.agent_direction = Direction.NORTH

    # Enforces wrap-around grid (teroidal world) on coordinates out of bounce
    def get_teroidal_cell_component(self, c):
        if c < 0:
            return self.length - 1
        elif c > (self.length - 1):
            return 0
        else:
            return c

    # Moves agent based on its new direction
    def calculate_agent_coordinates(self):
        if self.agent_direction == Direction.NORTH:
            self.agent_y = self.get_teroidal_cell_component(self.agent_y - 1)
        elif self.agent_direction == Direction.EAST:
            self.agent_x = self.get_teroidal_cell_component(self.agent_x + 1)
        elif self.agent_direction == Direction.SOUTH:
            self.agent_y = self.get_teroidal_cell_component(self.agent_y + 1)
        elif self.agent_direction == Direction.WEST:
            self.agent_x = self.get_teroidal_cell_component(self.agent_x - 1)

    # Change agent direction, coordinates and commit changes to grid
    def move_agent(self, move_direction):
        if move_direction != Move.STAND_STILL:
            self.calculate_agent_direction(move_direction)
            self.grid[self.agent_y][self.agent_x] = 0
            self.calculate_agent_coordinates()
            self.grid[self.agent_y][self.agent_x] = 3

    # Returns content of the LEFT, TOP, RIGHT cell with respect to agent direction
    def get_sensible_cells(self):
        cells = []
        if self.agent_direction == Direction.NORTH:
            cells.append(self.grid[self.agent_y][self.get_teroidal_cell_component(self.agent_x - 1)])
            cells.append(self.grid[self.get_teroidal_cell_component(self.agent_y - 1)][self.agent_x])
            cells.append(self.grid[self.agent_y][self.get_teroidal_cell_component(self.agent_x + 1)])
        elif self.agent_direction == Direction.EAST:
            cells.append(self.grid[self.get_teroidal_cell_component(self.agent_y - 1)][self.agent_x])
            cells.append(self.grid[self.agent_y][self.get_teroidal_cell_component(self.agent_x + 1)])
            cells.append(self.grid[self.get_teroidal_cell_component(self.agent_y + 1)][self.agent_x])
        elif self.agent_direction == Direction.SOUTH:
            cells.append(self.grid[self.agent_y][self.get_teroidal_cell_component(self.agent_x + 1)])
            cells.append(self.grid[self.get_teroidal_cell_component(self.agent_y + 1)][self.agent_x])
            cells.append(self.grid[self.agent_y][self.get_teroidal_cell_component(self.agent_x - 1)])
        elif self.agent_direction == Direction.WEST:
            cells.append(self.grid[self.get_teroidal_cell_component(self.agent_y + 1)][self.agent_x])
            cells.append(self.grid[self.agent_y][self.get_teroidal_cell_component(self.agent_x - 1)])
            cells.append(self.grid[self.get_teroidal_cell_component(self.agent_y - 1)][self.agent_x])

        return cells
