import pygame


class SoundEffect:
    def __init__(self):
        self.play_music = True
        pygame.mixer.music.load("assets/sounds/intro.mp3")
        pygame.mixer.music.play(-1)
        self.game_theme = pygame.mixer.Sound("assets/sounds/game_theme.wav")
        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)
        self.channel3 = pygame.mixer.Channel(2)
        self.channel4 = pygame.mixer.Channel(3)
        self.hurt_sound = pygame.mixer.Sound("assets/sounds/hurt.wav")
        self.miss_sound = pygame.mixer.Sound("assets/sounds/miss.mp3")
        self.bam_sound = pygame.mixer.Sound("assets/sounds/bam.mp3")
        self.hurt_sound.set_volume(.5)

    def play_miss_sound(self):
        self.channel1.play(self.miss_sound)

    def play_hurt_sound(self):
        self.channel2.play(self.hurt_sound)

    def play_bam_sound(self):
        self.channel4.play(self.bam_sound)

    def play_game_theme(self):
        self.channel3.play(self.game_theme)
        pass


def stop_intro():
    pygame.mixer.music.stop()
