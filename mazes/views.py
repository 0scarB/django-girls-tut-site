import random as rnd

from django.shortcuts import render
from django.utils import timezone
from .models import Maze


def get_connections_array(width, height):
    array = []
    for row_idx in range(height):
        if row_idx == 0:
            has_last_row = False
        else:
            last_row_idx = row_idx - 1
            has_last_row = True

        if row_idx == height - 1:
            has_next_row = False
        else:
            next_row_idx = row_idx + 1
            has_next_row = True

        row = []
        for column_idx in range(width):
            if column_idx == 0:
                has_last_column = False
            else:
                last_column_idx = column_idx - 1
                has_last_column = True

            if column_idx == width - 1:
                has_next_column = False
            else:
                next_column_idx = column_idx + 1
                has_next_column = True

            connections = set()
            if has_last_row:
                connections.add((last_row_idx, column_idx))
            if has_next_row:
                connections.add((next_row_idx, column_idx))
            if has_last_column:
                connections.add((row_idx, last_column_idx))
            if has_next_column:
                connections.add((row_idx, next_column_idx))

            row.append(connections)

        array.append(row)

    return array


def get_maze_connections(width, height):
    array = get_connections_array(width, height)

    coord_connections = []
    def update_neighbours(coord):
        row_idx, column_idx = coord
        for row_inc, column_inc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            try:
                connections = array[row_idx + row_inc][
                    column_idx + column_inc]
                if coord in connections:
                    connections.remove(coord)
            except IndexError:
                pass

    def get_next_coord():
        coord = idxs_with_connections[-1]
        row_idx, column_idx = coord
        connections = array[row_idx][column_idx]
        if connections:
            next_coord = rnd.choice(list(connections))
            update_neighbours(next_coord)
            idxs_with_connections.append(next_coord)
            coord_connections.append((coord, next_coord))
        else:
            next_coord = idxs_with_connections.pop()

    start_coord = (0, 0)
    update_neighbours(start_coord)
    idxs_with_connections = [start_coord]
    while idxs_with_connections:
        get_next_coord()

    return coord_connections


def get_maze_string_array(width, height, wall, path):
    maze_string_array = [[wall for _ in range(2 * width + 1)]
                         for _ in range(2 * height + 1)]
    for row_idx in range(1, 2 * height, 2):
        for column_idx in range(1, 2 * width, 2):
            maze_string_array[row_idx][column_idx] = path

    return maze_string_array


def get_maze_string(width, height, wall='||', path='  '):
    connections = get_maze_connections(width, height)

    string_array = get_maze_string_array(width, height, wall, path)
    for (row_idx1, column_idx1), (row_idx2, column_idx2) in connections:
        if row_idx1 == row_idx2:
            string_array[2 * row_idx1 + 1][
                2 * (1 + min(column_idx1, column_idx2))] = path
        else:
            string_array[2 * (1 + min(row_idx1, row_idx2))][
                2 * column_idx1 + 1] = path

    return '\n'.join([''.join(row) for row in string_array])


def get_mesurements(columns, rows,
                    spacing_horizontal, spacing_vertical,
                    rel_path_width_horizontal, rel_path_width_vertical):
    path_width_horizontal = (
        spacing_horizontal * rel_path_width_horizontal)
    path_width_vertical = (
        spacing_vertical * rel_path_width_vertical)

    wall_width_horizontal = spacing_horizontal - path_width_horizontal
    wall_width_vertical = spacing_vertical - path_width_vertical

    x_offset = wall_width_horizontal + path_width_horizontal / 2
    y_offset = wall_width_vertical + path_width_vertical / 2

    width = 2 * x_offset + (columns - 1) * spacing_horizontal
    height = 2 * y_offset + (rows - 1) * spacing_vertical

    return (width, height, x_offset, y_offset,
            path_width_horizontal, path_width_vertical)


class MazeSvg:
    def __init__(self, columns, rows,
                 spacing_horizontal, spacing_vertical,
                 rel_path_width_horizontal, rel_path_width_vertical,
                 path_color, wall_color):
        self.spacing_horizontal = spacing_horizontal
        self.spacing_vertical = spacing_vertical

        self.path_color = path_color
        self.wall_color = wall_color
        print(wall_color)

        (self.width, self.height,
         self.x_offset, self.y_offset,
         self.path_width_horizontal, self.path_width_vertical
         ) = get_mesurements(columns, rows,
                             spacing_horizontal,
                             spacing_vertical,
                             rel_path_width_horizontal,
                             rel_path_width_vertical)

        self.svg_lines = [
            f'<svg width="{self.width}" height="{self.height}">',
            f'<rect width="{self.width}" height="{self.height}" '
            f'x="0" y="0" fill="{wall_color}"/>'
        ]

    def add_connection(self, connection):
        (row1, column1), (row2, column2) = connection
        if row1 == row2:
            min_column, max_column = sorted((column1, column2))
            x1 = (self.x_offset
                  + self.spacing_horizontal * min_column
                  - self.path_width_vertical / 2)
            x2 = (self.x_offset
                  + self.spacing_horizontal * max_column
                  + self.path_width_vertical / 2)
            y1 = y2 = self.y_offset + self.spacing_vertical * row1

            line_width = self.path_width_horizontal
        if column1 == column2:
            min_row, max_row = sorted((row1, row2))
            x1 = x2 = self.x_offset + self.spacing_horizontal * column1
            y1 = (self.y_offset
                  + self.spacing_vertical * min_row
                  - self.path_width_horizontal / 2)
            y2 = (self.y_offset
                  + self.spacing_vertical * max_row
                  + self.path_width_horizontal / 2)

            line_width = self.path_width_vertical

        self.svg_lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'style="stroke: {self.path_color}; '
            f'stroke-width: {line_width}; stroke-linecap: butt"/>'
        )

    def get_svg(self):
        self.svg_lines.append('</svg>')
        return '\n'.join(self.svg_lines)


def get_maze_svg(columns, rows,
                 spacing_horizontal=10,
                 spacing_vertical=None,
                 rel_path_width_horizontal=0.5,
                 rel_path_width_vertical=None,
                 path_color='white', wall_color='black'):
    if spacing_vertical is None:
        spacing_vertical = spacing_horizontal
    if rel_path_width_vertical is None:
        rel_path_width_vertical = rel_path_width_horizontal

    maze_svg = MazeSvg(columns, rows,
                       spacing_horizontal,
                       spacing_vertical,
                       rel_path_width_horizontal,
                       rel_path_width_vertical,
                       path_color, wall_color)

    for connection in get_maze_connections(columns, rows):
        maze_svg.add_connection(connection)

    return maze_svg.get_svg()


def maze_list(request):
    mazes = Maze.objects.filter(published_date__lte=timezone.now()
        ).order_by('published_date')
    for maze in mazes:
        path_color = f'rgb({maze.path_r},{maze.path_g},{maze.path_b})'
        wall_color = f'rgb({maze.wall_r},{maze.wall_g},{maze.wall_b})'
        maze_svg = get_maze_svg(maze.width, maze.height,
                                maze.horizontal_spacing,
                                maze.vertical_spacing,
                                maze.horizontal_path_width,
                                maze.vertical_path_width,
                                path_color,
                                wall_color)
        maze.maze_svg = maze_svg
    return render(request, 'mazes/maze_list.html', {
        'mazes': mazes,
        })
