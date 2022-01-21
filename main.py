"""
The piece of code that puts everything together.
"""

import random

import pyxel

pyxel.init(160, 120, title="Diddi and the Bugs")


class Bullet:
    "An independent bullet."

    def __init__(self, x, y, bullet_trick=False):
        self.x = x
        self.y = y
        self.h = 2
        self.w = 6
        self.speed = 4
        self.alive = True
        # When "bullet_trick" is set True, it is part of the "bullet trick"
        self.bullet_trick = bullet_trick

    def update(self):
        self.x += self.speed
        if self.x > pyxel.width:
            self.alive = False

    def draw(self):
        if self.alive:
            # Will display in orange color (9) when
            # the bullet trick is on. If not, the bullet
            # will be green (11).
            color = 9 if self.bullet_trick else 11
            pyxel.rect(self.x, self.y, self.w, self.h, color)


class Enemy:
    "Some bugs!"

    def __init__(self):
        self.possible_enemies = [
            (0, 8),
            (8, 8),
            (16, 0),
            (24, 0),
            (32, 0),
            (32, 8),
            (40, 0),
        ]
        self.aspect = random.choice(self.possible_enemies)
        self.x = pyxel.width
        self.y = random.randint(10, pyxel.height - 10)
        self.max_speed = 2
        self.speed = random.randint(1, self.max_speed)
        self.alive = True
        self.show = False

    def try_to_activate(self, possibilities):
        if possibilities > 100:
            exp = 15
        elif possibilities > 50:
            exp = 10
        else:
            exp = 5
        if random.randint(1, possibilities * exp) == 1:
            self.show = True

    def update(self, bullets):
        if not self.show:
            return None
        self.x -= self.speed
        if self.x == 0:
            self.aspect = random.choice(self.possible_enemies)
            self.x = pyxel.width
            self.y = random.randint(10, pyxel.height - 10)
            self.speed = random.randint(1, self.max_speed)
            self.show = False
        for bullet in bullets:
            if (
                self.x in range(bullet.x - 5, bullet.x + bullet.w + 5)
                and self.y in range(bullet.y - 5, bullet.y + bullet.h + 5)
                and bullet.alive
            ):
                self.alive = False
                bullet.alive = False

    def draw(self):
        if not self.show:
            return None
        if self.alive:
            pyxel.blt(self.x, self.y, 0, self.aspect[0], self.aspect[1], 8, 8, 0)


class Trash(Enemy):
    "Not all the space trash is harmful. Here, it can make you win 50, 100 or even 200 extra points!"

    def __init__(self):
        # override these stuff
        self.possible_enemies = [
            (16, 8),
            (24, 8),
            (40, 8),
        ]
        self.aspect = random.choice(self.possible_enemies)
        self.max_speed = 3
        self.x = pyxel.width
        self.y = random.randint(10, pyxel.height - 10)
        self.speed = random.randint(1, self.max_speed)
        self.alive = True
        self.show = False


class App:
    "The main piece of the game. It also operates the starfighter."

    def __init__(self):
        self.reset()

        pyxel.run(self.update, self.draw)

    def reset(self):
        pyxel.load("resource.pyxres")

        self.alive = True  # the player is still alive
        self.already_won = False
        self.pause = False
        self.player_x = 10
        self.player_y = 50
        self.player_lives = 3
        self.bullet_list = []
        self.continous_bullets_delay = 30
        self.continous_bullets_spacing = 2
        self.bullet_last_num_frame = 0
        self.bullet_last_held_long = False
        self.enemies = [Enemy() for sth in range(200)]
        self.trash = [Trash() for sth in range(50)]
        self.score = 0

        pyxel.stop()
        pyxel.playm(0, loop=True)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
        if pyxel.btnp(pyxel.KEY_P):
            if self.pause:
                self.pause = False
                pyxel.playm(0, loop=True)
            else:
                self.pause = True
        if self.pause and self.alive:
            return None
        if not self.alive or self.already_won:
            return None
        if pyxel.btnp(pyxel.KEY_SPACE):
            # Reverting back the firing logic that was here, inside of `pyxel.btnp()`
            self.bullet_list.append(Bullet(self.player_x + 9, self.player_y + 3))
            pyxel.playm(3)

        if pyxel.btn(pyxel.KEY_SPACE):
            # The continous bullet easter-egg goes here, under `pyxel.btn()`
            self.bullet_last_num_frame += 1
            if self.bullet_last_held_long:
                if pyxel.frame_count % self.continous_bullets_spacing == 0:
                    self.bullet_list.append(
                        Bullet(self.player_x + 9, self.player_y + 3, True)
                    )
                    pyxel.playm(3)

        if pyxel.btnr(pyxel.KEY_SPACE):
            # Reset continous bullets back if space key is released
            self.bullet_last_num_frame = 0
            self.bullet_last_held_long = False
        for bullet in self.bullet_list:
            if bullet.alive:
                bullet.update()
            else:
                self.bullet_list.remove(bullet)
        for enem in self.enemies:
            enem.try_to_activate(len(self.enemies))
        for trash in self.trash:
            trash.try_to_activate(101)

        self.add_enemies()
        self.add_trash()
        self.move_spacecraft()

        if len(self.enemies) < 1 and self.alive and not self.already_won:
            # we can play a victory sound!
            pyxel.stop()
            pyxel.playm(2)
            self.already_won = True

        if self.bullet_last_num_frame >= self.continous_bullets_delay:
            self.bullet_last_num_frame = 0
            self.bullet_last_held_long = True

    def move_spacecraft(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y = max(self.player_y - 2, 10)
            # Resetting bullets back when moved
            self.bullet_last_num_frame = 0
            self.bullet_last_held_long = False
        elif pyxel.btn(pyxel.KEY_DOWN):
            # Resetting bullets back when moved
            self.bullet_last_num_frame = 0
            self.bullet_last_held_long = False
            self.player_y = min(self.player_y + 2, pyxel.height - 10)

    def add_enemies(self):
        try:
            for enem in range(len(self.enemies)):
                if self.enemies[enem].alive:
                    self.enemies[enem].update(self.bullet_list)
                    if self.player_x in range(
                        self.enemies[enem].x - 5, self.enemies[enem].x + 5
                    ) and self.player_y in range(
                        self.enemies[enem].y - 5, self.enemies[enem].y + 5
                    ):
                        self.alive = False
                        pyxel.stop()
                        pyxel.playm(1)
                else:
                    self.score += 10
                    self.enemies.pop(enem)
                    pyxel.playm(4)
        except Exception:
            # out of range, just pass
            pass

    def add_trash(self):
        try:
            for item in range(len(self.trash)):
                if self.trash[item].alive:
                    self.trash[item].update(self.bullet_list)
                    if self.player_x in range(
                        self.trash[item].x - 5, self.trash[item].x + 5
                    ) and self.player_y in range(
                        self.trash[item].y - 5, self.trash[item].y + 5
                    ):
                        self.alive = False
                        pyxel.stop()
                        pyxel.playm(1)
                else:
                    self.score += random.choice([50, 100, 200])
                    self.trash.pop(item)
                    pyxel.playm(4)
        except Exception:
            # just like the enemies, this will just pass
            pass

    def draw(self):
        pyxel.cls(0)
        score = f"Score: {self.score}"
        enem_count = f"Enemies: {len(self.enemies)}"
        pyxel.text(5, 4, score, 1)
        pyxel.text(4, 4, score, 7)
        pyxel.text(71, 4, enem_count, 1)
        pyxel.text(70, 4, enem_count, 7)
        if self.pause and self.alive:
            # paused, don't worry
            pyxel.stop()
            pyxel.text(
                19,
                50,
                "The game is paused. Press P to play,\nR to restart and Q to quit",
                1,
            )
            pyxel.text(
                18,
                50,
                "The game is paused. Press P to play,\nR to restart and Q to quit",
                7,
            )
        elif len(self.enemies) < 1 and self.alive:
            # you won!!!
            pyxel.text(
                21,
                50,
                "You won! :) Press R to restart\n or press Q to quit the game",
                1,
            )
            pyxel.text(
                20,
                50,
                "You won! :) Press R to restart\n or press Q to quit the game",
                7,
            )
        elif self.alive:
            # the show is keep going!
            pyxel.blt(self.player_x, self.player_y, 0, 8, 0, 8, 8, 0)
            for bullet in self.bullet_list:
                bullet.draw()
            for enem in self.enemies:
                enem.draw()
            for trash in self.trash:
                trash.draw()
        else:
            # you loose! try again
            pyxel.text(
                21, 50, "Oh no! :( Press R to restart\n or press Q to quit the game", 1
            )
            pyxel.text(
                20, 50, "Oh no! :( Press R to restart\n or press Q to quit the game", 7
            )


App()
