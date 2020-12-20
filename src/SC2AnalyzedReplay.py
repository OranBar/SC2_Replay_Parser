import heapq

# Only takes into account timings of completed scv.
# It includes orbital transformation time, time floating
# Does not take into account scv cancels (usure if it makes any difference tho)
SCV_BUILD_TIME = 12
ORBITAL_BUILD_TIME = 25
PLANETARY_BUILD_TIME = 36


class SC2AnalyzedReplay:

	def __init__(self, data_extractor):
		self.data_extractor = data_extractor

	def get_command_center_timelines(self):
		rslt = []
		global_timeline = []

		scv_finish_events = self.data_extractor.get_my_SCVs_born_events()
		orbitals_finish_events = self.data_extractor.get_orbitals_created()

		zero_event = {}
		zero_event['_gameloop'] = 0
		zero_event['time'] = '0'
		zero_event['_event'] = 'Zero Event'

		global_timeline = heapq.merge(orbitals_finish_events, scv_finish_events, key=lambda x: x['_gameloop'])
		# global_timeline = sorted(global_timeline, key=lambda x:  x['_gameloop'])

		for cc_tag in self.data_extractor.get_my_command_centers_tags():
			cc_timeline = self.data_extractor.filter_by_tags(cc_tag, global_timeline)
			cc_timeline.insert(0, zero_event)

			# Now we gotta insert the "Start/Begin" events, since starcraft only registers "End/Finish" events
			begin_events_to_add = []
			for event in cc_timeline:
				if(event['_event'] == 'NNet.Replay.Tracker.SUnitBornEvent'):
					if(event['m_unitTypeName'] == b'SCV'):
						scv_born_event = self.create_scv_born_event(event['_gameloop'], event['m_unitTypeName'])
						begin_events_to_add.append(scv_born_event)

				elif(event['_event'] == 'NNet.Replay.Tracker.SUnitTypeChangeEvent'):
					if(event['m_unitTypeName'] == b'OrbitalCommand'):
						orbital_end_event = self.create_orbital_event(event['_gameloop'], event['m_unitTypeName'])
						begin_events_to_add.append(orbital_end_event)
			
					# if(event['m_unitTypeName'] == b'PlanetaryFortress'):
					# 	orbital_begin_event = self.create_orbital_event()
					# 	begin_events_to_add.append(orbital_begin_event)
			
			tmp = heapq.merge(begin_events_to_add, cc_timeline, key=lambda x: x['_gameloop'])
			cc_timeline = sorted(tmp, key=lambda x:  x['_gameloop'])
			rslt.append(cc_timeline)

		return rslt

	def create_scv_born_event(self, scv_complete_gameloop, unit_type):
		unit_born_event = {}
		unit_born_event['_event'] = 'SC2.Python.Analyzer.UnitBeginEvent'

		unit_born_event['_gameloop'] = scv_complete_gameloop - SCV_BUILD_TIME * 22.4
		unit_born_event['time'] = self.data_extractor.gameloopToSeconds(unit_born_event['_gameloop'])
		unit_born_event['type'] = unit_type
		return unit_born_event

	def create_orbital_event(self, orbital_complete_gameloop, unit_type):
		orbital_start_event = {}
		orbital_start_event['_event'] = 'SC2.Python.Analyzer.UpgradeBeginEvent'

		orbital_start_event['_gameloop'] = orbital_complete_gameloop - ORBITAL_BUILD_TIME * 22.4
		orbital_start_event['time'] = self.data_extractor.gameloopToSeconds(orbital_start_event['_gameloop'])
		orbital_start_event['type'] = unit_type
		return orbital_start_event
