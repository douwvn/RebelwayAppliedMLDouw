
import numpy as np

coordinates = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4), (3, 4), (3, 5), (3, 6), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]


def make_move(coordinates)
for idx, coordinate in enumerate(coordinates):

	current_pos = coordinate  

	# get previous position index
	index = idx - 1
	if index <= 0:
	    n_index = 0
	else:
		n_index = index

	previous_pos = coordinates[n_index]     
	  
	current_pos_vec = np.array(current_pos)
	previous_pos_vec = np.array(previous_pos)

	movement_vec = current_pos_vec - previous_pos_vec


	print(movement_vec)





