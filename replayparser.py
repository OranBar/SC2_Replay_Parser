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
import matplotlib.pyplot as plt
import os
import glob
import os
reduce = functools.reduce

replay_folder_path = "C:/Users/King Pub/Documents/StarCraft II/Accounts/112520872/2-S2-1-543752/Replays/Multiplayer/*"
dir_path = os.path.dirname(os.path.realpath(__file__))
SCV_BUILD_TIME = 12
ORBITAL_BUILD_TIME = 25
PLANETARY_BUILD_TIME = 36


def get_latest_replay():
    # * means all if need specific format then *.csv
    list_of_files = glob.glob(replay_folder_path)
    latest_file = max(list_of_files, key=os.path.getctime)
    latest_file = latest_file.replace('\\', '/')
    return latest_file


def create_dbg_file(gamedata, printToConsole=True):
    f = open(dbgFileName, "w")
    for event in gamedata:
        f.write(str(event))
        f.write('\n')
        if(printToConsole):
            print(str(event))
            print('\n')

    f.close()
    print('Created file '+dbgFileName)

# Only takes into account timings of completed scv.
# It includes orbital transformation time, time floating
# Does not take into account scv cancels (usure if it makes any difference tho)


def get_command_center_idle_time():
    data = code.get_command_centers_production_queue()
    orbitals_finish_events = code.get_orbitals_created()

    idleSCVtimeline = {}
    for cc_tag, cc_prod in data.items():
        cc_orbital_time = code.filter_by_tags(cc_tag, orbitals_finish_events)
        cc_orbital_time = int(
            cc_orbital_time[0]['_gameloop']) if cc_orbital_time != [] else -1

        print("cc orbital time: "+str(cc_orbital_time))
        scv_time_deltas = []
        idleSCVtimeline[cc_tag] = scv_time_deltas

        for i in range(len(cc_prod)-2):
            scv_curr = cc_prod[i]
            scv_next = cc_prod[i+1]
            idleTimeBetweenScvs = scv_next['_gameloop'] - \
                scv_curr['_gameloop'] - SCV_BUILD_TIME*22.4

            # if orbitale tra scv_curr e scv_next
            orbital_was_made_between_scvs = (scv_curr['_gameloop'] < cc_orbital_time
                                             and scv_next['_gameloop'] > cc_orbital_time)

            if(orbital_was_made_between_scvs):
                idleTimeBetweenScvs = idleTimeBetweenScvs - ORBITAL_BUILD_TIME*22.4

            idleTimeBetweenScvs = code.gameloopToSeconds(idleTimeBetweenScvs)
            if(idleTimeBetweenScvs <= 0.1):
                idleTimeBetweenScvs = 0

            scv_time_deltas.append(idleTimeBetweenScvs)

    return idleSCVtimeline


# -----------------------------------------------------------------------------

if __name__ == "__main__":

    myId = 1
    # replayFilePath = dir_path+"\\mvp.SC2Replay"
    replayFilePath = get_latest_replay()
    print(replayFilePath)

    writeToFile = True
    dbgFileName = "Dbg1.txt"

    code = SC2ReplayData_Extractor(replayFilePath, "GengisKhan")

    # create_dbg_file(code.get_replay_tracker_events())
    # exit

    # rslt = parse_replay(replayFilePath)
    # print(rslt)
    # data = code.get_replay_game_events()
    # data = code.get_command_centers_production_queue().values()

    # data = code.get_orbitals_created()
    # data = code.get_replay_tracker_events()
    # create_dbg_file(data, True)

    scv_idle_per_cc = get_command_center_idle_time()

    print("\nIdle time per cc:\n ")
    print(scv_idle_per_cc)

    scv_idle_total_per_cc = {}
    i = 0
    plt.figure()
    for cc_key, cc_prod in scv_idle_per_cc.items():
        if(i >= 4):
            break

        scv_idle_total_per_cc[cc_key] = sum(cc_prod)
        if(len(cc_prod) > 3):
            plt.subplot("22"+str(i+1))
            plt.plot(cc_prod[:-1])
            plt.ylabel('Seconds between SCVs')

        i = i+1

    print("\nTotal idle time per cc:\n ")
    print(scv_idle_total_per_cc)

    print("\nTotal idle time:\n ")
    print(int(sum(scv_idle_total_per_cc.values())))

    print("\n Finish! :D\n\n\n------------------------------------------------------------------------")

    plt.show()
    exit

    # events = filter(code.filter_SUnitChangeType_MyOrbitals,
    #                 code.get_replay_tracker_events())
    # events = code.get_replay_tracker_events()
    # create_dbg_file(events)"""


# myCommandCentersTags = code.get_my_command_centers_tags()

# data = code.get_my_SCVs_born_events()
# data = code.get_command_centers_production_queue()
# for tagToProductionQueue in data:
# print(tagToProductionQueue);

# """
# if(writeToFile):
