"""
The piece of code that puts everything together.
"""

import random
import sys

import pyxel

# When bumping to a higher Python requirement, please
# modify this varible, basically to avoid users from
# running with an old Python.
EXPECTED_PYTHON = (3, 8)

if sys.version_info < EXPECTED_PYTHON:
    sys.exit(
        f"Error: expected Python version {EXPECTED_PYTHON} or newer, got {sys.version_info}"
    )

pyxel.init(180, 140, title="Diddi and the Bugs")

# We have set the "Z-move animation time" to 20
# frames. This means the special effect will last
# 20 frames, and then everything will turn back to normal.
Z_ANIMATION_TIME = 20


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
    # We've put this outside of __init__
    # to avoid issues with instances.
    z_killed = -1

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
            if self.bullet_collision(bullet):
                if hasattr(self, "hit_count"):
                    if self.hit_count == 2:
                        self.alive = False
                    else:
                        self.hit_count += 1
                else:
                    self.alive = False
                bullet.alive = False

    def draw_z(self):
        # Special func for drawing a z-killed
        # enemy... We draw a certain image
        pyxel.blt(self.x, self.y, 0, 40, 24, self.size, self.size, 0)

    def draw(self):
        if not self.show and self.z_killed < 0:
            return None
        if self.alive and self.z_killed < 0:
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
        if (
            pyxel.frame_count < (self.z_killed + Z_ANIMATION_TIME + 10)
            and not self.alive
        ):
            # print("Z-Move Graphics here?")  # test
            self.draw_z()

    def bullet_collision(self, bullet):
        return (
            self.x in range(bullet.x - 5, bullet.x + bullet.w + 5)
            and self.y in range(bullet.y - 5, bullet.y + bullet.h + 5)
            and bullet.alive
        )

    def hit_special_move(self):
        self.alive = False
        self.z_killed = pyxel.frame_count


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
        self.possible_enemies = [(48, 0), (48, 16)]
        self.aspect = self.possible_enemies[
            0
        ]  # there's only one aspect, no need to choose
        self.x = pyxel.width
        self.y = random.randint(10, pyxel.height - 28)
        self.max_speed = 6  # it can move *really* fast, or maybe not!
        self.speed = random.randint(1, self.max_speed)
        self.alive = True
        self.hit_count = 0
        self.show = False
        self.size = 16  # 16p per side, 4x4 blocks in the Pyxel editor
        self.recycle = False  # don't regenerate after reaching x=0
        self.available = (
            True  # this unique attribute will make the difference from the dead monster
        )

    def bullet_collision(self, bullet):
        # Adapt the bullet collision logic, so any
        # bullet that hits the monster's space will
        # raise a collision, instead of just passing
        return (
            self.x in range(bullet.x - 5, bullet.x + bullet.w + 5)
            and (
                self.y in range(bullet.y - 15, bullet.y + bullet.h + 15)
                if self.y <= (bullet.y + 2) and bullet.y <= (self.y + 17)
                else False
            )
            and bullet.alive
        )

    def hit_special_move(self):
        self.hit_count += 1

    def draw_z(self):
        pass

    def draw(self):
        # We fixed this function to add
        # an extra look when hit_count == 1.
        if self.hit_count == 1:
            # TODO: Find a better place to do this?
            self.aspect = self.possible_enemies[1]
        Enemy.draw(self)


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


class Star:
    "A star, that works behind the background."

    def __init__(self):
        self.x = pyxel.width
        self.y = random.randint(1, pyxel.height - 21)
        self.show = False
        self.alive = True
        self.speed = random.randint(1, 6)

    def try_to_activate(self, possibilities):
        if possibilities > 100:
            exp = 15
        elif possibilities > 50:
            exp = 10
        else:
            exp = 5
        if random.randint(1, possibilities * exp) == 1:
            self.show = True

    def update(self):
        self.try_to_activate(random.choice([k + 1 for k in range(150)]))

        if self.show:
            self.x -= self.speed
        if self.x == 0:
            self.alive = False

    def draw(self):
        if self.show:
            # ... draw here ...
            pyxel.pset(self.x, self.y, 7)


class App:
    "The main piece of the game. It also operates the starfighter."

    def __init__(self):
        # This variable is not on `reset`, because
        # we are keeping a message record until
        # the app quits.
        self.messages = []

        self.skins = ["resource.pyxres", "resource_2.pyxres"]
        self.current_skin = 0

        pyxel.load(self.skins[self.current_skin])

        self.message_goodies = [
            "Woo hoo!",
            "Let's save the Earth!",
            "Find the 'easter eggs'!",
            "Willpower to Earth, can you hear me?",
            "Hang tight...",
            "I'm hungry, aren't you?",
            "It's cold here, don't you think?",
            "Wow! This spacecraft really moves!",
            "Fire! Fire! Fire!",
        ]

        self.on_menu = True  # variable to show the menu

        self.z_frame = -5  # a variable used in gameplay

        self.startup()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.alive = True  # the player is still alive
        self.already_won = False
        self.used_special_move = False
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
        self.stars = [Star() for sth in range(100)]
        self.z_frame = -5

        pyxel.stop()
        pyxel.playm(0, loop=True)

    def reset_menu(self):
        # match the real behavior
        self.menu_enemies = [Enemy() for sth in range(200)]
        self.menu_trash = [Trash() for sth in range(50)]
        self.menu_monster = Monster()
        self.menu_stars = [Star() for sth in range(100)]

        self.menu_credits = False  # If True, display the credits
        self.menu_skin = False

        # This is the credits' text
        self.credits_text = """This game was created by Diego Ramirez.\n
This game is also possible thanks to
other contributors, whose names can be found
at github.com/DiddiLeija/diddi-and-the-bugs
(look for the THANKS.txt file).
        """

        pyxel.stop()
        pyxel.playm(6, loop=True)

    def startup(self):
        if self.on_menu:
            self.reset_menu()
        else:
            self.reset_game()
            self.add_message("Let's go!")

    def update(self):
        if self.on_menu:
            self.update_menu()
        else:
            self.update_game()

    def draw(self):
        if self.on_menu:
            self.draw_menu()
        else:
            self.draw_game()

    def update_game(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.on_menu = True
            self.startup()
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

        if pyxel.btnr(pyxel.KEY_Z):
            if self.used_special_move:
                self.add_message("You have already used the Z-Move", True)
                return
            z_affected = 0
            self.used_special_move = True
            self.z_frame = pyxel.frame_count
            self.add_message("Go Ahead! Z-Move Activated")
            # some cool animations
            for enem in self.enemies:
                if enem.alive and enem.show:
                    enem.hit_special_move()
                    z_affected += 1

            if self.monster.show and self.monster.alive:
                self.monster.hit_special_move()
                self.add_message("Yeah! Z-Move Hit The Monster")
                z_affected += 1

            # Check if somebody was affected and play the sound effects
            if z_affected > 0:
                pyxel.playm(7)

        # Kill all those stars who left the screen
        for star_pos in range(len(self.stars)):
            try:
                if not self.stars[star_pos].alive:
                    self.stars.pop(star_pos)
            except IndexError:
                # Just break, no more items are available
                break
        # If no more stars are available, just create more
        if len(self.stars) < 20:
            self.stars += [Star() for sth in range(80)]  # ~= 100 stars?

        for bullet in self.bullet_list:
            if bullet.alive:
                bullet.update()
            else:
                self.bullet_list.remove(bullet)
        for enem in self.enemies:
            enem.try_to_activate(len(self.enemies))
        for trash in self.trash:
            trash.try_to_activate(101)
        self.monster.try_to_activate(202)

        self.add_enemies()
        self.add_trash()
        self.add_monster()
        self.move_spacecraft()

        for star in self.stars:
            star.update()

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
                pyxel.playm(5)
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

    def draw_player(self):
        # A spec for drawing the player's
        # spacecraft during gameplay.
        if (
            self.used_special_move
            and pyxel.frame_count < self.z_frame + Z_ANIMATION_TIME
        ):
            pyxel.blt(self.player_x, self.player_y, 0, 40, 16, 8, 8, 0)
        else:
            pyxel.blt(self.player_x, self.player_y, 0, 8, 0, 8, 8, 0)

    def draw_game(self):
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
                20,
                50,
                " You won! :) Press R to return\n or press Q to quit the game",
                1,
            )
            pyxel.text(
                19,
                50,
                " You won! :) Press R to return\n or press Q to quit the game",
                7,
            )
        elif self.alive:
            # the show is keep going!
            for star in self.stars:
                star.draw()
            self.draw_player()
            for bullet in self.bullet_list:
                bullet.draw()
            for enem in self.enemies:
                enem.draw()
            for trash in self.trash:
                trash.draw()
            self.monster.draw()
        else:
            # you lost! try again
            pyxel.text(
                20, 50, " Oh no! :( Press R to return \n or press Q to quit the game", 1
            )
            pyxel.text(
                19, 50, " Oh no! :( Press R to return \n or press Q to quit the game", 7
            )

    def update_menu(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if not self.menu_credits and not self.menu_skin:
            if pyxel.btnp(pyxel.KEY_1) or pyxel.btnp(pyxel.KEY_KP_1):
                # Option 1 -- Start the game
                self.on_menu = False
                self.startup()
            if pyxel.btnp(pyxel.KEY_2) or pyxel.btnp(pyxel.KEY_KP_2):
                # Option 2 -- Display credits
                self.menu_credits = True
            if pyxel.btnp(pyxel.KEY_3) or pyxel.btnp(pyxel.KEY_KP_3):
                # Option 3 -- Choose the Skin
                self.menu_skin = True
        if self.menu_credits and pyxel.btnp(pyxel.KEY_SPACE):
            # Escape from option 2
            self.menu_credits = False
        if self.menu_skin:
            if pyxel.btnp(pyxel.KEY_SPACE):
                # Escape from option 3
                self.menu_skin = False
            if pyxel.btnp(pyxel.KEY_1) or pyxel.btnp(pyxel.KEY_KP_1):
                # Load resource 1
                self.current_skin = 0
                pyxel.load(self.skins[self.current_skin])
            if pyxel.btnp(pyxel.KEY_2) or pyxel.btnp(pyxel.KEY_KP_2):
                # Load resource 2
                self.current_skin = 1
                pyxel.load(self.skins[self.current_skin])
        # Kill all those stars who left the screen
        for star_pos in range(len(self.menu_stars)):
            try:
                if not self.menu_stars[star_pos].alive:
                    self.menu_stars.pop(star_pos)
            except IndexError:
                # Just break, no more items are available
                break
        # If no more stars are available, just create more
        if len(self.menu_stars) < 20:
            self.menu_stars += [Star() for sth in range(80)]  # ~= 100 stars?
        # Try to activate the enemies and the stars, using
        # the strategy that's used in the real game.
        for enem in self.menu_enemies:
            enem.try_to_activate(len(self.menu_enemies))
        for trash in self.menu_trash:
            trash.try_to_activate(101)
        self.menu_monster.try_to_activate(202)
        for star in self.menu_stars:
            star.update()
        # Move the enemies behind the screen.
        # These are shorter versions of add_monster(),
        # add_trash() and add_enemies(). The use of
        # self.bullet_list is replaced by an empty list.
        try:
            if self.menu_monster.alive and self.menu_monster.available:
                self.menu_monster.update([])
            for item in range(len(self.menu_trash)):
                if self.menu_trash[item].alive:
                    self.menu_trash[item].update([])
            for item in range(len(self.menu_enemies)):
                if self.menu_enemies[item].alive:
                    self.menu_enemies[item].update([])
        except Exception:
            pass

    def draw_menu(self):
        # Draw the screen
        pyxel.cls(0)
        # Draw stars
        for star in self.menu_stars:
            star.draw()
        # Draw the characters that play
        for enem in self.menu_enemies:
            enem.draw()
        for trash in self.menu_trash:
            trash.draw()
        self.menu_monster.draw()
        if not self.menu_credits and not self.menu_skin:
            # Intro text
            pyxel.text(26, 25, "=== Diddi and the Bugs ===", 1)
            pyxel.text(25, 25, "=== Diddi and the Bugs ===", 7)
            # Option 1
            pyxel.text(26, 35, "[1] Start game", 1)
            pyxel.text(25, 35, "[1] Start game", 7)
            # Option 2
            pyxel.text(26, 45, "[2] Credits", 1)
            pyxel.text(25, 45, "[2] Credits", 7)
            # Option 3
            pyxel.text(26, 55, "[3] Choose Skin", 1)
            pyxel.text(25, 55, "[3] Choose Skin", 7)
        elif self.menu_credits:
            # Show the credits...
            # Intro text
            pyxel.text(16, 25, "=== Credits of Diddi and the Bugs ===", 1)
            pyxel.text(15, 25, "=== Credits of Diddi and the Bugs ===", 7)
            # Credits text
            pyxel.text(6, 35, self.credits_text, 1)
            pyxel.text(5, 35, self.credits_text, 7)
            # Escape option
            pyxel.text(26, 95, "Press SPACE to return", 1)
            pyxel.text(25, 95, "Press SPACE to return", 7)
        elif self.menu_skin:
            # Choose the skin...
            # Intro text
            pyxel.text(16, 25, "=== Choose A Skin Pack ===", 1)
            pyxel.text(15, 25, "=== Choose A Skin Pack ===", 7)
            # Skin A
            pyxel.text(26, 35, "[1] Skin A" + ("<-" if self.current_skin == 0 else ""), 1)
            pyxel.text(25, 35, "[1] Skin A" + ("<-" if self.current_skin == 0 else ""), 7)
            # Skin B
            pyxel.text(26, 45, "[2] Skin B" + ("<-" if self.current_skin == 1 else ""), 1)
            pyxel.text(25, 45, "[2] Skin B" + ("<-" if self.current_skin == 1 else ""), 7)
            # Escape option
            pyxel.text(26, 95, "Press SPACE to return", 1)
            pyxel.text(25, 95, "Press SPACE to return", 7)
        # Quit option
        pyxel.text(26, 105, "Press Q to quit", 1)
        pyxel.text(25, 105, "Press Q to quit", 7)


App()
