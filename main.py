"""
The piece of code that puts everything together.
"""

import random
import sys

import pyxel

# When bumping to a higher Python requirement, please
# modify this varible, basically to avoid users from
# running with an old Python.
EXPECTED_PYTHON = (3, 7)

if sys.version_info < EXPECTED_PYTHON:
    sys.exit(
        f"Error: expected Python version {EXPECTED_PYTHON} or newer, got {sys.version_info}"
    )

pyxel.init(180, 140, title="Diddi and the Bugs")


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
            # Will display in dark green color (3) when
            # the bullet trick is on. If not, the bullet
            # will be a lighter green (11).
            color = 3 if self.bullet_trick else 11
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
        self.y = random.randint(10, pyxel.height - 28)
        self.max_speed = 2
        self.speed = random.randint(1, self.max_speed)
        self.alive = True
        self.show = False
        self.size = 8
        self.recycle = True

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
            if self.recycle:
                self.aspect = random.choice(self.possible_enemies)
                self.x = pyxel.width
                self.y = random.randint(10, pyxel.height - 28)
                self.speed = random.randint(1, self.max_speed)
            else:
                self.alive = False
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
            pyxel.blt(
                self.x,
                self.y,
                0,
                self.aspect[0],
                self.aspect[1],
                self.size,
                self.size,
                0,
            )


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
        self.y = random.randint(10, pyxel.height - 28)
        self.speed = random.randint(1, self.max_speed)
        self.alive = True
        self.show = False
        self.size = 8
        self.recycle = True


class Monster(Enemy):
    "A giant enemy that, if destroyed, generates 1000 extra points!"

    def __init__(self):
        # override all these stuff,
        # which heavily customizes the behavior
        self.possible_enemies = [(48, 0)]
        self.aspect = self.possible_enemies[
            0
        ]  # there's only one aspect, no need to choose
        self.x = pyxel.width
        self.y = random.randint(10, pyxel.height - 28)
        self.max_speed = 6  # it can move *really* fast, or maybe not!
        self.speed = random.randint(1, self.max_speed)
        self.alive = True
        self.show = False
        self.size = 16  # 16p per side, 4x4 blocks in the Pyxel editor
        self.recycle = False  # don't regenerate after reaching x=0
        self.available = (
            True  # this unique attribute will make the difference from the dead monster
        )


class DeadMonster(Monster):
    "Just like the monster, but with no activity enabled."

    def __init__(self):
        Monster.__init__(self)
        self.alive = False
        self.show = False
        self.available = False  # not available to play!

    def update(self, bullets):
        pass

    def draw(self):
        pass


class App:
    "The main piece of the game. It also operates the starfighter."

    def __init__(self):
        # This variable is not on `reset`, because
        # we are keeping a message record until
        # the app quits.
        self.messages = []

        self.message_goodies = [
            "Woo hoo!",
            "Let's save the Earth!",
            "Find the 'easter eggs'!",
            "Willpower to Earth, can you hear me?",
            "Hang tight...",
            "I'm hungry, aren't you?",
            "It's cold here, don't you think?",
            "Wow! This spacecraft really moves!",
        ]

        self.reset()

        self.add_message("Let's go!")

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
        self.continous_bullets_message = False
        self.bullet_last_num_frame = 0
        self.bullet_last_held_long = False
        self.enemies = [Enemy() for sth in range(200)]
        self.trash = [Trash() for sth in range(50)]
        self.score = 0
        self.monster = Monster()  # this guy is outside the other enemies

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
        if pyxel.btnp(pyxel.KEY_M):
            self.add_message(random.choice(self.message_goodies))
        if pyxel.btnr(pyxel.KEY_P) and self.alive:
            # We have just raised a "pause event", so we should say it
            self.add_message("Game paused" if self.pause else "Game resumed", True)
        if pyxel.btnr(pyxel.KEY_R):
            self.add_message("Re-started the game", True)
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
                    if not self.continous_bullets_message:
                        self.add_message("Ah! Continous bullets!")
                        self.continous_bullets_message = True
                    self.bullet_list.append(
                        Bullet(self.player_x + 9, self.player_y + 3, True)
                    )
                    pyxel.playm(3)

        if pyxel.btnr(pyxel.KEY_SPACE):
            # Reset continous bullets back if space key is released
            self.bullet_last_num_frame = 0
            self.bullet_last_held_long = False
            self.continous_bullets_message = False
        for bullet in self.bullet_list:
            if bullet.alive:
                bullet.update()
            else:
                self.bullet_list.remove(bullet)
        for enem in self.enemies:
            enem.try_to_activate(len(self.enemies))
        for trash in self.trash:
            trash.try_to_activate(101)
        self.monster.try_to_activate(200)

        self.add_enemies()
        self.add_trash()
        self.add_monster()
        self.move_spacecraft()

        if len(self.enemies) < 1 and self.alive and not self.already_won:
            # we can play a victory sound!
            pyxel.stop()
            pyxel.playm(2)
            self.already_won = True
            self.add_message("Yay! We won!")

        if self.bullet_last_num_frame >= self.continous_bullets_delay:
            self.bullet_last_num_frame = 0
            self.bullet_last_held_long = True

    def move_spacecraft(self):
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            # Move up
            self.player_y = max(self.player_y - 2, 10)
            # Resetting bullets back when moved
            self.bullet_last_num_frame = 0
            self.bullet_last_held_long = False
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            # Move down
            self.player_y = min(self.player_y + 2, pyxel.height - 28)
            # Resetting bullets back when moved
            self.bullet_last_num_frame = 0
            self.bullet_last_held_long = False

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
                        self.add_message("Oh no! We loose!")
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
                        self.add_message("Oh no! We loose!")
                else:
                    self.score += random.choice([50, 100, 200])
                    self.trash.pop(item)
                    pyxel.playm(4)
        except Exception:
            # just like the enemies, this will just pass
            pass

    def add_monster(self):
        try:
            if self.monster.alive and self.monster.available:
                self.monster.update(self.bullet_list)
                if self.player_x in range(
                    self.monster.x - 1, self.monster.x + 17
                ) and self.player_y in range(self.monster.y - 1, self.monster.y + 17):
                    self.alive = False
                    pyxel.stop()
                    pyxel.playm(1)
                    self.add_message("Oh no! We loose!")
            elif self.monster.available and self.monster.x > 2:
                self.score += 1000
                self.monster = DeadMonster()
                pyxel.playm(4)
                self.add_message("Oh my! We killed the Monster!")
                self.add_message("The Monster gave us extra points!")
        except Exception:
            pass

    def add_message(self, msg, system=False):
        self.messages.append(f"{'Diddi' if not system else 'System'}: {msg}")
        if len(self.messages) >= 3:
            self.messages.pop(0)

    def draw_message_bar(self):
        # This will draw the messages bar.
        pyxel.rect(0, pyxel.height - 20, pyxel.width, 20, 5)
        pyxel.rect(0, pyxel.height - 20, pyxel.width, 2, 13)

        # Draw the messages
        if len(self.messages) > 0:
            pyxel.text(1, pyxel.height - 17, self.messages[0], 1)
            pyxel.text(2, pyxel.height - 17, self.messages[0], 7)
        if len(self.messages) > 1:
            pyxel.text(1, pyxel.height - 8, self.messages[1], 1)
            pyxel.text(2, pyxel.height - 8, self.messages[1], 7)

    def draw(self):
        pyxel.cls(0)
        score = f"Score: {self.score}"
        enem_count = f"Enemies: {len(self.enemies)}"
        pyxel.text(5, 4, score, 1)
        pyxel.text(4, 4, score, 7)
        pyxel.text(71, 4, enem_count, 1)
        pyxel.text(70, 4, enem_count, 7)
        self.draw_message_bar()
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
            self.monster.draw()
        else:
            # you loose! try again
            pyxel.text(
                21, 50, "Oh no! :( Press R to restart\n or press Q to quit the game", 1
            )
            pyxel.text(
                20, 50, "Oh no! :( Press R to restart\n or press Q to quit the game", 7
            )


App()
