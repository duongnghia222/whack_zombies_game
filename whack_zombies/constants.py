class GameConstants:
    """
    Constants used for rendering of main game
    """
    game_width = int(1000 * 0.85)
    game_height = int(600 * 0.85)
    game_max_fps = 60


class LevelConstants:
    """
    Constants used to handle leveling
    """

    level_gap = 10  # score
    level_zombie_speed = 5  # % faster
    level_zombie_chance = 10  # % less


class HoleConstants:
    """
    Constants used in the holes
    """

    hole_width = 100
    hole_height = int(hole_width * (3 / 8))
    hole_row = 3  # !!
    hole_column = 3  # !!

    # Checks
    if hole_height * hole_row > GameConstants.game_height:
        raise ValueError("hole_row or hole_height too high (or game_height too small)")
    if hole_width * hole_column > GameConstants.game_width:
        raise ValueError("hole_column or hole_width too high (or game_width too small)")


class ZombieConstants:
    """
    Constants used for zombie_ generation and calculations
    """

    zombie_width = int(HoleConstants.hole_width * (2 / 3))
    zombie_height = int(zombie_width)
    zombie_depth = 15  # % of _height
    zombie_cooldown = 500  # ms

    zombie_stunned = 1000  # ms
    zombie_hit_hud = 500  # ms
    zombie_miss_hud = 250  # ms

    zombie_chance = 1 / 30
    zombie_count = 2  # !!
    zombie_up_min = 0.3  # s
    zombie_up_max = 2  # s

    # Checks
    if zombie_count > HoleConstants.hole_row * HoleConstants.hole_column:
        raise ValueError("zombie_COUNT too high")


class ImageConstants:
    """
    Constants that are image_ based
    """

    image_base = "assets/"

    image_background = image_base + "background1.jpg"

    image_zombie_normal = image_base + "zombie_rm.png"
    image_zombie_hit = image_base + "zombie_hit_rm.png"

    image_hole = image_base + "hole2.png"
    image_hammer = image_base + "hammer_rm.png"
    image_hit_effect = image_base + "hit_effect_rm.png"
    image_miss_effect = image_base + "miss_effect_rm.png"
    image_play_button = image_base + "button_play.png"
    image_sound_button_on = image_base + "button_sound-on.png"
    image_sound_button_off = image_base + "button_sound-off.png"
    image_banner = image_base + "banner.png"
    image_intro = image_base + "intro_img.png"


class HammerConstants:
    """
    Constants used for rendering the hammer
    """

    hammer_width = int(HoleConstants.hole_width)
    hammer_height = int(hammer_width)

    hammer_normal_angle = 15
    hammer_rotate_angle = 60


class Constants(GameConstants, LevelConstants, HoleConstants, ZombieConstants, ImageConstants,
                HammerConstants):
    """
    Stores all the constants used in the game
    """
    left_mouse_button = 1
