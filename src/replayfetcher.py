import glob
import os

sc2_replay_path = "C:/Users/King Pub/Documents/StarCraft II/Accounts/112520872/2-S2-1-543752/Replays/Multiplayer/*"
test_replays_path = "E:/Git_Repos/Starcraft_Replay_Parser/replays*"
dir_path = os.path.dirname(os.path.realpath(__file__))


def get_latest_replay_file_path():
	# * means all if need specific format then *.civ
	list_of_files = glob.glob(sc2_replay_path)
	latest_file = max(list_of_files, key=os.path.getctime)
	latest_file = latest_file.replace('\\', '/')
	return latest_file


def get_test_replay_file_path(replay_name):
	list_of_files = glob.glob(test_replays_path)

	file_index = list_of_files.index(replay_name)
	file = list_of_files[file_index]
	file = file.replace('\\', '/')
	return file
