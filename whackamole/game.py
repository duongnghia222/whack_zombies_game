# -*- coding: utf-8 -*-

"""
Whack a Mole
~~~~~~~~~~~~~~~~~~~
A simple Whack a Mole game written with PyGame
:copyright: (c) 2018 Matt Cowley (IPv4)
"""
import random

from pygame import init, mixer, font, display, image, transform, time, mouse, event, Surface, \
    SRCALPHA, QUIT, MOUSEBUTTONDOWN, KEYDOWN, \
    K_e, K_r, K_t, K_y, K_u, K_i, K_o, K_p, K_SPACE, K_ESCAPE

from .constants import Constants
from .mole import Mole
from .score import Score
from .text import Text
from .sound import SoundEffect


class Game:
    """
    Handles the main game
    Takes :time: in seconds for game timer
    """

    def __init__(self, *, timer: int = None, autostart: bool = True):
        # Init pygame
        init()
        mixer.init()
        self.sound_effect = SoundEffect()
        # Create pygame screen
        self.screen = display.set_mode((Constants.GAMEWIDTH, Constants.GAMEHEIGHT))
        display.set_caption(Constants.TEXTTITLE)


        # Load background
        self.img_background = image.load(Constants.IMAGEBACKGROUND)
        self.img_background = transform.scale(self.img_background, (Constants.GAMEWIDTH, Constants.GAMEHEIGHT))
        self.img_intro = image.load(Constants.image_intro)
        self.img_intro = transform.scale(self.img_intro, (Constants.GAMEWIDTH, Constants.GAMEHEIGHT))
        # Load banner
        self.banner = image.load(Constants.image_banner)
        self.banner = transform.scale(self.banner, (850, 90))

        # Load button
        self.play_button = image.load(Constants.IMAGEPLAYBUTTON)
        self.play_button = transform.scale(self.play_button, (100, 100))
        self.play_button_on = image.load(Constants.image_sound_button_on)
        self.play_button_on = transform.scale(self.play_button_on, (50, 50))
        self.play_button_off = image.load(Constants.image_sound_button_off)
        self.play_button_off = transform.scale(self.play_button_off, (50, 50))

        # Load hole
        self.img_hole = image.load(Constants.IMAGEHOLE)
        self.img_hole = transform.scale(self.img_hole, (Constants.HOLEWIDTH, Constants.HOLEHEIGHT))

        # Load mallet
        self.img_mallet = image.load(Constants.IMAGEMALLET)
        self.img_mallet = transform.scale(self.img_mallet, (Constants.MALLETWIDTH, Constants.MALLETHEIGHT))

        # Load hit effect
        self.hit_effect = image.load(Constants.IMAGEHITEFFECT)
        self.hit_effect = transform.scale(self.hit_effect, (840*0.1, 774*0.1))

        # Load miss effect
        self.miss_effect = image.load(Constants.IMAGEMISSEFFECT)
        self.miss_effect = transform.scale(self.miss_effect, (612 * 0.1, 408 * 0.1))

        # Load font
        self.font = font.Font('assets/myFont.ttf', 40)
        self.big_font = font.Font('assets/myFont.ttf', 85)

        display.set_icon(self.img_mallet)

        # Set timer
        self.timer = timer
        self.cool_down_time_for_hammer = 0

        self.game_theme_on = True

        # Load high score
        file = open('high_scores.txt', 'r')
        read_file = file.readlines()
        file.close()
        self.best_scores = int(read_file[0])
        print(self.best_scores)
        # Reset/initialise data
        self.reset()

        # Run
        if autostart:
            self.run()

    def reset(self):

        # Load moles
        self.moles = [Mole() for _ in range(Constants.MOLECOUNT)]

        # Generate hole positions
        self.holes = []
        self.used_holes = []
        base_row = Constants.GAMEHEIGHT / Constants.HOLEROWS - 50
        base_column = Constants.GAMEWIDTH / Constants.HOLECOLUMNS - 100
        for row in range(Constants.HOLEROWS):
            rowY = base_row * row + 150
            rowY += (base_row - Constants.HOLEHEIGHT) / 2
            for column in range(Constants.HOLECOLUMNS):
                thisX = base_column * column + 200
                thisX += (base_column - Constants.HOLEWIDTH) / 2
                self.holes.append((int(thisX), int(rowY)))

        # Get the text object
        self.text = Text()

        # Get the score object
        self.score = Score(self.text)

        # Indicates whether the HUD indicators should be displayed
        self.show_hit = 0
        self.show_miss = 0

        # Allow for game timer
        self.timer_start = 0

    @property
    def timerData(self):
        if self.timer is not None and self.timer_start != 0:
            remain = (time.get_ticks() - self.timer_start) / 1000
            remain = self.timer - remain
            endGame = True if remain <= 0 else False
            return (remain, endGame)
        return (None, False)

    def loop_events(self):

        hit = False
        miss = False
        clicked = False
        pos = mouse.get_pos()

        # Handle PyGame events
        for e in event.get():

            # Handle quit
            if e.type == QUIT:
                self.loop = False
                break

            gameTime, endGame = self.timerData

            if not endGame:

                # Handle click
                if e.type == MOUSEBUTTONDOWN and e.button == Constants.LEFTMOUSEBUTTON:

                    # Start timer if not started
                    if self.timer is not None and self.timer_start == 0:
                        mixer.music.stop()
                        self.sound_effect.play_game_theme()
                        self.timer_start = time.get_ticks()

                    else:
                        # Handle hit/miss
                        clicked = True
                        miss = True
                        for mole in self.moles:
                            if mole.is_hit(pos) == 1:  # Hit
                                hit = True
                                miss = False
                            if mole.is_hit(pos) == 2:  # Hit but stunned
                                miss = False

                        if hit:
                            self.score.hit()
                        if miss:
                            self.score.miss()

                if e.type == KEYDOWN:

                    # Allow escape to abort attempt
                    if e.key == K_ESCAPE:
                        self.reset()
                        break

                    # Handle cheats (for dev work)
                    if Constants.DEBUGMODE:
                        if e.key == K_e:
                            hit = True
                            miss = False
                            self.score.hit()
                        if e.key == K_r:
                            hit = False
                            miss = True
                            self.score.miss()

                        if e.key == K_t:
                            self.score.misses = 0
                        if e.key == K_y:
                            self.score.misses += 5
                        if e.key == K_u:
                            self.score.misses -= 5

                        if e.key == K_i:
                            self.score.hits = 0
                        if e.key == K_o:
                            self.score.hits += 5
                        if e.key == K_p:
                            self.score.hits -= 5

            # End game screen
            else:
                if e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        # Restart
                        self.reset()
                        break

        return (clicked, hit, miss)

    def loop_display(self, clicked, hit, miss):
        gameTime, endGame = self.timerData
        if not gameTime and self.timer:
            gameTime = -1

        # Display bg
        self.screen.blit(self.img_background, (0, 0))

        # Display banner
        self.screen.blit(self.banner, (0, 0))

        # Display text
        # points_text = self.font.render(f'Points: {self.timer}', True, 'black')
        points_text = self.font.render(self.score.show_score(), True, 'black')
        self.screen.blit(points_text, (70, 40))

        points_text = self.font.render(self.score.show_hits(), True, 'black')
        self.screen.blit(points_text, (270, 40))

        points_text = self.font.render(self.score.show_misses(), True, 'black')
        self.screen.blit(points_text, (470, 40))

        points_text = self.font.render("{}".format(round(gameTime, 2)), True, 'black')
        self.screen.blit(points_text, (690, 40))

        # Display sound button
        # if self.game_theme_on:
        #     self.screen.blit(self.play_button_off, (700, 30))

        # Display holes
        for position in self.holes:
            self.screen.blit(self.img_hole, position)

        # Display moles
        for mole in self.moles:
            holes = [f for f in self.holes if f not in self.used_holes]
            mole_display = mole.do_display(holes, self.score.level, not endGame)

            # If new/old hole given
            if len(mole_display) > 1:
                if mole_display[1] == 0:  # New hole
                    self.used_holes.append(mole_display[2])
                else:  # Old hole
                    if mole_display[2] in self.used_holes:
                        self.used_holes.remove(mole_display[2])

            # If should display
            if mole_display[0]:
                # Get pos and display
                pos = mole.get_hole_pos(not endGame)
                self.screen.blit(mole.image, pos)

        # Hammer
        if time.get_ticks() < self.cool_down_time_for_hammer:
            thisHammer = transform.rotate(self.img_mallet.copy(), Constants.MALLETROTHIT )
        else:
            thisHammer = transform.rotate(self.img_mallet.copy(), Constants.MALLETROTNORM )

        hammer_x, hammer_y = mouse.get_pos()
        hammer_x -= thisHammer.get_width() / 5
        hammer_y -= thisHammer.get_height() / 4 + 30
        if hammer_y > 40:
            self.screen.blit(thisHammer, (hammer_x, hammer_y))

        # Fade screen if not started or has ended
        if self.timer and (endGame or gameTime == -1):
            overlay = Surface((Constants.GAMEWIDTH, Constants.GAMEHEIGHT), SRCALPHA, 32)
            overlay = overlay.convert_alpha()
            overlay.fill((100, 100, 100, 0.9 * 255))
            self.screen.blit(overlay, (0, 0))

        # Debug data for readout
        debug_data = {}
        if Constants.DEBUGMODE:
            debug_data = {
                "DEBUG": True,
                "FPS": int(self.clock.get_fps()),
                "MOLES": "{}/{}".format(Constants.MOLECOUNT, Constants.HOLEROWS * Constants.HOLECOLUMNS),
                "KEYS": "E[H]R[M]T[M0]Y[M+5]U[M-5]I[H0]O[H+5]P[H-5]"
            }

        # Display data readout
        # data = self.score.label(timer=gameTime, debug=debug_data, size=(1.5 if endGame else 1))
        # self.screen.blit(data, (5, 5))

        # Display hit/miss indicators
        if not endGame:

            # Hit indicator
            if hit:
                self.show_hit = time.get_ticks()
            if self.show_hit > 0 and time.get_ticks() - self.show_hit <= Constants.MOLEHITHUD:
                hit_x, hit_y = mouse.get_pos()
                self.screen.blit(self.hit_effect, (hit_x - 30, hit_y - 30))
                self.sound_effect.play_bam_sound()
                self.sound_effect.play_hurt_sound()
            else:
                self.show_hit = 0

            # Miss indicator
            if miss:
                self.show_miss = time.get_ticks()
            if self.show_miss > 0 and time.get_ticks() - self.show_miss <= Constants.MOLEMISSHUD:
                miss_x, miss_y = mouse.get_pos()
                self.screen.blit(self.miss_effect, (miss_x, miss_y))
                self.sound_effect.play_miss_sound()
            else:
                self.show_miss = 0

        # Click to start indicator
        if self.timer and gameTime == -1:
            self.screen.blit(self.img_intro, (0, 0))
            best_scores = self.big_font.render("{}".format(self.best_scores), True, 'black')
            self.screen.blit(best_scores, (660, 380))

        # Time's up indicator
        if self.timer and endGame:
            temp_best_score = int(self.score.show_score())
            if temp_best_score > self.best_scores:
                file = open('high_scores.txt', 'w')
                file.write(f'{temp_best_score}')
                file.close()
            timer_label_1 = self.text.get_label("Time's up!", scale=3, color=(0, 150, 255))
            timer_label_2 = self.text.get_label("Press space to restart...", scale=2, color=(0, 150, 255))

            timer_x_1 = (Constants.GAMEWIDTH - timer_label_1.get_width()) / 2
            timer_x_2 = (Constants.GAMEWIDTH - timer_label_2.get_width()) / 2

            timer_y_1 = (Constants.GAMEHEIGHT / 2) - timer_label_1.get_height()
            timer_y_2 = (Constants.GAMEHEIGHT / 2)

            self.screen.blit(timer_label_1, (timer_x_1, timer_y_1))
            self.screen.blit(timer_label_2, (timer_x_2, timer_y_2))

    def start(self):
        self.clock = time.Clock()
        self.loop = True

        while self.loop:
            # Do all events
            clicked, hit, miss = self.loop_events()
            if clicked:
                self.cool_down_time_for_hammer = time.get_ticks() + 50
            # Do all render
            self.loop_display(clicked, hit, miss)

            # Update display
            self.clock.tick(Constants.GAMEMAXFPS)
            display.flip()

    def run(self):
        self.start()
        quit()
