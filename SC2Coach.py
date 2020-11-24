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

	def get_by_event_tag(eventTagIndex, eventTagRecycle):
		return

	def get_command_centers_finish(self):
		myCommandCentersInit = self.get_command_centers_created()
		myCommandCenterTags = map(self.map_unitTag_tuple, myCommandCentersInit)
		#TODO: continue




	def get_units_done_events(self):
		replay = self.archive.read_file('replay.tracker.events')

		return filter(self.filter_SUnitsDoneEvent, self.protocol.decode_replay_tracker_events(replay))

	def get_orbitals_created(self):
		replay = self.archive.read_file('replay.tracker.events')

		return filter(self.filter_SUnitChangeType_MyOrbitals, self.protocol.decode_replay_tracker_events(replay))

	def get_command_centers_created(self):
		replay = self.archive.read_file('replay.tracker.events')

		return filter(self.filter_MyCC_UnitInit, self.protocol.decode_replay_tracker_events(replay))

	def get_replay_tracker_events(self):
		replay = self.archive.read_file('replay.tracker.events')

		return self.protocol.decode_replay_tracker_events(replay)

	def filter_MyCC_UnitInit(self, e1):
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitInitEvent' and
                    e1['_gameloop'] != 0 and
                    e1["m_controlPlayerId"] == self.myId and
                    e1['m_unitTypeName'] == b'CommandCenter')

	def filter_SUnitChangeType_MyOrbitals(self, e1):
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitTypeChangeEvent' and
                    e1['_gameloop'] != 0 and
                    e1['m_unitTypeName'] == b'OrbitalCommand')

	def filter_SUnitBornEvent(self, e1):
		return (e1["_event"] == 'NNet.Replay.Tracker.SUnitBornEvent' and
                    e1["m_controlPlayerId"] == self.myId and
                    e1['m_unitTypeName'] == b'SCV' and
                    e1['_gameloop'] != 0)

	def filter_SUnitInitEvent(self, e1):
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
