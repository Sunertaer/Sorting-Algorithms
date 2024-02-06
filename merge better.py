from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import numpy as np

class Renderer(Window):
    def __init__(self):
        super().__init__(900, 600, "Merge Sort Visualizer")
        self.set_location(100, 50)
        self.batch = Batch()
        self.arr = np.random.randint(10, 200, 50)
        self.x = list(self.arr)
        #self.x = [60, 50, 10, 40, 80 , 90, 30, 70, 20]
        self.bars = []
        for e, i in enumerate(self.x):
            self.bars.append(Rectangle(15+e*15, 15, 10, i, batch=self.batch, color=(255, 255, 255, 255)))
        self.animation_generator = self.merge_sort_animation(0, len(self.x) - 1)

    def merge_sort_animation(self, l, r):
        if l < r:
            mid = (l + r) // 2
            yield from self.merge_sort_animation(l, mid)
            yield from self.merge_sort_animation(mid + 1, r)
            yield from self.merge(l, mid, r)

    def merge(self, l, mid, r):
        left, right = self.x[l:mid + 1], self.x[mid + 1:r + 1]
        i, j, k = 0, 0, l
        while i < len(left) and j < len(right):
            self.bars[l + i].color = (255, 0, 0, 255)
            self.bars[mid + 1 + j].color = (255, 0, 0, 255)
            yield
            self.bars[l + i].color = (255, 255, 255, 255)
            self.bars[mid + 1 + j].color = (255, 255, 255, 255)

            self.x[k] = min((left[i], right[j]))
            if self.x[k] == left[i]:
                i += 1
            else:
                j += 1
            k += 1
            yield

        self.x[k:r + 1] = left[i:] + right[j:]
        self.update_bars()

    def update_bars(self):
        self.bars = []
        for e, i in enumerate(self.x):
            self.bars.append(Rectangle(15+e*15, 15, 10, i, batch=self.batch, color=(255, 255, 255, 255)))
    
    def on_update(self, dt):
        try:
            next(self.animation_generator)
        except StopIteration:
            for bar in self.bars:
                bar.color = (0, 255, 0, 255)

    def on_draw(self):
        self.clear()
        self.batch.draw()

renderer = Renderer()
clock.schedule_interval(renderer.on_update, 0.1)
run()