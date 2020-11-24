import unittest
import mpyq
import os
from s2protocol import versions

gameLoopsInOneSecond = 22.4

archive = mpyq.MPQArchive("C:\\Users\\King Pub\\Documents\\StarCraft II\\Accounts\\112520872\\2-S2-1-543752\\Replays\\Multiplayer\\Jagannatha LE (28).SC2Replay")
contents = archive.header['user_data_header']['content']
header = versions.latest().decode_replay_header(contents)

base_build = header['m_version']['m_baseBuild']
try:
	protocol = versions.build(base_build)
except Exception as e:
	pass

required_internal_files = ['replay.details',
					'replay.details.backup',
					'replay.initData',
					'replay.game.events',
					'replay.message.events',
					'replay.tracker.events'		
]

# {'m_unitTagIndex': 320, 'm_unitTagRecycle': 1, 'm_unitTypeName': b'Marine', 'm_controlPlayerId': 2, 'm_upkeepPlayerId': 2, 'm_x': 55, 'm_y': 41, 'm_creatorUnitTagIndex': 216,
# 	'm_creatorUnitTagRecycle': 1, 'm_creatorAbilityName': b'BarracksTrain', '_event': 'NNet.Replay.Tracker.SUnitBornEvent', '_eventid': 1, '_gameloop': 6802, '_bits': 520}


contents = archive.read_file('replay.tracker.events')
print(len(contents))
i = 0

filterEvents = lambda e1: (e1["_event"] == 'NNet.Replay.Tracker.SUnitBornEvent' and
                           e1["m_controlPlayerId"] == 2 and
                           e1['m_unitTypeName'] == b'SCV' and
						   e1['_gameloop'] != 0)




units_created_events = filter( filterEvents, protocol.decode_replay_tracker_events(contents) )
for event in units_created_events:
	# print(event)
	print("SCV created at time "+ str(event['_gameloop']/gameLoopsInOneSecond) )


# contents = archive.read_file('replay.game.events')
# print ( len(contents) )
# i = 0
# for event in protocol.decode_replay_game_events(contents):
# 	i = i+1
# 	print(event)
# 	print('\n')
# 	if(i > 100):
# 		break

# i = i + 1
# if(i > 300):
# 	print(event)
# 	print('\n')

# if(i > 500):
# 	break

# for internal_file_name in required_internal_files:
# 	contents = archive.read_file(internal_file_name)
