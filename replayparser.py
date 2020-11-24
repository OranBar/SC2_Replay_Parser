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

myId = 1
replayFilePath = "C:\\Users\\King Pub\\Documents\\StarCraft II\\Accounts\\112520872\\2-S2-1-543752\\Replays\\Multiplayer\\testreplay.SC2Replay"

writeToFile = True
dbgFileName = "Dbg1.txt"

code = SC2Coach(replayFilePath, myId)

# events = filter(code.filter_SUnitChangeType_MyOrbitals,
#                 code.get_replay_tracker_events())

data = code.get_command_centers_production_queue()

# myCommandCentersTags = code.get_my_command_centers_tags()

# data = code.get_my_SCVs_born_events()
# data = code.get_command_centers_production_queue()
# for tagToProductionQueue in data:
	# print(tagToProductionQueue);

# """
data = data.values()
if(writeToFile):
	f = open(dbgFileName, "w")
	for event in data:
		f.write(str(event))
		f.write('\n')

	f.close()
	print('Created file '+dbgFileName)
else:
	for event in data:
		
		print(str(event))
		print('\n')
# """

print("\n Finish! :D\n\n\n------------------------------------------------------------------------")
