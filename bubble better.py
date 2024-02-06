from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import numpy as np

class Renderer(Window):
    def __init__(self):
        super().__init__(900, 600, "Bubble sort Visualizer")
        self.batch = Batch()
        self.x = np.random.randint(1, 200, 50)
        #self.x = [60, 50, 10, 40, 80 , 90, 30, 70, 20]
        self.bars = []
        for e, i in enumerate(self.x):
            self.bars.append(Rectangle(15+e*15, 15, 10, i, batch=self.batch))
        self.steps = self.bubble_sort()
        self.compare_indexs = None
        self.is_sort_done = False

    def bubble_sort(self):
        n = len(self.x)
        steps = []
        flag = False
        while not flag:
            flag = True
            for j in range(n - 1):
                steps.append((list(self.x), (j, j+1)))
                if self.x[j] > self.x[j + 1]:
                    self.x[j], self.x[j + 1] = self.x[j + 1], self.x[j]
                    flag = False
                steps.append((list(self.x), (j, j+1)))
            steps.append((list(self.x), None))
        return steps

    def on_update(self, deltatime):
        if self.steps:
            current_step, compare_indexs = self.steps.pop(0)
            self.compare_indexs = compare_indexs

            for i, bar in enumerate(self.bars):
                bar.height = current_step[i]

            if not self.steps:
                self.is_sort_done = True

    def on_draw(self):
        self.clear()
        for i, bar in enumerate(self.bars):
            if self.is_sort_done:
                bar.color = (0, 255, 0, 255)
            elif self.compare_indexs and i in self.compare_indexs:
                bar.color = (255, 0, 0, 255)
            else:
                bar.color = (255, 255, 255, 255)
            bar.draw()

renderer = Renderer()
clock.schedule_interval(renderer.on_update, 0.007)
run()