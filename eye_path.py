import copy
import csv
import pandas as pd  




def get_tracker_data(name):

	f = pd.read_csv(name, sep="\t")
	return f


def get_dot_data(name):

	f = pd.read_csv(name, sep="\t")
	return f


def get_gaze_distance(gaze_point, dot_loc):

	if gaze_point[0] > 0:
		x_diff = float(gaze_point[0]) - float(dot_loc[0])
		y_diff = float(gaze_point[1]) - float(dot_loc[1])
		diff = (x_diff**2 + y_diff**2)**0.5
		return diff
	else:
		return -1

def get_min_gaze(gaze_points, dot, cutoff=100):

	min_dist = -1
	which_gaze = None
	n_below_x = 0
	for g in gaze_points:
		dist = get_gaze_distance(g, dot)
		if min_dist == -1 or dist < min_dist:
			min_dist = dist
			which_gaze = g
		if dist < cutoff:
			n_below_x += 1


	return min_dist, which_gaze, n_below_x



def main():
	tracker_data = get_tracker_data("data/tracker_data.csv")
	response_data = get_dot_data("data/response_data.csv")
	
	trials = pd.unique(response_data["trial_id"])
	grouped_track = tracker_data.groupby("trial_id")

	new_resp_data = copy.deepcopy(response_data)
	new_resp_data["gazeX"] = None
	new_resp_data["gazeY"] = None
	new_resp_data["gazeDist"] = None
	new_resp_data["belowX"] = None

	z = 0
	for t in trials:
		td = tracker_data[tracker_data["trial_id"] == t]
		rd = response_data[response_data["trial_id"] == t]

		gaze = zip(td["GazePointX"], td["GazePoint"])
		points = zip(rd["dl_x"], rd["dl_y"])
		ps = []
		for p in points:
			min_gaze = get_min_gaze(gaze, p, cutoff=500)
			dist = min_gaze[0]
			gaze_x = min_gaze[1][0]
			gaze_y = min_gaze[1][1]
			n_below_x = min_gaze[2]
			#new_resp_data[new_resp_data["trial_id" == t]]

			new_resp_data.at[z, 'gazeDist'] = dist
			new_resp_data.at[z, 'gazeX'] = gaze_x
			new_resp_data.at[z, 'gazeY'] = gaze_y
			new_resp_data.at[z, 'belowX'] = n_below_x

			z += 1

	new_resp_data.to_csv("data/dot_gaze.csv", sep="\t")


if __name__ == "__main__":
	main()