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

        #combined surface and mask for collective blit and check
        self.checkpoint_surface = pygame.image.load(track_dir + "checkpoints.png").convert_alpha()
        self.checkpoint_mask = pygame.mask.from_surface(self.checkpoint_surface)

        self.checkpoint_surfaces = [
            pygame.image.load(track_dir + f"checkpoint_{i}.png").convert_alpha()
            for i in range (1,11)
        ]

        self.checkpoint_masks = [
            pygame.mask.from_surface(surface) for surface in self.checkpoint_surfaces
        ]

        self.finish_surface = pygame.image.load(track_dir + "finish.png").convert_alpha()
        self.finish_mask = pygame.mask.from_surface(self.finish_surface)


    def get_starting_position(self):
        start = maps[self.name].starting_point
        return start.x, start.y
    
    def get_starting_angle(self):
        return maps[self.name].starting_angle
    
    def check_position(self, player):
        if()
        offset = player.rect.topleft
        if self.wall_mask.overlap(player.mask, offset) is not None:
            pygame.event.post(pygame.event.Event(COLLISION))
       
        if self.checkpoint_mask.overlap(player.mask, offset) is not None:
            if player.on_checkpoint is None:
                checkpoint_hit = None 
                for i, mask in enumerate(self.checkpoint_masks):
                    if mask.overlap(player.mask, offset) is not None:
                        checkpoint_hit = i
                        break
                player.on_checkpoint = checkpoint_hit
                pygame.event.post(pygame.event.Event(CHECKPOINT, index=checkpoint_hit))
        else:
            player.on_checkpoint = None

        finish_hit = self.finish_mask.overlap(player.mask, offset) is not None
        if finish_hit and not player.on_finish:
            pygame.event.post(pygame.event.Event(FINISH))
        player.on_finish = finish_hit
    
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

