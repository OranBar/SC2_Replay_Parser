from zephyrus_sc2_parser import parse_replay
import glob
import os
import json

replay_folder_path = "C:/Users/King Pub/Documents/StarCraft II/Accounts/112520872/2-S2-1-543752/Replays/Multiplayer/*"


def get_latest_replay():
    # * means all if need specific format then *.civ
    list_of_files = glob.glob(replay_folder_path)
    latest_file = max(list_of_files, key=os.path.getctime)
    latest_file = latest_file.replace('\\', '/')
    return latest_file


if __name__ == "__main__":
    # replayFilePath = get_latest_replay()
    replayFilePath = replay_folder_path[:-1] + "testreplay.SC2Replay"
    players, timeline, summary_stats, metadata, k = parse_replay(
        replayFilePath)
    y = json.dumps(timeline[10:20])
    dbgFileName = "zephyrus.json"
    f = open(dbgFileName, "w")
    f.write(y)
    f.close()
    print('Created file '+dbgFileName)
