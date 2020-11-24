import mpyq
import os
from s2protocol import versions

gameLoopsInOneSecond = 22.4


class SC2Coach:

	def __init__(self, replayFilePath, myId):
		self.myId = myId
		# self.myId = self.get_my_id("GengisKhan") 
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

	#TODO
	def get_my_id(self, string):
		return self.myId

	def map_unitTag_tuple(self, e1):
		return (e1['m_unitTagIndex'], e1['m_unitTagRecycle'])

	# def filter_by_tagIndex(self, e1, tagIndex):

	def get_my_command_centers_tags(self):
		myCommandCentersInit = self.get_command_centers_created()
		myCommandCenterTags = list(map(self.map_unitTag_tuple, myCommandCentersInit))

		return myCommandCenterTags

	def filter_by_tags(self, tags, eventsList):
		rslt = [event for event in eventsList
                    if((event['m_unitTagIndex'], event['m_unitTagRecycle']) in tags)]
		return rslt;

	def filter_by_creatorTags(self, creatorTags, eventsList):
		rslt = [event for event in eventsList
                    if(event['m_creatorUnitTagIndex'] == creatorTags[0] and event['m_creatorUnitTagRecycle'] == creatorTags[1]) ]
		return rslt

	def get_command_centers_production_queue(self):
		myCommandCenterTags = self.get_my_command_centers_tags()

		rslt = {}
		for tag in myCommandCenterTags:
			# curr_CC_ProductionQueue = filter(
			# 	lambda e: (e['m_creatorUnitTagIndex'], e['m_creatorUnitTagRecycle']) in myCommandCenterTags, self.get_my_SCVs_born_events())
			curr_CC_ProductionQueue = self.filter_by_creatorTags(
				tag, self.get_my_SCVs_born_events())

			rslt[tag] = curr_CC_ProductionQueue

		return rslt

	def get_command_centers_finish(self):
		myCommandCenterTags = self.get_my_command_centers_tags()
		#TODO: continue
		rslt = self.filter_by_tags(
			myCommandCenterTags, self.get_my_units_done_events())

		rslt = list(map(self.map_add_time_to_events, rslt))
		return rslt

	def get_my_units_done_events(self):
		replay = self.archive.read_file('replay.tracker.events')

		rslt = filter(self.filter_SUnitsDoneEvent, self.get_replay_tracker_events())
		
		rslt = list(map(self.map_add_time_to_events, rslt))
		return rslt

	def get_my_SCVs_born_events(self):
		replay = self.archive.read_file('replay.tracker.events')

		rslt = filter(self.filter_SCVBornEvent, self.get_replay_tracker_events())

		rslt = list(map(self.map_add_time_to_events, rslt))
		return rslt

	def get_orbitals_created(self):
		replay = self.archive.read_file('replay.tracker.events')

		rslt = filter(self.filter_SUnitChangeType_MyOrbitals, self.get_replay_tracker_events())
		rslt = list(map(self.map_add_time_to_events, rslt))
		return rslt

	def get_command_centers_created(self):
		replay = self.archive.read_file('replay.tracker.events')

		rslt = list(filter(self.filter_MyCC_UnitInit, self.get_replay_tracker_events()))
		rslt = list(map(self.map_add_time_to_events, rslt))
		return rslt

	def get_replay_tracker_events(self):
		replay = self.archive.read_file('replay.tracker.events')

		rslt = self.protocol.decode_replay_tracker_events(replay)
		rslt = list(map(self.map_add_time_to_events, rslt))
		return rslt

	def filter_MyCC_UnitInit(self, e1):
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitInitEvent' and
                    e1['_gameloop'] != 0 and
                    e1["m_controlPlayerId"] == self.myId and
                    e1['m_unitTypeName'] == b'CommandCenter')

	def filter_SUnitChangeType_MyOrbitals(self, e1):
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitTypeChangeEvent' and
                    e1['_gameloop'] != 0 and
                    e1['m_unitTypeName'] == b'OrbitalCommand')

	def filter_SCVBornEvent(self, e1):
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitBornEvent' and
                    e1["m_controlPlayerId"] == self.myId and
                    e1['m_unitTypeName'] == b'SCV' and
                    e1['_gameloop'] != 0)

	def filter_SUnitInit_Mine(self, e1):
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitInitEvent' and
                    e1["m_controlPlayerId"] == self.myId and
                    e1['_gameloop'] != 0)

	def filter_SUnitsDoneEvent(self, e1):
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitDoneEvent' and
                    e1['_gameloop'] != 0)

	def gameloopToMinutes(self, gameloop):
		parteDecimale = round(gameloop / gameLoopsInOneSecond % 60 * 0.01, 2)
		minutiGiustiGiusti = int(
			gameloop / gameLoopsInOneSecond) // 60 + parteDecimale
		return minutiGiustiGiusti

	def map_add_time_to_events(self, e):
		e['time'] = self.gameloopToMinutes(e['_gameloop'])
		return e

	

