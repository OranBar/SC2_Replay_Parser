# required_internal_files = ['replay.details',
#                         'replay.details.backup',
#                         'replay.initData',
#                         'replay.game.events',
#                         'replay.message.events',
#                         'replay.tracker.events'
#                         ]

from SC2ReplayData_Extractor import SC2ReplayData_Extractor
import mpyq
import os
import functools
from s2protocol import versions
from zephyrus_sc2_parser import parse_replay
# import matplotlib.pyplot as plt
import os
import glob
import os
from SC2Sensei import SC2AnalizedReplay
from replayfetcher import get_latest_replay_file_path
reduce = functools.reduce

dbg_file_name = "logs/Dbg3.txt"
replay_folder_path = "C:/Users/King Pub/Documents/StarCraft II/Accounts/112520872/2-S2-1-543752/Replays/Multiplayer/*"
player_to_analyze_name = "GengisKhan"
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    my_id = 1
    # replayFilePath = dir_path+"\\mvp.SC2Replay"
    replay_file_path = get_latest_replay_file_path()
    print(replay_file_path)

    writeToFile = True
    
    replay_data_extractor = SC2ReplayData_Extractor(replay_file_path, player_to_analyze_name)
    output = SC2AnalizedReplay(replay_data_extractor)
    # Make Json: Start, End, Name

    output.get_command_center_timelines()
    # Use the ReplayExtractor to get a List of CommandCenter Objects

    # Using this list, build the arrays neede to draw the graph

    # code = SC2ReplayData_Extractor(replayFilePath, "GengisKhan")

    # scv_idle_per_cc = code.get_command_center_idle_time()

    # print("\nIdle time per cc:\n ")
    # print(scv_idle_per_cc)

    # scv_idle_total_per_cc = {}
    # i = 0
    # plt.figure()
    # for cc_key, cc_prod in scv_idle_per_cc.items():
    #     if(i >= 4):
    #         break

    #     scv_idle_total_per_cc[cc_key] = sum(cc_prod)
    #     if(len(cc_prod) > 3):
    #         plt.subplot("22"+str(i+1))
    #         plt.plot(cc_prod[:-1])
    #         plt.ylabel('Seconds between SCVs')

    #     i = i+1

    # print("\nTotal idle time per cc:\n ")
    # print(scv_idle_total_per_cc)

    # print("\nTotal idle time:\n ")
    # print(int(sum(scv_idle_total_per_cc.values())))

    # print("\n Finish! :D\n\n\n------------------------------------------------------------------------")

    # plt.show()
    # exit


#---------------------- main() END ------------------------------------------------------------------

def create_dbg_file(gamedata, printToConsole=True):
    f = open(dbg_file_name, "w")
    for event in gamedata:
        f.write(str(event))
        f.write('\n')
        if(printToConsole):
            print(str(event))
            print('\n')

    f.close()
    print('Created file '+dbg_file_name)
