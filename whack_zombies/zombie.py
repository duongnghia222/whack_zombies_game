from random import randint, choice

from pygame import image, transform, time

from .constants import ImageConstants, ZombieConstants, LevelConstants, HoleConstants


class Zombie:
    """
    Provides the zombie used in game
    """

    def __init__(self):
        # Load images
        self.img_normal = image.load(ImageConstants.image_zombie_normal)
        self.img_normal = transform.scale(self.img_normal, (ZombieConstants.zombie_width,
                                                            ZombieConstants.zombie_height))
        self.img_hit = image.load(ImageConstants.image_zombie_hit)
        self.img_hit = transform.scale(self.img_hit, (ZombieConstants.zombie_width, ZombieConstants.zombie_height))

        # State of showing animation
        # 0 = No, 1 = Doing Up, -1 = Doing Down
        self.showing_state = 0

        # Hold timestamp for staying up
        self.showing_counter = 0

        # Hold how long zombie will stay up
        self.show_time = 0

        # Our current hole data
        self.current_hole = (0, 0)
        self.last_hole = (0, 0)

        # Current frame of showing animation
        self.show_frame = 0

        # Total number of frames to show for popping up (not timed)
        self.frames = 12

        # Cooldown from last popup
        self.cooldown = 0

        # Indicates if zombie is hit
        # False = Not hit, timestamp for stunned freeze (boolean / int)
        self.hit = False

    @property
    def image(self):
        if self.hit:
            return self.img_hit
        return self.img_normal

    def do_display(self, holes, level, do_tick=True):
        # If in cooldown
        if self.cooldown:
            if time.get_ticks() - self.cooldown < ZombieConstants.zombie_cooldown:
                return [False]
            else:
                self.cooldown = 0
                return [False, 1, self.last_hole]

        # If doing a tick
        if do_tick:
            # Random choice if not showing
            new_hole = False
            if self.showing_state == 0 and holes:  # if zombie is not appearing
                # Reset
                self.show_frame = 0
                self.hit = False

                # Pick a hole
                # print(chance(level))
                random = randint(0, chance(level))
                if random == 0:
                    self.showing_state = 1
                    self.showing_counter = 0

                    self.show_time = randint(*time_limits(level))

                    # Pick a new hole, don't pick the last one, don't infinite loop
                    self.current_hole = self.last_hole
                    if len(holes) > 1 or self.current_hole != holes[0]:
                        while self.current_hole == self.last_hole:
                            self.current_hole = choice(holes)
                        self.last_hole = self.current_hole
                        new_hole = True

            # Show as popped up for a bit
            if self.showing_state == 1 and self.showing_counter != 0:
                if time.get_ticks() - self.showing_counter >= self.show_time:
                    self.showing_state = -1
                    self.showing_counter = 0

            # Return if game should display, including new hole data
            if new_hole:
                return [True, 0, self.current_hole]

        # Return if game should display
        return [self.showing_state != 0]

    def get_base_pos(self):
        hole_x, hole_y = self.current_hole
        offset = (HoleConstants.hole_width - ZombieConstants.zombie_width) / 2

        zombie_x = hole_x + offset
        zombie_y = (hole_y + HoleConstants.hole_height) - (ZombieConstants.zombie_height * 1.2)
        return zombie_x, zombie_y

    def get_hole_pos(self, do_tick=True):
        zombie_x, zombie_y = self.get_base_pos()

        frame = 0

        # Stunned
        if self.hit:
            if time.get_ticks() - self.hit >= ZombieConstants.zombie_stunned:
                # Unfrozen after hit, hide
                if self.showing_state != 0:
                    self.showing_state = -1
            else:
                # Frozen from hit
                do_tick = False

        # Going Up
        if self.showing_state == 1:
            if self.show_frame <= self.frames:
                frame = ZombieConstants.zombie_depth / self.frames * (self.frames - self.show_frame)
                if do_tick:
                    self.show_frame += 1
            else:
                # Hold
                if self.showing_counter == 0:
                    self.showing_counter = time.get_ticks()

        # Going Down
        if self.showing_state == -1:
            if do_tick:
                self.show_frame -= 1
            if self.show_frame >= 0:
                frame = ZombieConstants.zombie_depth / self.frames * (self.frames - self.show_frame)
            else:
                # Reset
                self.showing_state = 0
                frame = ZombieConstants.zombie_depth
                # Begin cooldown
                if do_tick:
                    self.cooldown = time.get_ticks()

        zombie_y += (ZombieConstants.zombie_height * (frame / 100))

        return zombie_x, zombie_y

    def is_hit(self, pos):
        mouse_x, mouse_y = pos

        # Top Left
        zombie_x1, zombie_y1 = self.get_hole_pos(False)
        # Bottom Right
        zombie_x2, zombie_y2 = (zombie_x1 + ZombieConstants.zombie_width, zombie_y1 + ZombieConstants.zombie_height)

        # Check is in valid to-be hit state
        if self.showing_state != 0:
            # Check x
            if zombie_x1 - 30 <= mouse_x <= zombie_x2:
                # Check y
                if zombie_y1 - 20 <= mouse_y <= zombie_y2:
                    # Check is not stunned
                    if self.hit is False:
                        self.hit = time.get_ticks()
                        return 1
                    else:
                        return 2
        return False


def time_limits(level):
    level -= 1  # Start at 0
    level_time = 1 - ((LevelConstants.level_zombie_speed / 100) * level)
    if level_time < 0:
        level_time = 0  # No wait, just up & down
    time_min = int(ZombieConstants.zombie_up_min * 1000 * level_time)
    time_max = int(ZombieConstants.zombie_up_max * 1000 * level_time)
    return time_min, time_max


def chance(level):
    level -= 1  # Start at 0
    level_chance = 1 + ((LevelConstants.level_zombie_chance / 100) * level)
    chance_ = int((ZombieConstants.zombie_chance ** -1) * level_chance)
    return chance_
