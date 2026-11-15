from dataclasses import dataclass, field
import pygame

COLLISION = pygame.USEREVENT + 1
CHECKPOINT = pygame.USEREVENT + 2
FINISH = pygame.USEREVENT + 3
BACKWARDS = pygame.USEREVENT + 4

@dataclass 
class Point:
    x: float = 0
    y: float = 0

@dataclass 
class Track:
    directory: str
    starting_point: Point
    starting_angle: int = 0

@dataclass
class PlayerStats:
    passed_checkpoints: list[int] = field(default_factory=list)
    on_finish: bool = False
    on_checkpoint: int = None

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
        self.map_size = self.wall_mask.get_size()

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

        self.players_state = {}

    def register_player(self, player):
        self.players_state[player.id] = PlayerStats()
    
    def reset_player_state(self, player_id):
        self.players_state[player_id] = PlayerStats()

    def get_starting_position(self):
        start = maps[self.name].starting_point
        return start.x, start.y
    
    def get_starting_angle(self):
        return maps[self.name].starting_angle
    
    def check_position(self, player_id, player_mask, player_offset):
        player_state = self.players_state[player_id]
        offset = player_offset

        if self.wall_mask.overlap(player_mask, offset) is not None:
            pygame.event.post(pygame.event.Event(COLLISION, player_id=player_id))
       
        finish_hit = self.finish_mask.overlap(player_mask, offset) is not None
        if finish_hit and not player_state.on_finish:
            if len(player_state.passed_checkpoints) == len(self.checkpoint_masks):
                pygame.event.post(pygame.event.Event(FINISH, player_id=player_id))
                player_state.passed_checkpoints.clear()
        player_state.on_finish = finish_hit

        if self.checkpoint_mask.overlap(player_mask, offset) is not None:
            if player_state.on_checkpoint is None:
                checkpoint_hit = None 
                for i, mask in enumerate(self.checkpoint_masks):
                    if mask.overlap(player_mask, offset) is not None:
                        checkpoint_hit = i
                        break
                player_state.on_checkpoint = checkpoint_hit
                if checkpoint_hit is None:
                    return
                if checkpoint_hit not in player_state.passed_checkpoints:
                    if checkpoint_hit==0 or checkpoint_hit - 1 in player_state.passed_checkpoints:
                        player_state.passed_checkpoints.append(checkpoint_hit)
                        pygame.event.post(pygame.event.Event(CHECKPOINT, player_id=player_id, index=checkpoint_hit))
                    else:
                        pygame.event.post(pygame.event.Event(BACKWARDS, player_id=player_id, index=checkpoint_hit))
                elif checkpoint_hit+1 in player_state.passed_checkpoints:
                    player_state.passed_checkpoints.remove(checkpoint_hit+1)
                    pygame.event.post(pygame.event.Event(BACKWARDS, player_id=player_id, index=checkpoint_hit))
        else:
            player_state.on_checkpoint = None

    def is_wall(self, x, y):
        if not (0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]):
            return True # collsion when out of bounds
        return self.wall_mask.get_at((x, y)) > 0
    
    def draw(self, display, color, thickness):
        display.blit(self.track_surface, (0, 0))
        #display.blit(self.checkpoint_surface, (0, 0)) 
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

