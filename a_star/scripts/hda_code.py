import hou
import math
import sys
import random
sys.path.append("/home/douw.vanniekerk/development/RebelwayAppliedMLDouw.git/houdini/a_star/scripts/")

from a_star import AStarPathFinding

### Randomly position and solve the maze of one target object, an n amount of npc objects based on the npc paramater on the HDA
### Execute button callback script: hou.phm().main(kwargs)

def onClickExecute(kwargs):
    util = Test()
    util.printer()


def get_main_char_path():
    main_char_path = hou.pwd().parm("main_char").eval()
    return main_char_path


def get_npc_char_path_list(kwargs):
    node = kwargs['node']
    npc_amount = node.parm("npcs").eval()
    npc_node_list = node.parm("npcs").multiParmInstances()

    npc_path_list = []
    for idx, npc in enumerate(npc_node_list):
        par_name = "npc_" + str(idx + 1)

        npc_path = node.parm(par_name).eval()
        npc_path_list.append(npc_path)
    return(npc_path_list, npc_amount)


def get_maze_from_grid():
    grid = hou.pwd().parm('grid_path').eval()
    geo = hou.node(grid).geometry()

    prims = geo.prims()
    num_rows = num_columns = int(math.sqrt(len(prims)))

    # Initialize the matrix
    grid_matrix = []

    # Populate the matrix
    for row in range(num_rows):
        row_data = []
        for col in range(num_columns):
            prim_index = row * num_columns + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")
            row_data.append(1 if color == (1.0,1.0,1.0) else 0)
        grid_matrix.append(row_data)

    return grid_matrix


def position_object(obj_path, row, col,cell_size=1):
    main_char = hou.node(obj_path)
    world_x = col * cell_size
    world_z = row * cell_size

    center = main_char.parmTuple("t").eval()
    main_char.parmTuple("t").set((world_x, 0, world_z))

    pos = (row, col)
    return pos


def reset_objects_position_key(kwargs):
    npc_paths = get_npc_char_path_list(kwargs)
    paths = npc_paths[:-1]
    paths = paths[0]

    for path in paths:
        obj = hou.node(path)
        parm_tuple = obj.parmTuple("t")
        reset_values = (0.0, 0.0, 0.0)

        for idx, value in enumerate(reset_values):
            parm = parm_tuple[idx]
            parm.deleteAllKeyframes()
            parm.set(value)


def set_frame_range(path_length):
    set_frame_range = hou.playbar.setFrameRange(1, path_length)
    set_playbar_range = hou.playbar.setPlaybackRange(1, path_length)


def get_unique_random_positions(matrix, n):
    # Collect all valid (row, col) positions where value == 1
    valid_positions = [
        (r, c)
        for r in range(len(matrix))
        for c in range(len(matrix[0]))
        if matrix[r][c] == 1
    ]

    if n > len(valid_positions):
        raise ValueError("Requested more positions than available 1's in the matrix")

    # Randomly choose n unique positions
    return random.sample(valid_positions, n)



def solve_maze(kwargs):
    main_char_path = get_main_char_path()
    npc_char_paths_return = get_npc_char_path_list(kwargs)
    npc_char_paths = npc_char_paths_return[0]
    npc_amount_number = npc_char_paths_return[1]

    # calc char amount = npc + 1 for main char
    char_amount = npc_amount_number + 1

    maze1 = get_maze_from_grid()

    positions = get_unique_random_positions(maze1, char_amount)
    start_coordinates = positions[1:]
    target_coordinates = positions[0]

    target_pos = position_object(obj_path=main_char_path, row=target_coordinates[0], col=target_coordinates[1])

    path_list = []
    for npc_index, coordinate in enumerate(start_coordinates):
        npc_char_path = npc_char_paths[npc_index]
        start_pos = position_object(obj_path=npc_char_path, row=coordinate[0], col=coordinate[1])
        maze1 = get_maze_from_grid()
        for row in maze1:
            print(row)

        pathfinder = AStarPathFinding(maze1, start_pos, target_pos)
        path = pathfinder.find_path()

        if path:
            path_list.append(path)
            #print("Path found:", path)
        else:
            print("No path found.")

    return path_list


def set_global_frame_range(path_list):
    # get the longest path
    longest_path = max(path_list, key=len)
    longest_path_length = len(longest_path)

    # set global frame range based on the longest_path_length
    set_frame_range(longest_path_length)


def animate_objects(kwargs):
    travel_paths = solve_maze(kwargs)
    set_global_frame_range(travel_paths)
    npc_paths = get_npc_char_path_list(kwargs)
    paths = npc_paths[:-1]
    paths = paths[0]

    for idx, path in enumerate(paths):
            travel_path = travel_paths[idx]
            path_length = len(travel_paths[idx])
            obj = hou.node(path)
            frame_range = path_length

            for idx, number in enumerate(range(frame_range)):
                frame = number + 1
                coordinate = travel_path[idx]
                col_val = coordinate[1]
                row_val = coordinate[0]

                # move playbar
                move = hou.setFrame(frame)

                parm_tuple = obj.parmTuple("t")
                parm_values = (col_val,  0, row_val)

                # set position values
                current_position = position_object(obj_path=path, row=row_val, col=col_val)

                # set keys
                for idx, value in enumerate(parm_values):
                    # key position values
                    key = hou.Keyframe()
                    key.setFrame(frame)
                    key.setValue(value)
                    parm = parm_tuple[idx]
                    parm.setKeyframe(key)


def main(kwargs):
    reset_objects_position_key(kwargs)
    animate_objects(kwargs)



