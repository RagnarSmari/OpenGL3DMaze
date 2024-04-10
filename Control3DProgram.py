
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *
from platform import python_branch

import pygame
from pygame.locals import *
from Collision import Collision

from Shaders import *
from Matrices import *
from Maze import MazeMaker

class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()
        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        # self.view_matrix.look(self.view_matrix.eye, Point(1, 1, 0), Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.view_matrix.eye.x = self.view_matrix.eye.x + 3
        self.projection_matrix = ProjectionMatrix()
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.fov = pi / 2
        self.projection_matrix.set_perspective(pi / 2, 800/600, 0.5, 10)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.collision = Collision(0.1)

        self.cube = Cube()
        self.sphere = Sphere(24, 48)
        self.plane = Cube()
        self.maze = MazeMaker()
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0
        self.sphereAngle = 0
        self.collision = False
        self.collisionDown = False
        self.collisionUp = False


        ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##
        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]
        self.UP_key_down = False
        self.DOWN_key_down = False
        self.C_key_down = False
        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False
        self.SPACE_key_down = False
        self.CTRL_key_down = False
        self.T_key_down = False
        self.G_key_down = False
        self.camera_speed = 10
        self.left_arrow_down = False
        self.right_arrow_down = False
        self.DOWN_key_down = False
        self.white_background = False
        self.currentCell = 0
        self.eyePosX = 0
        self.eyePosZ = 0
        self.playerX = 0
        self.playerY = 0
        self.playerZ = 0


    def collisionSystemForW(self, eyePosZ, eyePosX):
        if self.currentCell == 0:
            if 'south' in self.maze.mazeList[0][0]:
                if self.view_matrix.eye.x > 0 and self.view_matrix.eye.z > -1.2:
                    self.view_matrix.eye.z = eyePosZ

            if 'west' in self.maze.mazeList[0][0]:
                if self.view_matrix.eye.x < 1.2 and self.view_matrix.eye.z < -1:
                    self.view_matrix.eye.x = eyePosX
            if 'east' in self.maze.mazeList[0][0]:
                if self.view_matrix.eye.x > 9 and self.view_matrix.eye.z < -1:
                    self.view_matrix.eye.x = eyePosX



    def collisionCalc(self, eyePosZ, eyePosX, cellPosZ, cellPosX):
        if 'south' in self.maze.mazeList[cellPosX][cellPosZ]:
            print(self.view_matrix.eye.z, (10*cellPosZ)-1.2)
            if self.view_matrix.eye.z > (10*cellPosZ)-1.2:
                print("South")
                self.view_matrix.eye.z = ((eyePosZ))

        if 'west' in self.maze.mazeList[cellPosX][cellPosZ]:
            if self.view_matrix.eye.x < (cellPosX*10)+1.2:
                print("in west")
                self.view_matrix.eye.x = eyePosX
        if 'east' in self.maze.mazeList[cellPosX][cellPosZ]:
            if self.view_matrix.eye.x > 10*(cellPosX+1)-1.2:
                print("in east")
                self.view_matrix.eye.x = eyePosX

        if 'north' in self.maze.mazeList[cellPosX][cellPosZ]:
                if self.view_matrix.eye.z < -10*(cellPosZ+1)+1.2:
                    print("in north")
                    self.view_matrix.eye.z = eyePosZ

    # def collisionSystemForS(self):
    #     if self.currentCell == 0:
    #         for wall in self.maze.mazeList[0][0]:
    #             if wall == 'south':
    #                 if self.view_matrix.eye.x > 0 and self.view_matrix.eye.z > -0.5:
    #                     return True
    #                 else:
    #                     return False
    #             if wall == 'north':
    #                 if self.view_matrix.eye.x > 0 and self.view_matrix.eye.z > -0.5:
    #                     return Truewwwwwwwww
    #                 else:
    #                     return False
    #             if wall == 'west':
    #                 if self.view_matrix.eye.x < 0.5 and self.view_matrix.eye.z > 0:
    #                     return True
    #                 else:
    #                     return False
    #             if wall == 'east':
    #                 if self.view_matrix.eye.x > 0 and self.view_matrix.eye.z > -0.5:
    #                     return True
    #                 else:
    #                     return False
    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.angle += pi * delta_time
        self.sphereAngle += pi * delta_time
        self.eyePosZ = self.view_matrix.eye.z
        self.eyePosX = self.view_matrix.eye.x
        self.check_curr_cell()
        # cellPosX, cellPosZ = self.maze.get_maze_index(self.currentCell)
        cellPosX = (int)(self.view_matrix.eye.x - 2) // 10
        cellPosZ = -(int)(self.view_matrix.eye.z + 2) // 10

        if self.W_key_down:
            self.view_matrix.slide(0, 0, -self.camera_speed * delta_time)
            self.collisionCalc(self.eyePosZ,self.eyePosX,cellPosZ,cellPosX)
        if self.S_key_down:
            self.view_matrix.slide(0, 0, self.camera_speed * delta_time)
            self.collisionCalc(self.eyePosZ,self.eyePosX,cellPosZ,cellPosX)
        if self.A_key_down:
            # self.view_matrix.slide(-self.camera_speed * delta_time, 0, 0)
            self.view_matrix.rotate_horizontal(pi * delta_time)
        if self.D_key_down:
            # self.view_matrix.slide(self.camera_speed * delta_time, 0, 0)
            self.view_matrix.rotate_horizontal(-pi * delta_time)
        if self.SPACE_key_down:
            self.view_matrix.slide(0, self.camera_speed * delta_time, 0)
        if self.CTRL_key_down:
            self.view_matrix.slide(0, -self.camera_speed * delta_time, 0)

        if self.T_key_down:
            self.fov += 0.25 * delta_time
        if self.G_key_down:
            self.fov -= 0.25 * delta_time

        # Camera rotation
        if self.left_arrow_down:
            # Rotate left
            self.view_matrix.rotate_horizontal(pi * delta_time)
        if self.right_arrow_down:
            self.view_matrix.rotate_horizontal(-pi * delta_time)

        if self.UP_key_down:
            # if self.view_matrix.n.y > -0.5 and self.view_matrix.v.y > 0.1:
                self.view_matrix.rotate_vertical(-pi * delta_time)


        if self.DOWN_key_down:
            # if self.view_matrix.n.y < 1 and self.view_matrix.v.y >0.2:
                self.view_matrix.rotate_vertical(pi * delta_time)

        if self.C_key_down:
            self.white_background = True
        else:
            self.white_background = False



        if self.view_matrix.eye.y != 1:
            self.view_matrix.eye.y = 1


    def check_curr_cell(self):
        if int(self.view_matrix.eye.x) in range(0, 11) and -int(self.view_matrix.eye.z) in range(0, 11):
            self.currentCell = 0
        elif  int(self.view_matrix.eye.x) in range(0, 11) and -int(self.view_matrix.eye.z) in range(11, 21):
            self.currentCell = 1
        elif  int(self.view_matrix.eye.x) in range(0, 11) and -int(self.view_matrix.eye.z) in range(21, 31):
            self.currentCell = 2
        elif  int(self.view_matrix.eye.x) in range(10, 21) and -int(self.view_matrix.eye.z) in range(0, 11):
            self.currentCell = 3
        elif  int(self.view_matrix.eye.x) in range(10, 21) and -int(self.view_matrix.eye.z) in range(10, 21):
            self.currentCell = 4
        elif  int(self.view_matrix.eye.x) in range(10, 21) and -int(self.view_matrix.eye.z) in range(20, 31):
            self.currentCell = 5
        elif  int(self.view_matrix.eye.x) in range(20, 31) and -int(self.view_matrix.eye.z) in range(0, 11):
            self.currentCell = 6
        elif  int(self.view_matrix.eye.x) in range(20, 31) and -int(self.view_matrix.eye.z) in range(10, 21):
            self.currentCell = 7
        elif  int(self.view_matrix.eye.x) in range(20, 31) and -int(self.view_matrix.eye.z) in range(20, 31):
            self.currentCell = 8
        else:
            pass


    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.shader.set_eye_position(self.view_matrix.eye)

        self.model_matrix.load_identity()

        self.shader.set_light_position_second(Point(1.0, 10.0, -5.0))
        self.shader.set_light_diffuse_second(0.2, 0.2, 0.2)
        self.shader.set_light_specular_second(1.0, 1.0, 1.0)
        self.shader.set_material_specular_second(1.0, 1.0, 1.0)
        self.shader.set_material_shininess_second(40)
        self.shader.set_material_diffuse_second(1.0, 1.0, 1.0)


        self.cube.set_vertices(self.shader)

        # Setting lights before drawing them
        # Set the light position just above the eye
        self.shader.set_light_position(Point(self.eyePosX, 20.0, self.eyePosZ))
        self.shader.set_light_diffuse(0.3, 0.2, 0.5)
        self.shader.set_light_specular(0.0, 0.0, 0.0)
        self.shader.set_material_specular(0.3, 0.3, 0.3)
        self.shader.set_material_shininess(40)
        self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        self.draw_plane()

        # Draw our maze
        self.draw_maze()

        # Draw player
        # self.shader.set_light_diffuse(0.0, 1.0, 0.0)
        # self.shader.set_light_specular(0.0, 1.0, 0.0)

        # self.draw_player()

        # Set light for the sphere only # Going to be red
        self.shader.set_light_diffuse(1.0, 0.0, 0.0)
        self.shader.set_light_specular(1.0, 0.0, 0.0)

        self.sphere.set_vertices(self.shader)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(25.0, 4.0, -5.0)
        self.model_matrix.add_scale(3, 1, 3)
        self.model_matrix.add_rotate_z(self.angle)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()

        pygame.display.flip()



    def draw_wall(self, x_pos, z_pos, width=0.2, horizontal=False):
        length = 10
        self.model_matrix.push_matrix()
        self.cube.set_vertices(self.shader)
        # Set color
        if not horizontal:
            self.model_matrix.add_translation(x_pos + width/2, 5, z_pos + length/-2) # Original point
            self.model_matrix.add_scale(width, 10.0, length) # Horizontal so length will be the z-axis
        else:
            self.model_matrix.add_translation(x_pos + length/2, 5,(z_pos + width/-2)) # Original point
            self.model_matrix.add_scale(length, 10.0, width) # Vertical so length will be the x-axis
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()


    def draw_plane(self):
        self.cube.set_vertices(self.shader)
        self.model_matrix.push_matrix()
        # Add translation to our ground
        self.model_matrix.add_translation(15.0, 0.0, -15.0)
        self.model_matrix.add_scale(30.0, 0.1, 30.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    def draw_player(self):
        self.cube.set_vertices(self.shader)
        self.model_matrix.push_matrix()
        # Add translation to our ground
        self.model_matrix.add_translation(4.0, 1.0, -4.0)
        self.model_matrix.add_scale(1.0, 2.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    def draw_maze(self):
        for x, column in enumerate(self.maze.mazeList):
            for z, row in enumerate(column):
                if "south" in row:
                    self.draw_wall(x*10, -z*10, horizontal=True)
                if "north" in row:
                    self.draw_wall(x*10, -z*10 - 10, horizontal=True)
                if "east" in row:
                    self.draw_wall(x * 10 + 10, -z * 10)
                if "west" in row:
                    self.draw_wall(x * 10, -z * 10)


    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True

                    if event.key == K_c:
                        self.C_key_down = True
                    # W A S D keys movement
                    if event.key == K_w:
                        self.W_key_down = True
                    if event.key == K_s:
                        self.S_key_down = True
                    if event.key == K_a:
                        self.A_key_down = True
                    if event.key == K_d:
                        self.D_key_down = True
                    if event.key == K_SPACE:
                        self.SPACE_key_down = True
                    if event.key == K_LCTRL or event.key == K_RCTRL:
                        self.CTRL_key_down = True
                    if event.key == K_t:
                        self.T_key_down = True
                    if event.key == K_g:
                        self.G_key_down = True
                    if event.key == K_LEFT:
                        self.left_arrow_down = True
                    if event.key == K_RIGHT:
                        self.right_arrow_down = True
                    if event.key == K_DOWN:
                        self.DOWN_key_down = True
                    if event.key == K_UP:
                        self.UP_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_c:
                        self.C_key_down = False
                    if event.key == K_w:
                        self.W_key_down = False
                    if event.key == K_s:
                        self.S_key_down = False
                    if event.key == K_a:
                        self.A_key_down = False
                    if event.key == K_d:
                        self.D_key_down = False
                    if event.key == K_SPACE:
                        self.SPACE_key_down = False
                    if event.key == K_LCTRL or event.key == K_RCTRL:
                        self.CTRL_key_down = False
                    if event.key == K_t:
                        self.T_key_down = False
                    if event.key == K_g:
                        self.G_key_down = False
                    if event.key == K_LEFT:
                        self.left_arrow_down = False
                    if event.key == K_RIGHT:
                        self.right_arrow_down = False
                    if event.key == K_DOWN:
                        self.DOWN_key_down = False
                    if event.key == K_UP:
                        self.UP_key_down = False

            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()