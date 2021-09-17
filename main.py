import pygame
import math

pygame.init()



def centroid(vertexes):
    _x_list = [vertex [0] for vertex in vertexes]
    _y_list = [vertex [1] for vertex in vertexes]
    _len = len(vertexes)
    _x = sum(_x_list) / _len
    _y = sum(_y_list) / _len
    return(_x, _y)


class Block:
    """ This class represents a simple block the player collects. """

    def __init__(self, x, y, z, name):
        """ Constructor, create the image of the block. """
        self.x = x
        self.y = y
        self.z = z

        self.name = name

        self.verts = []
        self.edges = []
        self.faces = []

        if name != 0:

            file = open(name + "_verts", "r")

            lines = file.readlines()

            for line in lines:
                line = line.split(",")
                self.verts.append((float(line[0]), float(line[1]), float(line[2])))
            print(self.verts)

            file = open(name + "_edges", "r")

            lines = file.readlines()

            for line in lines:
                line = line.split(",")
                self.edges.append((int(line[0]), int(line[1])))
            print(self.edges)

            file = open(name + "_faces", "r")

            lines = file.readlines()

            for line in lines:
                line = line.split(",")
                append_tuple = ()
                line = line[:-1]
                for num in line:
                    num = int(num)
                    append_tuple = append_tuple + (num,)
                self.faces.append(append_tuple)
            print(self.faces)


block_list = []
block = Block(x=0, y=0, z=0, name="tri")
block_list.append(block)

width, height = 700, 700
cx = width // 2
cy = height // 2

screen = pygame.display.set_mode((width, height))
pygame.display.flip()

running = True
pygame.display.set_caption('3d game engine')

cam = [0, 0, 10, 0, 0]

clock = pygame.time.Clock()

pygame.event.get()
pygame.mouse.get_rel()
pygame.event.set_grab(True)


def rotate(verts, angle):
    x = verts[0]
    y = verts[1]
    s, c = math.sin(angle), math.cos(angle)
    return x * c - y * s, y * c + x * s


ignore = False

print("[W][A][S][D] to move, [F] to toggle cursor, Cursor to look around, [ESC] To quit")

while running:

    dt = clock.tick() / 1000
    step = dt * 5
    keys = pygame.key.get_pressed()

    x, y = step * math.sin(cam[3]), step * math.cos(cam[3])
    real_x, real_y = step * math.sin(cam[4]), step * math.cos(cam[4])

    if keys[pygame.K_w]:

        cam[0] -= x
        cam[2] -= y

    elif keys[pygame.K_s]:

        cam[0] += x
        cam[2] += y

    if keys[pygame.K_a]:

        cam[0] += y
        cam[2] -= x

    elif keys[pygame.K_d]:
        cam[0] -= y
        cam[2] += x

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                exit()

        if event.type == pygame.MOUSEMOTION and ignore == False:
            x, y = event.rel
            x /= 200
            y /= 200
            cam[3] += x;
            cam[4] += y

        if event.type == pygame.MOUSEMOTION and ignore == True:
            ignore = False

        if pygame.mouse.get_pos()[0] <= 0 or pygame.mouse.get_pos()[0] >= width - 1:
            pygame.mouse.set_pos([width / 2, height / 2])
            ignore = True

        if pygame.mouse.get_pos()[1] <= 0 or pygame.mouse.get_pos()[1] >= height - 1:
            ignore = True

    screen.fill((255, 255, 255))

    for face in block.faces:

        points = []
        vert_list = ()

        for x in face:
            vert_list = vert_list + (block.verts[x],)

        for x, y, z in vert_list:
            x -= cam[0]
            y -= cam[1]
            z -= cam[2]
            x -= block.x / 10
            y -= block.y / 10
            x, z = rotate((x, z), cam[3])
            y, z = rotate((y, z), cam[4])
            f = width / z
            x, y = x * f, y * f
            x, y = cx + int(x), cy + int(y)

            points.append((x, y))

        pygame.draw.polygon(screen, (0, 0, 0), points, 5)
        pygame.draw.polygon(screen, (0, 0, 255), points)

    #     pygame.draw.rect(screen, (255,255,255), (320,347,60,6),0)
    #     pygame.draw.rect(screen, (255,255,255), (347,320,6,60),0)

    pygame.display.flip()

