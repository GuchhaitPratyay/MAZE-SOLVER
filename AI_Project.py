import numpy as np
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0      #g is the cost from the start to current Node
        self.h = 0      #h is the heuritic cost estimation for current Node to the end Node
        self.f = 0      #f is the total cost of the present node (f=g+h)

    #returns True or Flase according to position
    def __eq__(self, other):
        return self.position == other.position

#This function return the path of the search
def returnPath(current_node,maze):
    path = []
    no_rows, no_columns = np.shape(maze)        #shape funtion asssigns the number of rows and colloumns 
    # here we create the initialized result maze with -1 in every position
    result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # Return reversed path as we need to show from start to end path
    path = path[::-1]
    startValue = 0
    # we update the path of start to end found by A-star serch with every step incremented by 1
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = startValue
        startValue += 1
    return result


def search(maze, cost, start, end):
    # Create start and end node with initized values for g, h and f
    startNode = Node(None, tuple(start))
    startNode.g = startNode.h = startNode.f = 0
    endNode = Node(None, tuple(end))
    endNode.g = endNode.h = endNode.f = 0

    # Initialize both yetToVisit and visited list
    # in this list we will put all node that are yet_to_visit for exploration. 
    # From here we will find the lowest cost node to expand next
    yetToVisitList = []  
    # in this list we will put all node those already explored so that we don't explore it again
    visitedList = [] 
    
    # Add the start node
    yetToVisitList.append(startNode)
    
    # Adding a stop condition. This is to avoid any infinite loop and stop 
    # execution after some reasonable number of steps
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    # what squares do we search . serarch movement is left-right-top-bottom 
    #(4 movements) from every positon

    move  =  [[-1, 0 ], # go up
              [ 0, -1], # go left
              [ 1, 0 ], # go down
              [ 0, 1 ]] # go right

    #find maze has got how many rows and columns 
    no_rows, no_columns = np.shape(maze)
    
    # Loop until you find the end
    
    while len(yetToVisitList) > 0:        
        # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
        outer_iterations += 1         
        # Get the current node
        current_node = yetToVisitList[0]
        current_index = 0
        for index, item in enumerate(yetToVisitList):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        # if we hit this point return the path such as it may be no solution or 
        # computation cost is too high
        if outer_iterations > max_iterations:
            print ("Path cannot be found because of too many iterations")
            return returnPath(current_node,maze)

        # Pop current node out off yet_to_visit list, add to visited list
        yetToVisitList.pop(current_index)
        visitedList.append(current_node)

        # test if goal is reached or not, if yes then return the path
        if current_node == endNode:
            return returnPath(current_node,maze)

        # Generate children from all adjacent squares
        children = []

        for new_position in move: 

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range (check if within maze boundary)
            if (node_position[0] > (no_rows - 1) or node_position[0] < 0 or node_position[1] > (no_columns -1) or node_position[1] < 0):
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            
            # Child is on the visited list (search entire visited list)
            if len([visitedChild for visitedChild in visitedList if visitedChild == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + cost
            ## Heuristic costs calculated here, this is using eucledian distance
            child.h = (((child.position[0] - endNode.position[0]) ** 2) + 
                       ((child.position[1] - endNode.position[1]) ** 2)) 

            child.f = child.g + child.h

            # Child is already in the yet_to_visit list and g cost is already lower
            if len([i for i in yetToVisitList if child == i and child.g > i.g]) > 0:
                continue
            # Add the child to the yetToVisitList
            yetToVisitList.append(child)


if __name__ == '__main__':

    maze = [[0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0]]
    
    start = [0, 0] # starting position
    end = [5,5] # ending position
    cost = 1 # cost per movement
      
    path = search(maze,cost, start, end)
    #print(path)
    #print("\n")
    print("\n".join([' '.join(["{:" " >2d}".format(item) for item in row ])for row in path]))