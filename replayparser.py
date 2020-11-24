# required_internal_files = ['replay.details',
#                         'replay.details.backup',
#                         'replay.initData',
#                         'replay.game.events',
#                         'replay.message.events',
#                         'replay.tracker.events'
#                         ]

from SC2Coach import SC2Coach
import mpyq
import os
from s2protocol import versions

myId = 2
replayFilePath = "C:\\Users\\King Pub\\Documents\\StarCraft II\\Accounts\\112520872\\2-S2-1-543752\\Replays\\Multiplayer\\testreplay.SC2Replay"
dbgFileName = "Dbg1.txt"

code = SC2Coach(replayFilePath, myId=2)

events = filter(code.filter_SUnitChangeType_MyOrbitals,
                code.get_replay_tracker_events())

data = code.get_units_done_events()

f = open(dbgFileName, "w")
for event in data:
	event['time'] = code.gameloopToMinutes(event['_gameloop'])
	f.write(str(event))
	f.write('\n')

f.close()
