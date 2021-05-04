import math
from random import randint, random

import tkinter as tk

from gamelib import Sprite, GameApp, Text

from consts import *

class Fruit(Sprite):
    image = None
    score = 0

    def __init__(self, app, x, y):
        super().__init__(app, self.image, x, y)
        self.app = app

    def update(self):
        if self.y > CANVAS_WIDTH + 30:
            self.to_be_deleted = True

class SlowFruit(Fruit):
    image = 'images/apple.png'
    score = 1
        
    def update(self):
        self.y += FRUIT_SLOW_SPEED
        super().update()


class FastFruit(Fruit):
    image = 'images/banana.png'
    score = 2

    def update(self):
        self.y += FRUIT_FAST_SPEED

        super().update()

class Side_Fruit(Fruit):
    image = None
    score = 0

    def update(self):
        if self.x <= 0:
                self.x = 795
                print(self.x)
        if self.x >= 800:
                self.x = 5
                print(self.x)
        super().update()

class SlideFruit(Side_Fruit):
    image = 'images/cherry.png'
    score  = 2

    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.direction = randint(0,1)*2 - 1

    def update(self):
        self.y += FRUIT_FAST_SPEED
        self.x += self.direction * 5
        super().update()


class CurvyFruit(Side_Fruit):
    image = 'images/pear.png'
    score = 2

    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.t = randint(0,360) * 2 * math.pi / 360

    def update(self):
        self.y += FRUIT_SLOW_SPEED * 1.2
        self.t += 1
        self.x += math.sin(self.t*0.08)*10
        super().update()


class Basket(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/basket.png', x, y)

        self.app = app
        self.direction = None

    def update(self):
        if self.direction == BASKET_LEFT:
            if self.x >= BASKET_MARGIN:
                self.x -= BASKET_SPEED
            if self.x <= 10:
                self.x = 800
        elif self.direction == BASKET_RIGHT:
            if self.x <= CANVAS_WIDTH - BASKET_MARGIN:
                self.x += BASKET_SPEED
            if self.x >= 790:
                self.x = 0

    def check_collision(self, fruit):
        if self.distance_to(fruit) <= BASKET_CATCH_DISTANCE:
            fruit.to_be_deleted = True
            self.app.score += fruit.score
            self.app.update_score()


class BasketGame(GameApp):
    def init_game(self):
        self.basket = Basket(self, CANVAS_WIDTH // 2, CANVAS_HEIGHT - 50)
        self.elements.append(self.basket)

        self.score = 0
        self.score_text = Text(self, 'Score: 0', 100, 40)
        self.fruits = []

    def update_score(self):
        self.score_text.set_text('Score: ' + str(self.score))

    def random_fruits(self):
        if random() > 0.95:
            p = random()
            x = randint(50, CANVAS_WIDTH - 50)
            if p <= 0.3:
                new_fruit = SlowFruit(self, x, 0)
            elif p <= 0.6:
                new_fruit = FastFruit(self, x, 0)
            elif p <= 0.8:
                new_fruit = SlideFruit(self, x, 0)
            else:
                new_fruit = CurvyFruit(self, x, 0)

            self.fruits.append(new_fruit)

    def process_collisions(self):
        for f in self.fruits:
            self.basket.check_collision(f)

    def update_and_filter_deleted(self, elements):
        new_list = []
        for e in elements:
            e.update()
            e.render()
            if e.to_be_deleted:
                e.delete()
            else:
                new_list.append(e)
        return new_list

    def post_update(self):
        self.process_collisions()

        self.random_fruits()

        self.fruits = self.update_and_filter_deleted(self.fruits)

    def on_key_pressed(self, event):
        if event.keysym == 'Left':
            self.basket.direction = BASKET_LEFT
        elif event.keysym == 'Right':
            self.basket.direction = BASKET_RIGHT
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Basket Fighter")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = BasketGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
