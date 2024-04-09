import math

from algebra import *


class Player:
    def __init__(self, pos=player_pos, angle=player_angle, collision_boxes_types = [[], []]):
        self.x, self.y, self.z = pos
        self.gr = True
        self.noclip = False
        self.noclip_flag = False
        self.angle_x, self.angle_y, self.angle_z = angle
        self.f3_flag = False
        self.show_debug = True
        self.tp_flag = False
        self.health = 100
        self.gravity = -9.80665
        self.jump_vilocity = 4.142660678839144
        self.vilocity = [0, 0, 0]
        self.slowing_flag = False
        self.BBOX  = BBOX
        self.BBOX2 = BBOX2
        self.collision_boxes_types = collision_boxes_types
        self.sit_flag = False
        pygame.mouse.set_visible(False)

    @property
    def pos(self):
        return self.x, self.y, self.z

    @property
    def angle(self):
        return self.angle_x, self.angle_y, self.angle_z

    def collision_detect(self, collision_box, pos):
        min_depth = None
        if not len(collision_box):
            return None
        for cut_plane in collision_box:

            position = distance_to_plane(pos, cut_plane)
            if position > 0 or null(position, accuracy):
                return None
            if min_depth is None:
                min_depth = position
                vector = cut_plane[0]
            else:
                if (min_depth < position):
                    min_depth = position
                    vector = cut_plane[0]

        return vector_multiplied_on_number(vector, -min_depth)

    def collider(self, collision_boxes, pos):
        offs_vect = [0, 0, 0]
        flag = False
        if not self.noclip:
            for i in range(len(collision_boxes)):
                mov = self.collision_detect(collision_boxes[i], pos)
                if mov is not None:
                    if not flag:
                        flag = True
                    offs_vect = sum_of_vectors(mov, offs_vect)
        return offs_vect, flag

    def movement(self, time_koeff):
        dx, dy = sum_of_vectors(pygame.mouse.get_pos(), (HALF_WIDTH, HALF_HEIGHT), 0)
        if (abs(dx) >= HALF_WIDTH) or (abs(dy) >= HALF_HEIGHT):
            pygame.mouse.set_pos(HALF_WIDTH, HALF_HEIGHT)
            dx, dy = 0, 0

        if (self.angle_x - dy / 500) < -math.pi/2:
            self.angle_x = -math.pi/2
        elif (self.angle_x - dy / 500) > math.pi/2:
            self.angle_x = math.pi/2
        else:
            self.angle_x -= dy / 500
        self.angle_z += dx / 500



        keys = pygame.key.get_pressed()
        W, A, S, D = keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d]
        delta_vilocity = [0, 0, 0]
        cos_z, sin_z = math.cos(self.angle_z), math.sin(self.angle_z)

        if W:
            delta_vilocity[0] += sin_z
            delta_vilocity[1] += cos_z
        if D:
            delta_vilocity[0] += cos_z
            delta_vilocity[1] -= sin_z
        if S:
            delta_vilocity[0] -= sin_z
            delta_vilocity[1] -= cos_z
        if A:
            delta_vilocity[0] -= cos_z
            delta_vilocity[1] += sin_z

        if keys[pygame.K_SPACE]:
            delta_vilocity[2] += 1
        if keys[pygame.K_LSHIFT]:
            delta_vilocity[2] -= 1
        if scalar_vector_multiplying(delta_vilocity, delta_vilocity) > 0.01:
            delta_vilocity = vector_multiplied_on_number(normalize(delta_vilocity), player_speed * time_koeff)

        self.x, self.y, self.z = sum_of_vectors(self.pos, delta_vilocity)

        #if module(sum_of_vectors(self.vilocity, delta_vilocity)) > player_max_speed:
        #    pass

        self.angle_y %= 2 * math.pi
        self.angle_z %= 2 * math.pi
        if dx or dy:
            pygame.mouse.set_pos(HALF_WIDTH, HALF_HEIGHT)
        if self.health < 40:
            self.angle_y = -math.radians(35)
        if self.health <= 0:
            if self.health < 0:
                self.health = 0
            self.angle_y = -math.radians(90)

