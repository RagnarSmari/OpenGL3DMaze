

class MazeMaker():
    def __init__(self) -> None:
        self.mazeList = []
        for column in range(3):
            self.mazeList.append([])
            for row in range(3):
                self.mazeList[column].append([])
        self.initialize_walls()

    def initialize_walls(self):
        self.mazeList[0][0].append("south")
        self.mazeList[0][0].append("west")
        self.mazeList[0][0].append("east")

        self.mazeList[0][1].append("west")
        self.mazeList[0][1].append("east")

        self.mazeList[0][2].append("west")
        self.mazeList[0][2].append("north")

        self.mazeList[1][0].append("south")
        self.mazeList[1][0].append("east")
        self.mazeList[1][0].append("west")


        self.mazeList[1][1].append("east")
        self.mazeList[1][1].append("west")
        self.mazeList[1][1].append("south")

        self.mazeList[1][2].append("north")

        self.mazeList[2][0].append("south")
        self.mazeList[2][0].append("east")
        self.mazeList[2][0].append("west")
        self.mazeList[2][0].append("sphere")
        
        self.mazeList[2][1].append("east")
        self.mazeList[2][1].append("west")

        self.mazeList[2][2].append("north")
        self.mazeList[2][2].append("east")



    

    def get_maze_index(self, currCell):
        if currCell == 0:
            return 0,0
        elif currCell == 1:
            return 0,1
        elif currCell == 2:
            return 0,2
        elif currCell == 3:
            return 1,0
        elif currCell == 4:
            return 1,1
        elif currCell == 5:
            return 1,2
        elif currCell == 6:
            return 2,0
        elif currCell == 7:
            return 2,1
        elif currCell == 8:
            return 2,2


    # def draw_wall(self, x_pos, z_pos, width=0.2,set_vertices=False, horizontal=False):
    #     length = 1
    #     self.model_matrix.push_matrix()
    #     if set_vertices:
    #         self.cube.set_vertices(self.shader)
    
    #     if not horizontal:
    #         self.model_matrix.add_translation(x_pos + width/2, 5, z_pos + length/-2) # Original point
    #         self.model_matrix.add_scale(width, 10.0, length) # Horizontal so length will be the z-axis
    #     else:
    #         self.model_matrix.add_translation(x_pos + length/2, 5,(z_pos + width/-2)) # Original point
    #         self.model_matrix.add_scale(length, 10.0, width) # Vertical so length will be the x-axis
    #     self.shader.set_model_matrix(self.model_matrix.matrix)
    #     self.cube.draw(self.shader)
    #     self.model_matrix.pop_matrix()


    # def draw(self):
    #     for x, column in enumerate(self.mazeList):
    #         for z, row in enumerate(column):
    #             print("row",row)
    #             if "south" in row:
    #                 self.draw_wall(x, -z, horizontal=True)
    #             if "north" in row:
    #                 self.draw_wall(x + 0.9, -z, horizontal=True)
    #             if "east" in row:
    #                 self.draw_wall(x, -z - 0.9)
    #             if "west" in row:
    #                 self.draw_wall(x, -z)


