from dataclasses import dataclass
import pygame

COLLISION = pygame.USEREVENT + 1
CHECKPOINT = pygame.USEREVENT + 2
FINISH = pygame.USEREVENT + 3

@dataclass 
class Point:
    x: float = 0
    y: float = 0

@dataclass 
class Track:
    directory: str
    starting_point: Point
    starting_angle: int = 0

maps = { 
    "oval": Track("./tracks/oval/", Point(880, 400), 180),
    "stadium" : Track("./tracks/stadium/", Point(350,170), 90),
 }

class Map():
    def __init__(self, window, map_name = "stadium"):
        self.window = window
        self.name = map_name
        track_dir = maps[self.name].directory
        self.track_surface = pygame.image.load(track_dir + "track.png").convert_alpha()
        self.wall_mask = pygame.mask.from_surface(self.track_surface)
        self.checkpoint_surface = pygame.image.load(track_dir + "checkpoints.png").convert_alpha()
        self.checkpoint_mask = pygame.mask.from_surface(self.checkpoint_surface)
        self.finish_surface = pygame.image.load(track_dir + "finish.png").convert_alpha()
        self.finish_mask = pygame.mask.from_surface(self.finish_surface)

    def get_starting_position(self):
        start = maps[self.name].starting_point
        return start.x, start.y
    def get_starting_angle(self):
        return maps[self.name].starting_angle
    def check_position(self, player):
        if self.wall_mask.overlap(player.mask, player.rect.topleft) is not None:
            pygame.event.post(pygame.event.Event(COLLISION))
        hit = self.checkpoint_mask.overlap(player.mask, player.rect.topleft) is not None
        if hit and not player.on_checkpoint:
            pygame.event.post(pygame.event.Event(CHECKPOINT))
        player.on_checkpoint = hit
        hit = self.finish_mask.overlap(player.mask, player.rect.topleft) is not None
        if hit and not player.on_finish:
            pygame.event.post(pygame.event.Event(FINISH))
        player.on_finish = hit
    def draw(self, display, color, thickness):
        display.blit(self.track_surface, (0, 0))
        display.blit(self.checkpoint_surface, (0, 0))
        display.blit(self.finish_surface, (0, 0))


class EmptyMap():
    def __init__(self, window):
        self.window = window
        self.outer_walls = window.get_rect().inflate(-10, -10)
    def get_starting_position(self):
        w, h = self.window.get_size()
        return w/2, h - 150
    def check_collision(self, player):
        return not self.outer_walls.contains(player.rect)
    def draw(self, display, color, thickness):
        pygame.draw.rect(display, color, self.outer_walls, 2)

