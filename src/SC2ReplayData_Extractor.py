import mpyq
import os
from s2protocol import versions
import json

gameLoopsInOneSecond = 22.4


class SC2ReplayData_Extractor:

	def __init__(self, replayFilePath, player_to_analyze_name):

		self.replayHeader, self.protocol = self.build_replay(replayFilePath)
		game_events = self.protocol.decode_replay_game_events(self.game_events)
		tracker_events = self.protocol.decode_replay_tracker_events(self.contents)

		player_info = self.protocol.decode_replay_details(self.details)
		# detailed_info = self.protocol.decode_replay_initdata(self.init_data)
		self.myId = self.get_my_id(player_to_analyze_name, player_info)

		self.game_events = list(map(
			self.map_add_time_to_events, game_events))

		self.tracker_events = list(map(
			self.map_add_time_to_events, tracker_events))

	def build_replay(self, path):
		self.archive = mpyq.MPQArchive(path)
		replay = self.archive.header['user_data_header']['content']
		header = versions.latest().decode_replay_header(replay)

		self.contents = self.archive.read_file('replay.tracker.events')
		self.details = self.archive.read_file('replay.details')
		self.game_events = self.archive.read_file('replay.game.events')
		self.init_data = self.archive.read_file('replay.initDaa')

		self.metadata = json.loads(
			self.archive.read_file('replay.gamemetadata.json'))
		base_build = header['m_version']['m_baseBuild']
		try:
			return (replay, versions.build(base_build))
		except Exception as e:
			raise Exception('Unsupported base build: {0} ({1!s})'.format(base_build, e))

	# TODO

	def get_my_id(self, myName, player_info):
		player_1_name, player_2_name = self.get_player_names(player_info)

		if myName in player_1_name:
			return 1
		elif myName in player_2_name:
			return 2
		else:
			raise Exception("Player Not Found")

	def get_player_names(self, player_info):
		player_names = []
		for player in player_info['m_playerList']:
			player_names.append(player['m_name'])

		return (str(player_names[0]), str(player_names[1]))

	def map_unitTag_tuple(self, e1):
		return (e1['m_unitTagIndex'], e1['m_unitTagRecycle'])

	# def filter_by_tagIndex(self, e1, tagIndex):
	# RELP
	def get_my_command_centers_tags(self):
		myCommandCentersInit = self.get_command_centers_created()
		myCommandCenterTags = list(map(self.map_unitTag_tuple, myCommandCentersInit))

		return myCommandCenterTags

	def filter_by_tags(self, tags, eventsList):
		rslt = [event for event in eventsList
                    if((event['m_unitTagIndex'] == tags[0] and event['m_unitTagRecycle'] == tags[1])
                        or (event['m_creatorUnitTagIndex'] == tags[0] and event['m_creatorUnitTagRecycle'] == tags[1])
                       )]
		return rslt



	def filter_by_tags_new(self, tags, eventsList):
		rslt = [event for event in eventsList
				if("("+str(event['m_unitTagIndex'])+", "+str(event['m_unitTagRecycle'])+")" in tags)]
		return rslt

	def filter_by_creatorTags(self, creatorTags, eventsList):
		rslt = [event for event in eventsList
				if(event['m_creatorUnitTagIndex'] == creatorTags[0] and event['m_creatorUnitTagRecycle'] == creatorTags[1])]
		return rslt

	def get_command_centers_production_queue(self):
		myCommandCenterTags = self.get_my_command_centers_tags()

		rslt = {}
		scv_born_events = self.get_my_SCVs_born_events()
		for tag in myCommandCenterTags:
			curr_CC_ProductionQueue = self.filter_by_creatorTags(
				tag, scv_born_events)

			rslt[str(tag)] = curr_CC_ProductionQueue

		return rslt

	def get_command_centers_finish(self):
		myCommandCenterTags = self.get_my_command_centers_tags()

		rslt = self.filter_by_tags(
			myCommandCenterTags, self.get_my_units_done_events())

		return list(rslt)

	def get_my_units_done_events(self):
		rslt = filter(self.filter_SUnitsDoneEvent, self.get_replay_tracker_events())
		return list(rslt)

	def get_my_SCVs_born_events(self):
		rslt = filter(self.filter_SCVBornEvent, self.get_replay_tracker_events())
		return list(rslt)

	def get_orbitals_created(self):
		tmp = filter(self.filter_SUnitChangeType_MyOrbitals, self.get_replay_tracker_events())

		rslt = []
		for event in tmp:
			event['m_creatorUnitTagIndex'] = event['m_unitTagIndex']
			event['m_creatorUnitTagRecycle'] = event['m_unitTagRecycle']
			rslt.append(event)

		return list(rslt)

	def get_command_centers_created(self):
		rslt = filter(self.filter_MyCC_UnitInit, self.get_replay_tracker_events())

		return list(rslt)

	def get_replay_tracker_events(self):
		return self.tracker_events

	def get_replay_game_events(self):
		return self.game_events

	def filter_MyCC_UnitInit(self, e1):
		return ((e1["_event"] == 'NNet.Replay.Tracker.SUnitInitEvent'
				 or e1["_event"] == 'NNet.Replay.Tracker.SUnitBornEvent')
				and
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

	def gameloopToSeconds(self, gameloop):
		seconds = gameloop / gameLoopsInOneSecond
		seconds = int(seconds)
		return seconds

	def map_add_time_to_events(self, e):
		e['time'] = self.gameloopToMinutes(e['_gameloop'])
		return e
