from algebra import *
import pygame

class Drawing:
    def __init__(self, sc):
        pygame.font.init()
        self.sc = sc
        self.font = pygame.font.SysFont('Arial', int(25*Font_koeff), bold=True)
    def Error(self):
        self.font = pygame.font.SysFont('Arial', int(50 * Font_koeff), bold=True)
        render = self.font.render("BSP дерево пусто", 0, (200, 200, 0))
        self.sc.blit(render, (5, 5 + 30))
    def debug(self, player, fps):
        speed_color = (200, 200, 0)

        render = [
            self.font.render("КАДРЫ В СЕКУНДУ : " + str(int(fps)), 0, (200, 200, 0)),
            self.font.render("ПОЛЕ ЗРЕНИЯ : " + str(round(math.degrees(FOV) % 360, 2)) + "°", 0, (200, 200, 0)),
            self.font.render("ОТРИСОВКА: " + ("BSP" if player.gr else "ПО ГРАНЯМ" ), 0, (200, 200, 0)),
            self.font.render("ПЕРЕМЕЩЕНИЕ: " + ("БЕЗ СТОЛКНОВЕНИЙ" if player.noclip else "ОБЫЧНОЕ"), 0, (200, 200, 0)),
            self.font.render("ВЕРТИКАЛЬНЫЙ УГОЛ : " + str(round(math.degrees(player.angle_x), 4)), 0, (200, 200, 0)),
            self.font.render("ГОРИЗОНТАЛЬНЫЙ УГОЛ : " + str(round(math.degrees(player.angle_z), 4)), 0, (200, 200, 0)),
            self.font.render("ПОПЕРЕЧНЫЙ УГОЛ : " + str(round(math.degrees(player.angle_y), 4)), 0, (200, 200, 0)),
            self.font.render("X : " + str(round(player.x, 6)), 0, (200, 200, 0)),
            self.font.render("Y : " + str(round(player.y, 6)), 0, (200, 200, 0)),
            self.font.render("Z : " + str(round(player.z, 6)), 0, (200, 200, 0)),
            self.font.render(str(int(player.health)), 0, speed_color),
        ]
        for i in range(len(render)):
            self.sc.blit(render[i], (5, 5 + 30*Font_koeff * i))

    def render(self, plane, player, edges = False):
        math_plane, colour, alg_plane = plane
        vector, D = alg_plane
        if not edges and ((positioning(player.pos, alg_plane) is False) or (colour is None)):
            return 0
        if colour is None or ((colour == 0) and edges):
            colour = 7
        try:
            colour = colours[colour]
        except IndexError:
            colour = (255, 0, 255)
        result_plane = \
            rotation_of_plane2(transfer(math_plane, -player.x, -player.y, -player.z),
                              (-player.angle_x, -player.angle_y, -player.angle_z))
        vector = rotation_of_plane2([vector], (-player.angle_x, -player.angle_y, -player.angle_z))[0]
        for cut_plane in cut_planes:
            partition = Sutherland_Hodgman_algorithm(result_plane, cut_plane)

            if (partition != 0) and (partition != 1):
                if partition == -1:
                    return 0
                else:
                    result_plane = partition[1]

        if not(edges):
            guros_k = -vector[1]
            if guros_k < 0:
                guros_k = 0
            guros_k *= guros_k0
            if guros_k + guros > 1:
                guros_k = 1 - guros
            colour = vector_multiplied_on_number(colour, (guros_k + guros))
        result_plane = linear_perspective(result_plane)
        if colour is None:
            colour = (255, 255, 255)
        if not edges:
            pygame.draw.polygon(self.sc, colour, result_plane)
        else:
            pygame.draw.lines(self.sc, colour, True, result_plane) 
    def sprite_render(self, player, pos, size):
        pos = rotation([pos], vector_multiplied_on_number(player.angle, -1), player.pos)
        pass




    def painters_algoritm(self, node, player):
        if node.root is not None:
            if (node.left is None and node.right is None):
                if positioning(player.pos, node.root[2]):
                    self.render(node.root, player)
            else:
                p = positioning(player.pos, node.root[2])
                if p is not None:
                    if p:
                        self.painters_algoritm(node.left, player)
                        self.render(node.root, player)
                        for i in node.mid:
                            self.render(i, player)
                        self.painters_algoritm(node.right, player)
                    else:
                        self.painters_algoritm(node.right, player)
                        self.render(node.root, player)
                        for i in node.mid:
                            self.render(i, player)
                        self.painters_algoritm(node.left, player)
                else:
                    self.painters_algoritm(node.right, player)
                    self.painters_algoritm(node.left, player)
