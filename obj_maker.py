import pygame

import math
import os

x = 1000
y = 0

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)



pygame.init()
font = pygame.font.Font(os.path.join("res", "fonts", "C:\\Users\\15154\\Downloads\\vt323\\VT323-Regular.ttf"), 30)

class Block():
    """ This class represents a simple block the player collects. """
 
    def __init__(self, x, y, z, name):
        """ Constructor, create the image of the block. """
        self.x = x
        self.y = y
        self.z = z
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
        else:
            self.verts = [(1,1,1), (-1,1,1)]
            self.edges = [(0,1)]
            self.faces = []
#         self.verts = [(1,1,1), (-1, -1, 1), (1, -1, 1), (1, 1,-1), (-1, -1, -1), (1, -1, -1)] 
#         self.edges = [(0,1), (1,2), (2,0), (0,3), (3,4), (4,1), (5,4), (5,2), (3,5)]
    
block_list = []
edit = input("Edit (e) or new (n)? ")
if edit == "e":
    fname = input("Name? ")
    block = Block(x = 0, y = 0, z = 0, name = fname)
    block_list.append(block)
else:
    block = Block(x = 0, y = 0, z = 0, name = 0)
    block_list.append(block)

'''block = Block(x = 200, y = 30, z = 100, length = 10, width = 10, depth = 100)
block_list.add(block)'''
 
width, height = 700, 700
cx = width//2
cy = height//2
screen = pygame.display.set_mode((width, height))
pygame.display.flip()



running = True
pygame.display.set_caption('3d game engine')

cam = [0,0,10,0,0]

clock = pygame.time.Clock()


forward = True
side = True
drawline = pygame.draw.line
greater = 0
best_x = 0
forward = False
left_right = 0
angle = 0
pygame.event.get()
pygame.mouse.get_rel()
pygame.event.set_grab(True)
def rotate(verts, angle):
     x = verts[0]
     y = verts[1]
     #z = verts[2]
     s,c = math.sin(angle),math.cos(angle)
     return x*c-y*s,y*c+x*s
ignore = False

print("[W][A][S][D] to move, [t] to toggle cursor, Cursor to look around, [ESC] To quit. [Space] for new point. [M] to save. [f] for new face")
walking_up = 0
walking_down = 0

while running:
    
    dt = clock.tick() / 1000
    step = dt * 5
    keys=pygame.key.get_pressed()
    
    #print(greater)
    
    x,y = step*math.sin(cam[3]), step*math.cos(cam[3])
    real_x, real_y = step*math.sin(cam[4]), step*math.cos(cam[4])
    '''forward = False
    if int(left_right) > 1.5 or int(left_right) < -1.5:
   
       forward = True
    elif greater > 3:
       forward = True'''
    if keys[pygame.K_w]:
        if walking_up == 0:
           walking_up += 1
        if walking_up > 0 and walking_up < 200:
            walking_up += 1
            cam[1] += step / 5
        if walking_up >= 200 and walking_down == 0:
            walking_down += 1
            cam[1] -= step / 5
        if walking_down > 0 and walking_down < 200:
            walking_down += 1
            cam[1] -= step / 5
        if walking_down >= 200:
            walking_up = 0
            walking_down = 0
        cam[0] -= x
        cam[1] -= real_x
        cam[2] -= y
        #print(cam[2])
    
    
    
   
    
 
    elif keys[pygame.K_s]:
        if walking_up == 0:
           walking_up += 1
        if walking_up > 0 and walking_up < 200:
            walking_up += 1
            cam[1] += step / 5
        if walking_up >= 200 and walking_down == 0:
            walking_down += 1
            cam[1] -= step / 5
        if walking_down > 0 and walking_down < 200:
            walking_down += 1
            cam[1] -= step / 5
        if walking_down >= 200:
            walking_up = 0
            walking_down = 0
        cam[0] += x
        cam[2] += y
        cam[1] += real_x
    if keys[pygame.K_a]:
        cam[0] += y
        cam[2] -= x
        
    if keys[pygame.K_d]:
        cam[0] -= y
        cam[2] += x
    
    
    
        
        
        
     
    polygon = []

    
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
          pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                exit()
            if event.key == pygame.K_t:
                cam = [0,0,10,0,0]
                
                
                
            if event.key == pygame.K_f:
                pygame.event.set_grab(False)
                face = ()
                index = 1
                while True:
                    asked = input("Enter " + str(index) + " number for face: [z] to end: ")
                    if asked != "z":
                        face = face + (int(asked),)
                        index += 1
                    else:
                        break
                pygame.mouse.set_pos([width/2, height/2])
                block.faces.append(face)
                    
            if event.key == pygame.K_SPACE:
                pygame.event.set_grab(False)
                first = input("First connect point: ")
                pygame.mouse.set_pos([width/2, height/2])
                pygame.event.set_grab(True)
                block.verts.append((0,0,0))
                block.edges.append((len(block.verts) - 1,int(first)))
            if event.key == pygame.K_l:
                last = block.verts[-1]
                block.verts[-1] = (last[0] - 0.25, last[1], last[2])
                
            if event.key == pygame.K_j:
                last = block.verts[-1]
                block.verts[-1] = (last[0] + 0.25, last[1], last[2])
                
            if event.key == pygame.K_i:
                last = block.verts[-1]
                block.verts[-1] = (last[0], last[1], last[2] - 0.25)
            
            if event.key == pygame.K_k:
                last = block.verts[-1]
                block.verts[-1] = (last[0], last[1], last[2] + 0.25)
                
            if event.key == pygame.K_UP:
                last = block.verts[-1]
                block.verts[-1] = (last[0], last[1] + 0.25, last[2])
                
            if event.key == pygame.K_DOWN:
                last = block.verts[-1]
                block.verts[-1] = (last[0], last[1] - 0.25, last[2])
            if event.key == pygame.K_c:
                pygame.event.set_grab(False)
                new_num = input("New connect point: ")
                pygame.mouse.set_pos([width/2, height/2])
                pygame.event.set_grab(True)
                last = block.edges[-1]
                block.edges[-1] = (len(block.verts) - 1, int(new_num))
            if event.key == pygame.K_m:
                pygame.event.set_grab(False)
                if edit == "e":
                    new_or_save = input("Save as new (n) or save (s)? ")
                    if new_or_save == "n":
                        name = input("Name: ")
                        pygame.event.set_grab(True)
                        file = open(name + "_verts", "w+")
                        for vert in block.verts:
                            for num in vert:
                                file.write(str(num) + ",")
                            file.write("\n")
                        file.close()
                        
                        file = open(name + "_edges", "w+")
                        for edges in block.edges:
                            for num in edges:
                                file.write(str(num) + ",")
                            file.write("\n")
                        file.close()
                        
                        file = open(name + "_faces", "w+")
                        for face in block.faces:
                            for num in face:
                                file.write(str(num) + ",")
                            file.write("\n")
                        file.close()
                    else:
                        name = fname
                        pygame.event.set_grab(True)
                        file = open(name + "_verts", "w")
                        for vert in block.verts:
                            for num in vert:
                                file.write(str(num) + ",")
                            file.write("\n")
                        file.close()
                        
                        file = open(name + "_edges", "w")
                        for edges in block.edges:
                            for num in edges:
                                file.write(str(num) + ",")
                            file.write("\n")
                        file.close()
                    
                        file = open(name + "_faces", "w+")
                        for face in block.faces:
                            for num in face:
                                file.write(str(num) + ",")
                            file.write("\n")
                        file.close()
                else:
                    name = input("Name: ")
                    pygame.event.set_grab(True)
                    file = open(name + "_verts", "w+")
                    for vert in block.verts:
                        for num in vert:
                            file.write(str(num) + ",")
                        file.write("\n")
                    file.close()
                        
                    file = open(name + "_edges", "w+")
                    for edges in block.edges:
                        for num in edges:
                            file.write(str(num) + ",")
                        file.write("\n")
                    file.close()
                    
                    file = open(name + "_faces", "w+")
                    for face in block.faces:
                        for num in face:
                            file.write(str(num) + ",")
                        file.write("\n")
                    file.close()
                pygame.quit()
                exit()
            
            
        if event.type == pygame.MOUSEMOTION and ignore == False:
            x,y = event.rel
            x/= 200
            y/= 200
            cam[3] += x;cam[4] += y
        if event.type == pygame.MOUSEMOTION and ignore == True:
            ignore = False
        
        if pygame.mouse.get_pos()[0] <= 0 or pygame.mouse.get_pos()[0] >= width - 1:
            pygame.mouse.set_pos([width / 2,height / 2])
            ignore = True
        if pygame.mouse.get_pos()[1] <= 0 or pygame.mouse.get_pos()[1] >= height - 1:
            
            ignore = True
    screen.fill((255,255,255))  
    all_points = []       
                  
    for block in block_list:
        
        for edge in block.edges:
            points = []
            greater = -np.inf
            greater_x = -np.inf
            color = "none"
            for x, y, z in (block.verts[edge[0]], block.verts[edge[1]]):
                
                if x - int(x) == 0 and y - int(y) == 0 and z - int(z) == 0:
                    color = "red"
                else:
                    color = "none"
                x -= cam[0]
                y -= cam[1]
                z -= cam[2]
                x -= block.x / 10
                y -= block.y / 10
                
                
                x,z = rotate((x,z), cam[3])
                y,z = rotate((y,z), cam[4])
                #z += 5
                
                f = width / z
                
                x,y = x * f, y * f
                
                x,y = cx + int(x), cy + int(y)
                
                points.append((x,y))
                
                if (x,y) not in all_points:
                    all_points.append((x,y))
            if color == "red":     
                pygame.draw.line(screen, (255,0,0), points[0], points[1], 1)
            if color == "none":
                pygame.draw.line(screen, (250,0,250), points[0], points[1], 1)
       
            
        
                
        
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
                
                
                x,z = rotate((x,z), cam[3])
                y,z = rotate((y,z), cam[4])
                #z += 5
                
                f = width / z
                
                x,y = x * f, y * f
                
                x,y = cx + int(x), cy + int(y)
                
                points.append((x,y))
                
                if (x,y) not in all_points:
                    all_points.append((x,y))
            
            pygame.draw.polygon(screen, (0,0,0), points, 5)
            pygame.draw.polygon(screen, (0,0,255), points)
            
    index = 0
    for point in block.verts:
        x,y,z = point
        
        x -= cam[0]
        y -= cam[1]
        z -= cam[2]
        x -= block.x / 10
        y -= block.y / 10
                
                
        x,z = rotate((x,z), cam[3])
        y,z = rotate((y,z), cam[4])
                #z += 5
                
        f = width / z
                
        x,y = x * f, y * f
                
        x,y = cx + int(x), cy + int(y)
        
        screen.blit(font.render(str(index), 1, (0, 255, 0)), (x,y))
        index += 1
   
    
   
#     pygame.draw.rect(screen, (0,0,0), (320,347,60,6),0)
#     pygame.draw.rect(screen, (0,0,0), (347,320,6,60),0)
    
    pygame.display.flip()
        
