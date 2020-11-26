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
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def create_dbg_file(gamedata):
	f = open(dbgFileName, "w")
	for event in gamedata:
		f.write(str(event))
		f.write('\n')

	f.close()
	print('Created file '+dbgFileName)


def get_CC_idle_time(production_queue):
	idleSCVtime = {}
	for cc_key, cc_prod in production_queue.items():
		scv_time_deltas = []
		idleSCVtime[cc_key] = scv_time_deltas

		for i in range(len(cc_prod)-2):
			scv_curr = cc_prod[i]
			scv_next = cc_prod[i+1]
			scv_build_time = 12
			idleTimeBetweenScvs = scv_next['_gameloop'] - scv_curr['_gameloop']

			idleTimeBetweenScvs = code.gameloopToMinutes(idleTimeBetweenScvs)
			if(idleTimeBetweenScvs < 0.001):
				idleTimeBetweenScvs = 0

			scv_time_deltas.append(idleTimeBetweenScvs)

	return idleSCVtime

#Only takes into account timings of completed scv. 
#It includes orbital transformation time, time floating
#Does not take into account scv cancels (usure if it makes any difference tho)
def get_command_center_idle_time():
	data = code.get_command_centers_production_queue()

	idleSCVtimeline = {}
	for cc_key, cc_prod in data.items():
		scv_time_deltas = []
		idleSCVtimeline[cc_key] = scv_time_deltas

		for i in range(len(cc_prod)-2):
			scv_curr = cc_prod[i]
			scv_next = cc_prod[i+1]
			scv_build_time = 12
			idleTimeBetweenScvs = scv_next['_gameloop'] - \
				scv_curr['_gameloop'] - 12*22.4

			idleTimeBetweenScvs = code.gameloopToSeconds(idleTimeBetweenScvs)
			if(idleTimeBetweenScvs <= 0.1):
				idleTimeBetweenScvs = 0

			scv_time_deltas.append(idleTimeBetweenScvs)

	return idleSCVtimeline
	

#-----------------------------------------------------------------------------

if __name__ == "__main__":
	
	myId = 1
	replayFilePath = dir_path+"\\testreplay.SC2Replay"

	writeToFile = True
	dbgFileName = "Dbg2.txt"
	reduce = functools.reduce

	code = SC2ReplayData_Extractor(replayFilePath, myId)

	scv_idle_per_cc = get_command_center_idle_time()

	print("\nIdle time per cc:\n ")
	print(scv_idle_per_cc)

	scv_idle_total_per_cc = {}
	for cc_key, cc_prod in scv_idle_per_cc.items():
		scv_idle_total_per_cc[cc_key] = sum(cc_prod)

	print("\nTotal idle time per cc:\n ")
	print(scv_idle_total_per_cc)

	print("\nTotal idle time:\n ")
	print(int(sum(scv_idle_total_per_cc.values())))

	# events = filter(code.filter_SUnitChangeType_MyOrbitals,
	#                 code.get_replay_tracker_events())
	# events = code.get_replay_tracker_events()
	# create_dbg_file(events)

	print("\n Finish! :D\n\n\n------------------------------------------------------------------------")
	exit


# myCommandCentersTags = code.get_my_command_centers_tags()

# data = code.get_my_SCVs_born_events()
# data = code.get_command_centers_production_queue()
# for tagToProductionQueue in data:
	# print(tagToProductionQueue);

# """
# if(writeToFile):
