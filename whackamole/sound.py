import pygame


class SoundEffect:
    def __init__(self):
        pygame.mixer.music.load("assets/sounds/intro.mp3")
        pygame.mixer.music.play(-1)
        # self.intro = pygame.mixer.Sound("assets/sounds/intro.mp3")
        self.game_theme = pygame.mixer.Sound("assets/sounds/game_theme.wav")
        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)
        self.channel3 = pygame.mixer.Channel(2)
        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
        self.pop_sound = pygame.mixer.Sound("assets/sounds/pop.mp3")
        self.hurt_sound = pygame.mixer.Sound("assets/sounds/hurt.wav")
        self.miss_sound = pygame.mixer.Sound("assets/sounds/miss.mp3")
        self.hurt_sound.set_volume(.3)


    def play_hit_sound(self):
        self.hit_sound.play()

    def play_miss_sound(self):
        #self.miss_sound.play()
        self.channel1.play(self.miss_sound)

    def play_pop_sound(self):
        self.pop_sound.play()

    def stop_pop_sound(self):
        self.pop_sound.stop()

    def play_hurt_sound(self):
        # self.hurt_sound.play()
        self.channel2.play(self.hurt_sound)
    def stop_hurt_sound(self):
        self.hurt_sound.stop()

    def play_game_theme(self):
        # self.game_theme.play(-1)
        self.channel3.play(self.game_theme)
        pass

    def stop_intro(self):
        pygame.mixer.music.stop()