#!/usr/bin/env python3
"""Study blue routing by exchanging the eight copies surrounding each centre.

Standalone Python 3.10+, standard library only. Run this file directly.
Each cell is first repeated into a 3x3 block, including its centre. Facing
edge copies swap in pairs. At each four-cell junction, diagonally opposite
corner copies swap in pairs. The final 3x3 block is the cell's neighbourhood.

This is Michael's explanatory 3x3 representation, not manufacturing geometry.
The original blue diagram has repeated ports on a 4x4 face; the 3x3 display
here makes the neighbour exchanges explicit without those repeated ports.
IMPORTANT: the six corner classes alone do not constitute a 3x3-footprint
physical tile layer. Separate edge swaps have three rotational classes;
centre pass-throughs must also be accounted for. The source instead uses
4x4 blue pieces, whose larger faces include edge routing. The functions
below model that face layout as well; they are not solid CAD.
Source: https://conwaylife.com/forums/viewtopic.php?p=73018#p73018
"""

from itertools import product

GLIDER = ((0, 1, 0), (0, 0, 1), (1, 1, 1))


def repeat_cells(grid):
    return [[grid[r // 3][c // 3] for c in range(3 * len(grid[0]))]
            for r in range(3 * len(grid))]


def corner_swap(face):
    """Two diagonal mutual swaps: A<->D and B<->C, with no new values."""
    (a, b), (c, d) = face
    return ((d, c), (b, a))


def exchange_neighbours(repeated):
    """Operate on distinct physical copy positions; keep all centres intact."""
    result = [row[:] for row in repeated]
    rows, cols = len(result) // 3, len(result[0]) // 3

    def swap(r1, c1, r2, c2):
        result[r1][c1], result[r2][c2] = result[r2][c2], result[r1][c1]

    # Facing east/west copies at every horizontal cell boundary.
    for r, c in product(range(rows), range(cols - 1)):
        swap(3 * r + 1, 3 * c + 2, 3 * r + 1, 3 * c + 3)
    # Facing south/north copies at every vertical cell boundary.
    for r, c in product(range(rows - 1), range(cols)):
        swap(3 * r + 2, 3 * c + 1, 3 * r + 3, 3 * c + 1)
    # Four corners meeting at a junction: each gets the diagonally opposite cell.
    for r, c in product(range(rows - 1), range(cols - 1)):
        y, x = 3 * r + 2, 3 * c + 2
        face = ((result[y][x], result[y][x + 1]),
                (result[y + 1][x], result[y + 1][x + 1]))
        swapped = corner_swap(face)
        for dy, dx in product(range(2), repeat=2):
            result[y + dy][x + dx] = swapped[dy][dx]
    return result


def gather(grid):
    """Return routed macroblocks for a finite pattern in a dead exterior."""
    rows, cols = len(grid), len(grid[0])
    padded = [[0] * (cols + 2)]
    padded += [[0, *row, 0] for row in grid]
    padded += [[0] * (cols + 2)]
    routed = exchange_neighbours(repeat_cells(padded))
    return [row[3:3 + 3 * cols] for row in routed[3:3 + 3 * rows]]


def rotate(face):
    return tuple(tuple(row) for row in zip(*face[::-1]))


def rotational_class(face):
    rotations = []
    for _ in range(4):
        rotations.append(face)
        face = rotate(face)
    return min(rotations)


def blue_faces(face):
    """4x4 blue piece at a junction: bottom quadrants -> four copies on top.

    Bottom:    Top:
    A A B B    A B A B
    A A B B    C D C D
    C C D D    A B A B
    C C D D    C D C D

    Four inputs determine the entire piece, not only its diagonal swaps.
    Both faces transform together when the piece is rotated.
    """
    bottom = tuple(tuple(face[r // 2][c // 2] for c in range(4)) for r in range(4))
    top = tuple(tuple(face[r % 2][c % 2] for c in range(4)) for r in range(4))
    return bottom, top


def blue_layer(grid):
    """Partition the blue layer into disjoint 4x4 pieces offset half a cell.

    Life squares are 4x4. Blue squares are also 4x4, translated (2,2).
    Each Life square consequently gets one 2x2 quadrant from four blues.
    """
    rows, cols = len(grid), len(grid[0])
    padded = [[0] * (cols + 2)] + [[0, *row, 0] for row in grid] + [[0] * (cols + 2)]
    assembled = [[None] * (4 * (cols + 2)) for _ in range(4 * (rows + 2))]
    for r, c in product(range(rows + 1), range(cols + 1)):
        face = tuple(tuple(padded[r + dr][c + dc] for dc in range(2)) for dr in range(2))
        _, top = blue_faces(face)
        for dr, dc in product(range(4), repeat=2):
            y, x = 4 * r + 2 + dr, 4 * c + 2 + dc
            assert assembled[y][x] is None, 'Blue pieces overlap'
            assembled[y][x] = top[dr][dc]
    cropped = [row[4:4 + 4 * cols] for row in assembled[4:4 + 4 * rows]]
    assert all(value is not None for row in cropped for value in row), 'Uncovered output port'
    return cropped


def verify():
    classes = {}
    for bits in product((0, 1), repeat=4):
        face = (bits[:2], bits[2:])
        key = rotational_class(face)
        classes[key] = classes.get(key, 0) + 1
        assert corner_swap(corner_swap(face)) == face
        assert rotate(corner_swap(face)) == corner_swap(rotate(face))
        bottom, top = blue_faces(face)
        assert blue_faces(rotate(face)) == (rotate(bottom), rotate(top))
    assert len(classes) == 6
    assert sorted(classes.values()) == [1, 1, 2, 4, 4, 4]
    # Every central neighbourhood, with neighbours independently 0 or 1.
    for bits in product((0, 1), repeat=9):
        grid = tuple(bits[r * 3:r * 3 + 3] for r in range(3))
        result = gather(grid)
        assert tuple(tuple(row[3:6]) for row in result[3:6]) == grid
        blue = blue_layer(grid)
        indices = (0, 1, 1, 2)
        expected = tuple(tuple(grid[indices[r]][indices[c]] for c in range(4))
                         for r in range(4))
        assert tuple(tuple(row[4:8]) for row in blue[4:8]) == expected
    # Check every glider block, including its dead exterior neighbours.
    routed = gather(GLIDER)
    for r, c, dy, dx in product(range(3), repeat=4):
        nr, nc = r + dy - 1, c + dx - 1
        expected = GLIDER[nr][nc] if 0 <= nr < 3 and 0 <= nc < 3 else 0
        assert routed[3 * r + dy][3 * c + dx] == expected
    return classes


def print_blocks(grid):
    for r, row in enumerate(grid):
        if r and r % 3 == 0:
            print()
        print(' '.join(''.join(str(x) for x in row[c:c + 3])
                       for c in range(0, len(row), 3)))


if __name__ == '__main__':
    classes = verify()
    print('Glider copies before swaps:')
    print_blocks(repeat_cells(GLIDER))
    print('\nAfter edge and diagonal swaps (dead exterior):')
    print_blocks(gather(GLIDER))
    print('\nSix rotational corner classes:')
    for face, size in sorted(classes.items()):
        print('/'.join(''.join(map(str, row)) for row in face), 'orientations:', size)
    bottom, top = blue_faces((('A', 'B'), ('C', 'D')))
    print('\nOriginal 4x4 blue face layout: BOTTOM -> TOP')
    for lower, upper in zip(bottom, top):
        print(' '.join(lower), ' -> ', ' '.join(upper))
    print('The 3x3 corner sketch additionally needs edge swaps; the 4x4 blue layout includes their routing.')
    print('PASS: all 16 blue inputs and rotations; both routing layouts on all 512 central neighbourhoods.')
