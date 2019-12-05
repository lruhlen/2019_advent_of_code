import numpy as np
from scipy.sparse import lil_matrix # For EFFICIENCY!!!!!

# Part 1
default_origin = np.array([0, 0])


class Grid():
    def __init__(self, nrows=10, ncols=10, origin=default_origin):
        self.nrows = nrows
        self.ncols = ncols
        self.grid = lil_matrix((self.nrows, self.ncols), dtype=np.int8)
        self.origin = origin
        self._current_x = self.origin[0]
        self._current_y = self.origin[1]

    def show(self):
        """Display origin point in lower left"""
        print(self.grid.toarray()[::-1])

    def parse_instruction(self, inst):
        direction = inst[0]
        magnitude = int(inst[1:])

        if direction in ('D', 'L'):
            magnitude = -1 * magnitude

        if direction in ('D', 'U'):
            direction = 'v'
        else:
            direction = 'h'

        return (magnitude, direction)

    def update(self, instruction):
        """Numpy indexing order: row (y), col (x)"""
        import pdb; pdb.set_trace()

        magnitude, direction = self.parse_instruction(instruction)
        if direction == "v":
            new_y = self._current_y + magnitude
            
            if (new_y < 0) | (new_y > self.nrows):
                raise Exception("You've gone off the grid")

            low = min(new_y, self._current_y)
            high = max(new_y, self._current_y)
            self.grid[low:high, self._current_x] = 1
            self._current_y = new_y
        elif direction == "h":
            new_x = self._current_x + magnitude

            if (new_x < 0) | (new_x > self.ncols):
                raise Exception("You've gone off the grid")

            low = min(new_x, self._current_x)
            high = max(new_x, self._current_x)
            self.grid[self._current_y, low:high] = 1
            self._current_x = new_x

        # Fix the missing corners bug with a hammer
        self.grid[self._current_y, self._current_x] = 1 

    def build_path(self, instructions):
        for inst in instructions:
            #m, d = self.parse_instruction(inst)
            self.update(inst)


def find_intersections(grid1, grid2):
    crosses = np.logical_and(grid1.grid.toarray(), grid2.grid.toarray()).nonzero()
    result = np.array(list(zip(crosses[0], crosses[1])))

    return result


def calc_distance(point, origin=default_origin):
    """Using Manhattan distance!"""
    deltas = np.abs(point - origin)
    return (sum(deltas))


def find_closest_intersection(grid1, grid2, origin=default_origin):
    itxs = find_intersections(grid1, grid2)
    distances = [calc_distance(i, origin=origin) for i in itxs if (i != origin).any()]
    
    if len(distances) == 0:
        raise Exception("No intersections detected")

    return min(distances)


def main(l1, l2):
    l1 = l1.split(',')
    l2 = l2.split(',')

    g1 = Grid(nrows=1000, ncols=1000, origin=[500,500])
    g2 = Grid(nrows=1000, ncols=1000, origin=[500,500])

    g1.build_path(l1)
    g2.build_path(l2)

    result = find_closest_intersection(g1, g2)
    return result
    



# Tests

def test_main():
    i1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    i2 = 'U62,R66,U55,R34,D71,R55,D58,R83'
    result = main(i1, i2)
    assert (result == 159)


def test_update():
    g = Grid(nrows=3, ncols=3)
    g.update(2, 'h')
    g.update(2, 'v')
    g.update(-2, 'h')
    expected_result = np.array([[1, 1, 1], [0, 0, 1], [1, 1, 1]])
    assert (g.grid == expected_result).all()


def test_parse_instructions():
    my_grid = Grid()
    assert (my_grid.parse_instruction('U10') == (10, 'v'))
    assert (my_grid.parse_instruction('D10') == (-10, 'v'))
    assert (my_grid.parse_instruction('R10') == (10, 'h'))
    assert (my_grid.parse_instruction('L10') == (-10, 'h'))


def test_find_intersections():
    g1 = np.zeros((3, 3))
    g2 = np.zeros((3, 3))
    g1[0, 0] = g1[1, 1] = g1[2, 2] = g1[0, 2] = 1
    g2[2, 0] = g2[1, 1] = g2[0, 2] = 1

    result = find_intersections(g1, g2)
    assert (len(result) == 2)
    assert (result == np.array([[0, 2], [1, 1]])).all()


def test_manhattan_distance_calculator():
    assert (calc_distance(np.array([0,0])) == 0)
    assert (calc_distance(np.array([12, 3])) == 15)
    assert (calc_distance(np.array([0,0]), origin=[10, 10]) == 20)


def test_find_closest_intersection():
    g1 = np.zeros((3, 3))
    g2 = np.zeros((3, 3))
    g1[0, 0] = g1[1, 1] = g1[2, 2] = g1[0, 2] = 1
    g2[2, 0] = g2[1, 1] = g2[0, 2] = 1

    result = find_closest_intersection(g1, g2)
    assert (result == 2)

    result = find_closest_intersection(g1, g2, origin=np.array([0,1]))
    assert (result == 1)
