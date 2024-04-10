maze = {}
for i in range(9):
    maze[i] = []

mazelist = []
for column in range(3):
    mazelist.append([])
    for row in range(3):
        mazelist[column].append([])

mazelist[0].append("south")
mazelist[0].append("west")
mazelist[0].append("east")

mazelist[1].append("west")
mazelist[1].append("east")

mazelist[2].append("east")
mazelist[2].append("north")

mazelist[5].append("north")

mazelist[8].append("north")
mazelist[8].append("east")

mazelist[7].append("east")
mazelist[7].append("west")

mazelist[6].append("south")
mazelist[6].append("east")
mazelist[6].append("west")