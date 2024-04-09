from drawing import Drawing
from player import Player
from map import *
import pygame


class Engine:
    def __init__(self, Width, Height, fullscreen = False, drawing = False, server = True):
        self.screen = pygame.display.set_mode((Width, Height))
        if fullscreen:
            pygame.display.toggle_fullscreen()
        self.running = False
        self.always_fills = True
        self.drawing = drawing
        self.players = []
        self.player = Player()
        self.server = server
        self.BSP_node = BSP()
        self.plane_matrix = []
        self.collision_boxes = []
        self.Draw_class = Drawing(self.screen)

    def add_player(self, player):
        self.players.append(player)
    def remove_player(self, player):
        self.players.remove(player)
    def load_map(self, file_name):
        self.plane_matrix = load(file_name)
        #print(self.plane_matrix[0])
        self.set_bsp()
    def set_bsp(self):
        self.BSP_node.set_bsp_tree(self.plane_matrix)
    def debug(self, fps):
        self.Draw_class.debug(self.player, fps)
    def draw(self):
        if self.player.gr:
            self.Draw_class.painters_algoritm(self.BSP_node, self.player)
        else:
            for plane in self.plane_matrix:
                self.Draw_class.render(plane, self.player, True)

    def Exit(self):
        self.running = False
        pygame.quit()
    def run(self):

        clock = pygame.time.Clock()

        self.running = True

        while self.running:
            if self.always_fills:
                self.screen.fill(colours[0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.Exit()
                    return 0

            if self.BSP_node.root is None:
                self.Draw_class.Error()
                pygame.display.update()
                continue
            self.draw()

            time = clock.get_time()/1000

            if self.player.show_debug:
                self.debug(clock.get_fps())

            self.player.movement(time)
            pygame.draw.line(self.screen, (255, 0, 0), (HALF_WIDTH - 5, HALF_HEIGHT), (HALF_WIDTH + 5, HALF_HEIGHT))
            pygame.draw.line(self.screen, (255, 0, 0), (HALF_WIDTH, HALF_HEIGHT - 5), (HALF_WIDTH, HALF_HEIGHT + 5))
            for player in self.players:
                player.movement(time + clock.get_time())
                if self.drawing:
                    for i in player.model:
                        math_plane, colour, vector = i

                        math_plane = matrix_multiplying(math_plane, rotation_matrix_y(player.angle_y))
                        math_plane = matrix_multiplying(math_plane, rotation_matrix_x(player.angle_x))
                        math_plane = matrix_multiplying(math_plane, rotation_matrix_z(player.angle_z))

                        math_plane = transfer(math_plane, player.x, player.y, player.z)
                        self.Draw_class.render((math_plane, colour, vector), self.player, True)

            pygame.display.update()
            clock.tick()



if file:
    engine = Engine(WIDTH, HEIGHT, fullscreen, True, 0)
    engine.player.collision_boxes_types = collision_boxes_types
    pygame.display.set_icon(pygame.image.load("icon.ico"))
    pygame.display.set_caption("Проверка работы 3D BSP-алгоритма")
    engine.plane_matrix = matrix
    engine.set_bsp()
    engine.run()
