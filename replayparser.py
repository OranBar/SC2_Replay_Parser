import unittest
import mpyq
import os
from s2protocol import versions

myId = 2
replayFilePath = "C:\\Users\\King Pub\\Documents\\StarCraft II\\Accounts\\112520872\\2-S2-1-543752\\Replays\\Multiplayer\\testreplay.SC2Replay"

gameLoopsInOneSecond = 22.4
TEMPO_PRODUZIONE_SCV = 12

class SC2Coach:

	# required_internal_files = ['replay.details',
    #                         'replay.details.backup',
    #                         'replay.initData',
    #                         'replay.game.events',
    #                         'replay.message.events',
    #                         'replay.tracker.events'
    #                         ]

	def __init__(self, replayFilePath):
		# self.replayFilePath = replayFilePath
		self.myId = self.get_my_id("GengisKhan")
		self.replayHeader, self.protocol = self.build_replay(replayFilePath)

	def build_replay(self, path):
		self.archive = mpyq.MPQArchive(path)
		replay = self.archive.header['user_data_header']['content']
		header = versions.latest().decode_replay_header(replay)

		base_build = header['m_version']['m_baseBuild']
		try:
			return (replay, versions.build(base_build))
		except Exception as e:
			return (replay, None)
		
		
	def get_my_id(self, string):
		#TODO
		return myId

	def gameloopToMinutes(self, gameloop):
		parteDecimale = round(gameloop / gameLoopsInOneSecond % 60 * 0.01, 2)
		minutiGiustiGiusti = int(
			gameloop / gameLoopsInOneSecond) // 60 + parteDecimale
		return minutiGiustiGiusti

	def SelectCommandCenterFinishEvent(self, myList, tagIndx, tagRecy):
		for event in myList:
			if(event['m_unitTagIndex'] == tagIndx and event['m_unitTagRecycle'] == tagRecy):
				return event

		return None
	
	def CommandCenterCreatedEvent_Me(self, e1): 
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitInitEvent' and
                                               #   e1['_gameloop'] != 0 )
                                               e1['_gameloop'] != 0 and
                                               e1["m_controlPlayerId"] == self.myId and
                                               # e1['m_unitTypeName'] == b'OrbitalCommand')
                                               e1['m_unitTypeName'] == b'CommandCenter')

	def OrbitalCreatedEvent_Me(self, e1): 
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitTypeChangeEvent' and
                                        #    e1['_gameloop'] != 0 )
                                         e1['_gameloop'] != 0 and
                                        #  e1["m_controlPlayerId"] == self.myId and
                                         e1['m_unitTypeName'] == b'OrbitalCommand')
                                        #  e1['m_unitTypeName'] == b'CommandCenter')


	def SCVCreatedEvents_Me(self, e1): 
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitBornEvent' and
                                     e1["m_controlPlayerId"] == self.myId and
                                     e1['m_unitTypeName'] == b'SCV' and
                                     e1['_gameloop'] != 0)

	def UnitsCreatedEvents_Me(self, e1): 
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitInitEvent' and
                                         e1["m_controlPlayerId"] == self.myId and
                                         e1['_gameloop'] != 0)

	def SUnitsDone(self, e1): 
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitDoneEvent' and
                             e1['_gameloop'] != 0)

	def get_orbitals_created(self):
		replay = self.archive.read_file('replay.tracker.events')

		return filter(self.OrbitalCreatedEvent_Me, self.protocol.decode_replay_tracker_events(replay))

	def get_command_centers_created(self):
		replay = self.archive.read_file('replay.tracker.events')

		return filter(self.CommandCenterCreatedEvent_Me, self.protocol.decode_replay_tracker_events(replay))
	
	def get_replay_tracker_events(self):
		replay = self.archive.read_file('replay.tracker.events')
		return self.protocol.decode_replay_tracker_events(replay)


	# for internal_file_name in required_internal_files:
	# 	contents = archive.read_file(internal_file_name)

	# {'m_unitTagIndex': 320, 'm_unitTagRecycle': 1, 'm_unitTypeName': b'Marine', 'm_controlPlayerId': 2, 'm_upkeepPlayerId': 2, 'm_x': 55, 'm_y': 41, 'm_creatorUnitTagIndex': 216,
	# 	'm_creatorUnitTagRecycle': 1, 'm_creatorAbilityName': b'BarracksTrain', '_event': 'NNet.Replay.Tracker.SUnitBornEvent', '_eventid': 1, '_gameloop': 6802, '_bits': 520}

code = SC2Coach(replayFilePath)

events = filter(code.OrbitalCreatedEvent_Me, code.get_replay_tracker_events())

f=open("UnitsEvents4.txt", "w")
for event in events:
	
	event['time'] = code.gameloopToMinutes(event['_gameloop'])
	f.write(str(event))
	f.write('\n')

f.close()


