import pygame
from PhysicsObjects import Player
from FliesWorlds import *
from LinAlg import Vector3
from math import pi
import sys
from World import World

pygame.init()
pygame.font.init()
DEGREES = 180 / pi


def cap(x, low, high):
    if x < low:
        return low
    elif x > high:
        return high
    return x


class Camera:
    def __init__(self, target=None, debug=False):
        self.offset = Vector3(400, -300, 0)
        self.location = Vector3(0, 0, 0)
        self.target = target
        self.zoom = 1.9
        self.zoom_modifier = 0
        self.debug = debug

    def tick(self):
        if self.target is None:
            pass
        else:
            temp_v = self.target.velocity.flatten().magnitude()
            temp = self.target.location + (self.target.velocity * Vector3(0.9 - cap(temp_v / 2000, 0, 0.9), 0, 0))
            direction, distance = (temp - self.location).normalize(True)
            if distance > 1:
                self.location += (direction * (distance / 8))

    def render_entity(self, window, entity: Entity):
        zoom = self.zoom_modifier + self.zoom
        if entity.texture is not None:
            rotation = entity.rotation + entity.texture.rotation_offset
            transformed = pygame.transform.rotozoom(entity.texture.surface, rotation * DEGREES, zoom)
            half = Vector3(*transformed.get_size(), 0) / 2
            location = (entity.location + entity.texture.location_offset - self.location) * zoom - half + self.offset
            window.blit(transformed, location.render())

        if self.debug and entity.hitbox is not None:
            for i in range(len(entity.hitbox.vertices)):
                start = (entity.hitbox.vertices[i - 1] - self.location) * zoom + self.offset
                end = (entity.hitbox.vertices[i] - self.location) * zoom + self.offset
                pygame.draw.line(window, entity.hitbox.color, start.render(), end.render(), 2)


def get_sprite(sheet, rectangle):
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    return image


class Game:
    def __init__(self):
        self.resolution = [800, 600]
        self.window = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("SuperChocolateSantaJam")

        self.font = pygame.font.SysFont("courier", self.resolution[0] // 60)

        self.left = self.right = self.up = self.down = self.space = self.reset = False

        self.player_a = Player(
            name="player",
            shape=center_rectangle(10, 16),
            material=Material(friction=0.05, restitution=0),
            location=Vector3(480, 400, 0),
            affected_by_torque=False,
        )
        self.player_b = Player(
            name="player",
            shape=center_rectangle(10, 16),
            material=Material(friction=0.05, restitution=0),
            location=Vector3(480, 400, 0),
            affected_by_torque=False,
        )

        self.players = (
            self.player_a,
            self.player_b,
        )
        self.player_index = 0
        self.current_player = self.players[self.player_index]

        self.world_index = 0
        self.worlds = (
            World((0, 0, 3200, 3200), (230, 230, 230), make_world_a() + [self.player_a]),
            World((0, 0, 3200, 3200), (230, 230, 230), make_world_b() + [self.player_b]),
        )

        self.camera = Camera(self.current_player, True)
        self.camera.location = self.current_player.location.copy()

        self.current_world = self.worlds[self.world_index]

        self.running = True
        self.superjumps = 0
        self.frame = 0
        self.deaths = 0
        self.resets = 0
        self.jumps = 0
        self.swaps = 0
        self.zoom = False
        self.won = False
        self.start_frame = -1
        self.run()

    def setup(self):
        self.left = self.right = self.up = self.down = self.space = False
        self.player_a.location = Vector3(480, 400, 0)
        self.player_a.velocity = Vector3(0, 0, 0)
        self.player_a.force = Vector3(0, 0, 0)
        self.player_a.dead = False
        self.player_a.on_ground = False
        self.player_a.double_jump = self.player_a.last_gap = 0
        self.player_a.spawnpoint = Vector3(480, 400, 0)

        self.player_b.location = Vector3(480, 400, 0)
        self.player_b.velocity = Vector3(0, 0, 0)
        self.player_b.force = Vector3(0, 0, 0)
        self.player_b.dead = False
        self.player_b.on_ground = True
        self.player_b.double_jump = self.player_b.last_gap = 0
        self.player_b.spawnpoint = Vector3(480, 400, 0)

        self.worlds = (
            World((0, 0, 3200, 3200), (230, 230, 230), make_world_a() + [self.player_a]),
            World((0, 0, 3200, 3200), (230, 230, 230), make_world_b() + [self.player_b]),
        )

        for item in spawners:
            item.hitbox.color = (0, 200, 20)

        self.player_index = 0
        self.current_player = self.players[self.player_index]
        self.camera = Camera(self.current_player, True)
        self.camera.location = self.current_player.location.copy()
        self.world_index = 0
        self.current_world = self.worlds[self.world_index]
        self.running = True
        self.superjumps = 0
        self.frame = 0
        self.deaths = 0
        self.jumps = 0
        self.swaps = 0
        self.zoom = False
        self.won = False
        self.start_frame = -1
        self.resets += 1
        self.run()

    def player_movement(self):
        if not self.current_player.on_ground and not self.up and self.current_player.double_jump == 0:
            self.current_player.double_jump = 1
        elif self.current_player.on_ground:
            self.current_player.double_jump = 0

        self.current_player.rotation = cap(self.current_player.velocity[0], -200, 200) / 1000

        if self.left:
            if self.current_player.on_ground:
                self.current_player.apply_force(Vector3(-700, 0, 0))
            elif self.current_player.velocity[0] > -100:
                self.current_player.apply_force(Vector3(-2000, 0, 0))
            else:
                self.current_player.apply_force(Vector3(-250, 0, 0))
        if self.right:
            if self.current_player.on_ground:
                self.current_player.apply_force(Vector3(700, 0, 0))
            elif self.current_player.velocity[0] < 100:
                self.current_player.apply_force(Vector3(2000, 0, 0))
            else:
                self.current_player.apply_force(Vector3(250, 0, 0))
        if self.up:
            if self.current_player.on_ground:
                self.jumps += 1
                self.current_player.apply_force(Vector3(0, 25000, 0))
                if self.right:
                    self.current_player.apply_force(Vector3(6000, 0, 0))
                elif self.left:
                    self.current_player.apply_force(Vector3(-6000, 0, 0))
            elif self.current_player.double_jump == 1:
                self.jumps += 1
                self.current_player.double_jump = 2
                self.current_player.velocity[1] = 0
                self.current_player.apply_force(Vector3(0, 35000, 0))
                if self.right:
                    self.current_player.apply_force(Vector3(3000, 0, 0))
                elif self.left:
                    self.current_player.apply_force(Vector3(-3000, 0, 0))

    def process_events(self):
        self.up = self.down = self.reset = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.camera.zoom *= 1.1
                    self.zoom = True
                elif event.button == 5:
                    self.camera.zoom *= 0.9
                    self.zoom = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.up = True
                elif event.key == pygame.K_LEFT:
                    self.left = True
                elif event.key == pygame.K_RIGHT:
                    self.right = True
                elif event.key == pygame.K_DOWN:
                    self.down = True
                elif event.key == pygame.K_SPACE:
                    self.space = True
                elif event.key == pygame.K_q:
                    self.reset = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left = False
                elif event.key == pygame.K_RIGHT:
                    self.right = False
                elif event.key == pygame.K_SPACE:
                    self.space = False
        if self.space:
            self.left = self.right = 0

    def logic(self):
        if self.reset:
            self.setup()
        elif not self.won:
            if self.current_player.location.x > 3200:
                self.running = False
                self.won = True

            self.current_player.hitbox.color = (30, 30, 30)

            if self.current_player.dead:
                spawnpoint = self.current_player.spawnpoint.copy()
                self.current_player.dead = False
                self.world_index = 0
                self.player_index = 0
                self.deaths += 1
                self.current_world = self.worlds[self.world_index]
                self.current_player = self.players[self.player_index]
                self.current_player.location = spawnpoint.copy()
                self.current_player.spawnpoint = spawnpoint.copy()
                self.current_player.velocity = Vector3(0, 0, 0)
                self.camera.target = self.current_player

            if self.down:
                if self.start_frame == -1:
                    self.start_frame = self.frame
                next_world = self.worlds[not self.world_index]
                next_player = self.players[not self.player_index]
                next_player.location = self.current_player.location.copy()
                next_player.velocity = self.current_player.velocity.copy()
                next_player.rotation = self.current_player.rotation
                next_player.on_ground = self.current_player.on_ground
                next_player.double_jump = self.current_player.double_jump
                next_player.spawnpoint = self.current_player.spawnpoint.copy()
                superjump_flag = next_player.force.y > 20000

                next_world.tick()
                if not next_player.on_ground or next_player.last_gap < 3:
                    self.swaps += 1
                    self.player_index = not self.player_index
                    self.world_index = not self.world_index
                    self.current_world = next_world
                    self.current_player = next_player
                    self.camera.target = self.current_player
                    if superjump_flag:
                        self.superjumps += 1

            if self.space and self.camera.zoom_modifier > -1.25:
                error = 1.0 - self.camera.zoom_modifier
                self.camera.zoom_modifier -= error / 15
            elif not self.space and self.camera.zoom_modifier < 0.0:
                error = -self.camera.zoom_modifier
                self.camera.zoom_modifier += error / 15

    def render(self):
        self.window.fill(self.current_world.background_color)

        for item in self.current_world.objects:
            self.camera.render_entity(self.window, item)

        # self.camera.render_entity(self.window, self.players[not self.player_index])

        for item in texts:
            x = 400
            y = 10
            if item.visible:
                rect = self.font.render(item.text, 1, (0, 0, 0))
                x -= int(rect.get_rect().width // 2)
                self.window.blit(rect, (x, y))
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            self.frame += 1
            self.process_events()
            self.current_world.tick()
            self.logic()
            self.player_movement()
            self.camera.tick()
            self.render()
        if self.won:
            self.window.fill(self.current_world.background_color)
            hit_checkpoints = len([p for p in spawners if p.hitbox.color != (0, 200, 20)])

            strings = ["Finished!",
                       "Time: %s frames" % str(self.frame - self.start_frame),
                       "Jumps: %s" % str(self.jumps),
                       "Superjumps: %s" % str(self.superjumps),
                       "Swaps: %s" % str(self.swaps),
                       "Checkpoints: %s/8" % hit_checkpoints,
                       "Deaths: %s" % str(self.deaths),
                       "Zoom used: %s" % str(self.zoom),
                       ]
            for i in range(len(strings)):
                x = 400
                y = 200 + (i * 15)
                rect = self.font.render(strings[i], 1, (0, 0, 0))
                x -= int(rect.get_rect().width // 2)
                self.window.blit(rect, (x, y))
            pygame.display.update()
            self.running = True
            while self.running:
                self.process_events()
                if self.reset:
                    self.setup()
        pygame.quit()
        sys.exit(0)


flies = Game()
