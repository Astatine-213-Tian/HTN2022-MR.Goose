import numpy as np
import time
import sys
from maze_map import LEN_6_MAP, LEN_8_MAP

if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 60  # pixels
HALF_LENGTH = UNIT / 2 - 7 # half_length of a square
WALL = 1
TRAP = 2
GRASS = 3
STU = 4


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.maze_grid = LEN_8_MAP
        self.height = len(self.maze_grid)
        self.width = len(self.maze_grid[0])
        for i in range(self.height):
            for j in range(self.width):
                if self.maze_grid[i][j] == STU:
                    self.target = (i, j)
        self.title('maze')
        self.geometry('{0}x{1}'.format(self.width * UNIT, self.height * UNIT))
        self._build_maze()
        self.visited = set()
        self.curr = (0, 0)

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white', height=self.height * UNIT, width=self.width * UNIT)

        # create grids
        for c in range(0, self.width * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, self.height * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, self.height * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, self.width * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([UNIT / 2, UNIT / 2])

        # hell
        self.hells = []
        for i in range(self.height):
            for j in range(self.width):
                if self.maze_grid[i][j] == TRAP:
                    self.canvas.create_line(UNIT * (j) + 15, UNIT * (i), UNIT * (j + 1), UNIT * (i + 1),
                                            fill="black", width=8)
                    self.canvas.create_line(UNIT * (j + 1) - 15, UNIT * (i) + 15, UNIT * (j), UNIT * (i + 1),
                                            fill="black", width=8)
                # elif self.maze_grid[i][j] == GRASS:
                #     center = origin + np.array([UNIT * j, UNIT * i])
                #     self.canvas.create_rectangle(center[0] - UNIT / 2, center[1] - UNIT / 2,
                #                                  center[0] + UNIT / 2, center[1] + UNIT / 2,
                #                                  fill="green")
                elif self.maze_grid[i][j] == WALL:
                    center = origin + np.array([UNIT * j, UNIT * i])
                    self.canvas.create_rectangle(center[0] - UNIT / 2, center[1] - UNIT / 2,
                                                 center[0] + UNIT / 2, center[1] + UNIT / 2,
                                                 fill="brown")
                elif self.maze_grid[i][j] == STU:
                    self.canvas.create_polygon(UNIT * (j) + UNIT * 3 / 7, UNIT * (i) + UNIT / 6,
                                               UNIT * (j) + UNIT * 3 / 7, UNIT * (i) + UNIT / 11,
                                               UNIT * (j) + UNIT * 4 / 7, UNIT * (i) + UNIT / 11,
                                               UNIT * (j) + UNIT * 4 / 7, UNIT * (i) + UNIT / 6,
                                               UNIT * (j) + UNIT * 9 / 10,
                                               UNIT * (i) + UNIT * 4 / 10,
                                               UNIT * (j) + UNIT * 8 / 10,
                                               UNIT * (i) + UNIT * 5 / 10,
                                               UNIT * (j) + UNIT * 4 / 7, UNIT * (i) + UNIT * 2 / 7,
                                               UNIT * (j) + UNIT * 5 / 7,
                                               UNIT * (i) + UNIT * 9 / 10,
                                               UNIT * (j) + UNIT * 4 / 7,
                                               UNIT * (i) + UNIT * 9 / 10, UNIT * (j) + UNIT / 2,
                                               UNIT * (i) + UNIT * 7 / 10,
                                               UNIT * (j) + UNIT * 3 / 7,
                                               UNIT * (i) + UNIT * 9 / 10,
                                               UNIT * (j) + UNIT * 2 / 7,
                                               UNIT * (i) + UNIT * 9 / 10,
                                               UNIT * (j) + UNIT * 3 / 7, UNIT * (i) + UNIT * 2 / 7,
                                               UNIT * (j) + UNIT / 5, UNIT * (i) + UNIT * 5 / 10,
                                               UNIT * (j) + UNIT / 10, UNIT * (i) + UNIT * 4 / 10,
                                               fill='#df2498')

        # create goose
        self.goose = self.canvas.create_polygon(UNIT / 10, UNIT / 2, UNIT / 2, UNIT / 2, UNIT * 7 / 10, UNIT / 8,
                                                UNIT * 9.5 / 10, UNIT / 6.5, UNIT * 7.5 / 10, UNIT / 4, UNIT * 9 / 10,
                                                UNIT * 2 / 3, UNIT * 7 / 10, UNIT * 8 / 10, UNIT / 8, UNIT * 8 / 10,
                                                UNIT / 5, UNIT * 2 / 3, fill='green')

        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.2)
        self.canvas.delete(self.goose)
        self.visited = set()
        self.curr = (0, 0)
        self.goose = self.canvas.create_polygon(UNIT / 10, UNIT / 2, UNIT / 2, UNIT / 2, UNIT * 7 / 10, UNIT / 8,
                                               UNIT * 9.5 / 10, UNIT / 6.5, UNIT * 7.5 / 10, UNIT / 4, UNIT * 9 / 10,
                                               UNIT * 2 / 3, UNIT * 7 / 10, UNIT * 8 / 10, UNIT / 8, UNIT * 8 / 10,
                                               UNIT / 5, UNIT * 2 / 3, fill='green')
        return self.canvas.coords(self.goose)

    def step(self, action):
        base_action = np.array([0, 0])
        moved = False
        curr_i, curr_j = self.curr[0], self.curr[1]
        if action == 0:  # up
            if curr_i > 0:
                base_action[1] -= UNIT
                self.curr = (curr_i - 1, curr_j)
                moved = True
        elif action == 1:  # down
            if curr_i < self.height - 1:
                base_action[1] += UNIT
                self.curr = (curr_i + 1, curr_j)
                moved = True
        elif action == 2:  # right
            if curr_j < self.width - 1:
                base_action[0] += UNIT
                self.curr = (curr_i, curr_j + 1)
                moved = True
        elif action == 3:  # left
            if curr_j > 0:
                base_action[0] -= UNIT
                self.curr = (curr_i, curr_j - 1)
                moved = True
        self.canvas.move(self.goose, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.goose)
        curr_i, curr_j = self.curr[0], self.curr[1]

        if self.curr == self.target:
            reward = 5
            done = True
            s_ = 'terminal'
        elif self.maze_grid[curr_i][curr_j] == WALL:
            reward = -0.75
            base_action = np.array([0, 0])
            if moved:
                if action == 0:
                    base_action[1] += UNIT
                    self.curr = (curr_i + 1, curr_j)
                elif action == 1:
                    base_action[1] -= UNIT
                    self.curr = (curr_i - 1, curr_j)
                elif action == 2:
                    base_action[0] -= UNIT
                    self.curr = (curr_i, curr_j - 1)
                elif action == 3:
                    base_action[0] += UNIT
                    self.curr = (curr_i, curr_j + 1)
                self.canvas.move(self.goose, base_action[0], base_action[1])
            done = False
        elif self.maze_grid[curr_i][curr_j] == TRAP:
            reward = -1
            done = True
            s_ = 'terminal'
        # elif self.maze_grid[curr_i][curr_j] == GRASS:
        #     reward = 0.25
        #     done = False
        elif self.curr in self.visited:
            reward = -0.25
            done = False
        else:
            reward = -0.01
            done = False

        if moved:
            self.visited.add(self.curr)
        else:
            reward = -0.8

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()


def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break


if __name__ == '__main__':
    env = Maze()
    env.after(100, update)
    env.mainloop()
