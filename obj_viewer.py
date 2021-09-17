import pygame
import math

pygame.init()




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
        file = open(name + ".obj", "r")
        lines = file.readlines()
        for line in lines:
            if line[0] == "v":
                line = line[2:].split("  ")

                self.verts.append((float(line[0]), float(line[1]), float(line[2])))


            if line[0] == "f":
                line = line[2:].split("  ")

                self.faces.append((int(line[0]) -1, int(line[1]) -1, int(line[2]) -1))






block_list = []
block = Block(x=0, y=0, z=0, name="diamond")
block_list.append(block)

width, height = 700, 700
cx = width // 2
cy = height // 2

screen = pygame.display.set_mode((width, height))
pygame.display.flip()

running = True
pygame.display.set_caption('3d game engine')

cam = [0, 0, 10, 0, 0]
colors = [(0,255,0), (255,0,0), (0,0,255), (255, 255, 0), (0,255,255), (0, 100, 0), (100, 0, 0), (0,0,100)]
clock = pygame.time.Clock()

pygame.event.get()
pygame.mouse.get_rel()
pygame.event.set_grab(True)


def rotate(verts, angle):
    x = verts[0]
    y = verts[1]
    cosTheta = math.cos(angle)
    sinTheta = math.sin(angle)
    return x * cosTheta - y * sinTheta, y * cosTheta + x * sinTheta;


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
            rot_x, rot_y = event.rel
            rot_x /= 100
            rot_y /= 100
            index = 0
            for verts in block.verts:

                y, z = rotate((verts[1], verts[2]), rot_y)
                block.verts[index] = (verts[0], y, z)
                index += 1
        if event.type == pygame.MOUSEMOTION and ignore == False:
            rot_x, rot_y = event.rel
            rot_x /= 100
            rot_y /= 100
            index = 0
            for verts in block.verts:
                x, z = rotate((verts[0], verts[2]), rot_x)

                block.verts[index] = (x, verts[1], z)
                index += 1


        if event.type == pygame.MOUSEMOTION and ignore == True:
            ignore = False

        if pygame.mouse.get_pos()[0] <= 0 or pygame.mouse.get_pos()[0] >= width - 1:
            pygame.mouse.set_pos([width / 2, height / 2])
            ignore = True

        if pygame.mouse.get_pos()[1] <= 0 or pygame.mouse.get_pos()[1] >= height - 1:
            ignore = True

    screen.fill((255, 255, 255))
    face_list = []
    depth = []
    color_index = 0
    for face in block.faces:

        points = []
        vert_list = ()

        for x in face:
            vert_list = vert_list + (block.verts[x],)
        zees = []
        for x, y, z in vert_list:

            x -= cam[0]
            y -= cam[1]
            z -= cam[2]
            x -= block.x / 10
            y -= block.y / 10

            f = width / z
            x, y = x * f, y * f
            x, y = cx + int(x), cy + int(y)
            zees.append(z)
            points.append((x, y))
        points.append(colors[color_index])
        face_list.append(points)
        depth.append(sum(iter(zees)) / len(zees))
        color_index += 1
    order = [x for _, x in sorted(zip(depth, face_list))]



    for face in order:

        pygame.draw.polygon(screen, face[-1], face[:-1], 5)
        pygame.draw.polygon(screen, face[-1], face[:-1])

    #     pygame.draw.rect(screen, (255,255,255), (320,347,60,6),0)
    #     pygame.draw.rect(screen, (255,255,255), (347,320,6,60),0)

    pygame.display.flip()

