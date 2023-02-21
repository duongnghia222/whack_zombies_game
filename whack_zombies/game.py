from pygame import init, mixer, font, display, image, transform, time, mouse, event, Surface, \
    SRCALPHA, QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_SPACE, K_ESCAPE

from .constants import Constants
from .zombie import Zombie
from .score import Score
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
        self.screen = display.set_mode((Constants.game_width, Constants.game_height))
        display.set_caption("Whack a Zombie")

        # Load background
        self.img_background = image.load(Constants.image_background)
        self.img_background = transform.scale(self.img_background, (Constants.game_width, Constants.game_height))
        self.img_intro = image.load(Constants.image_intro)
        self.img_intro = transform.scale(self.img_intro, (Constants.game_width, Constants.game_height))
        # Load banner
        self.banner = image.load(Constants.image_banner)
        self.banner = transform.scale(self.banner, (850, 90))

        # Load button
        self.play_button_on = image.load(Constants.image_sound_button_on)
        self.play_button_on = transform.scale(self.play_button_on, (50, 50))
        self.play_button_off = image.load(Constants.image_sound_button_off)
        self.play_button_off = transform.scale(self.play_button_off, (50, 50))

        # Load hole
        self.img_hole = image.load(Constants.image_hole)
        self.img_hole = transform.scale(self.img_hole, (Constants.hole_width, Constants.hole_height))

        # Load hammer
        self.img_hammer = image.load(Constants.image_hammer)
        self.img_hammer = transform.scale(self.img_hammer, (Constants.hammer_width, Constants.hammer_height))

        # Load hit effect
        self.hit_effect = image.load(Constants.image_hit_effect)
        self.hit_effect = transform.scale(self.hit_effect, (840*0.1, 774*0.1))

        # Load miss effect
        self.miss_effect = image.load(Constants.image_miss_effect)
        self.miss_effect = transform.scale(self.miss_effect, (612 * 0.1, 408 * 0.1))

        # Load font
        self.font = font.Font('assets/myFont.ttf', 40)
        self.big_font = font.Font('assets/myFont.ttf', 85)

        display.set_icon(self.img_hammer)

        # Set timer
        self.timer = timer
        self.cool_down_time_for_hammer = 0

        self.game_theme_on = True

        # Load high score
        file = open('high_scores.txt', 'r')
        read_file = file.readlines()
        file.close()
        self.best_scores = int(read_file[0])

        self.zombies = []
        self.holes = []
        self.used_holes = []
        self.score = Score()
        self.show_hit = 0
        self.show_miss = 0
        self.loop = True
        self.clock = time.Clock()
        # Allow for game timer

        self.timer_start = 0
        # Reset/initialise data
        self.reset()

        # Run
        if autostart:
            self.run()

    def reset(self):
        # Load zombies
        self.zombies = [Zombie() for _ in range(Constants.zombie_count)]

        # Generate hole positions
        self.holes = []
        self.used_holes = []
        base_row = Constants.game_height / Constants.hole_row - 50
        base_column = Constants.game_width / Constants.hole_column - 100
        for row in range(Constants.hole_row):
            row_y = base_row * row + 150
            row_y += (base_row - Constants.hole_height) / 2
            for column in range(Constants.hole_column):
                this_x = base_column * column + 200
                this_x += (base_column - Constants.hole_width) / 2
                self.holes.append((int(this_x), int(row_y)))

        # Get the score object
        self.score = Score()

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
            end_game = True if remain <= 0 else False
            return remain, end_game
        return None, False

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

            game_time, end_game = self.timerData

            if not end_game:

                # Handle click
                if e.type == MOUSEBUTTONDOWN and e.button == Constants.left_mouse_button:

                    # Start timer if not started
                    if self.timer is not None and self.timer_start == 0:
                        mixer.music.stop()
                        self.sound_effect.play_game_theme()
                        self.timer_start = time.get_ticks()

                    else:
                        # Handle hit/miss
                        clicked = True
                        miss = True
                        for zombie in self.zombies:
                            if zombie.is_hit(pos) == 1:  # Hit
                                hit = True
                                miss = False
                            if zombie.is_hit(pos) == 2:  # Hit but stunned
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

            # End game screen
            else:
                if e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        # Restart
                        self.reset()
                        break

        return clicked, hit, miss

    def loop_display(self, hit, miss):
        game_time, end_game = self.timerData
        if not game_time and self.timer:
            game_time = -1

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

        time_display = game_time
        if time_display < 0:
            time_display = 0
        points_text = self.font.render("{}".format(round(time_display, 2)), True, 'black')
        self.screen.blit(points_text, (690, 40))

        # Display sound button
        # if self.game_theme_on:
        #     self.screen.blit(self.play_button_off, (700, 30))

        # Display holes
        for position in self.holes:
            self.screen.blit(self.img_hole, position)

        # Display zombies
        for zombie in self.zombies:
            holes = [f for f in self.holes if f not in self.used_holes]
            zombie_display = zombie.do_display(holes, self.score.level, not end_game)

            # If new/old hole given
            if len(zombie_display) > 1:
                if zombie_display[1] == 0:  # New hole
                    self.used_holes.append(zombie_display[2])
                else:  # Old hole
                    if zombie_display[2] in self.used_holes:
                        self.used_holes.remove(zombie_display[2])

            # If should display
            if zombie_display[0]:
                # Get pos and display
                pos = zombie.get_hole_pos(not end_game)
                self.screen.blit(zombie.image, (pos[0] - 15, pos[1]))

        # Hammer
        if time.get_ticks() < self.cool_down_time_for_hammer:
            this_hammer = transform.rotate(self.img_hammer.copy(), Constants.hammer_rotate_angle)
        else:
            this_hammer = transform.rotate(self.img_hammer.copy(), Constants.hammer_normal_angle)

        hammer_x, hammer_y = mouse.get_pos()
        hammer_x -= this_hammer.get_width() / 5
        hammer_y -= this_hammer.get_height() / 4 + 30
        if hammer_y > 40:
            self.screen.blit(this_hammer, (hammer_x, hammer_y))

        # Fade screen if not started or has ended
        if self.timer and end_game:
            overlay = Surface((Constants.game_width, Constants.game_height), SRCALPHA, 32)
            overlay = overlay.convert_alpha()
            overlay.fill((100, 100, 100, 0.9 * 255))
            self.screen.blit(overlay, (0, 0))

        # Display hit/miss indicators
        if not end_game:

            # Hit indicator
            if hit:
                self.show_hit = time.get_ticks()
            if self.show_hit > 0 and time.get_ticks() - self.show_hit <= Constants.zombie_hit_hud:
                hit_x, hit_y = mouse.get_pos()
                self.screen.blit(self.hit_effect, (hit_x - 30, hit_y - 30))
                self.sound_effect.play_bam_sound()
                self.sound_effect.play_hurt_sound()
            else:
                self.show_hit = 0

            # Miss indicator
            if miss:
                self.show_miss = time.get_ticks()
            if self.show_miss > 0 and time.get_ticks() - self.show_miss <= Constants.zombie_miss_hud:
                miss_x, miss_y = mouse.get_pos()
                self.screen.blit(self.miss_effect, (miss_x, miss_y))
                self.sound_effect.play_miss_sound()
            else:
                self.show_miss = 0

        # Click to start indicator
        if self.timer and game_time == -1:
            self.screen.blit(self.img_intro, (0, 0))
            best_scores = self.big_font.render("{}".format(self.best_scores), True, 'black')
            self.screen.blit(best_scores, (660, 380))

        # Time's up indicator
        if self.timer and end_game:
            temp_best_score = int(self.score.show_score())
            if temp_best_score > self.best_scores:
                self.best_scores = temp_best_score
                file = open('high_scores.txt', 'w')
                file.write(f'{temp_best_score}')
                file.close()

            text = self.big_font.render("Time's up!", True, 'black')
            text1 = self.font.render("Press space to restart...", True, 'black')
            text2 = self.font.render("Your Score: {}".format(temp_best_score), True, 'black')

            self.screen.blit(text, (250, 80))
            self.screen.blit(text2, (250, 250))
            self.screen.blit(text1, (250, 400))

    def start(self):
        self.clock = time.Clock()
        self.loop = True

        while self.loop:
            # Do all events
            clicked, hit, miss = self.loop_events()
            if clicked:
                self.cool_down_time_for_hammer = time.get_ticks() + 50
            # Do all render
            self.loop_display(hit, miss)

            # Update display
            self.clock.tick(Constants.game_max_fps)
            display.flip()

    def run(self):
        self.start()
        quit()
