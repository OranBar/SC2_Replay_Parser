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

	def get_command_centers_timelines(self):
		rslt = []
		global_timeline = []

		scv_finish_events = self.data_extractor.get_my_SCVs_born_events()
		orbitals_finish_events = self.data_extractor.get_orbitals_created()

		zero_event = {}
		zero_event['_gameloop'] = 0
		zero_event['time'] = '0'
		zero_event['_event'] = 'Zero Event'

		global_timeline = heapq.merge(orbitals_finish_events, scv_finish_events, key=lambda x: x['_gameloop'])
		global_timeline = sorted(global_timeline, key=lambda x:  x['_gameloop'])

		cc_index = 0

		for cc_tag in self.data_extractor.get_my_command_centers_tags():
			cc_index = cc_index + 1 
			cc_name = "CC " + str(cc_index)

			cc_timeline = self.data_extractor.filter_by_tags(cc_tag, global_timeline)
			cc_timeline.insert(0, zero_event)
			# cc_timeline = sorted(cc_timeline, key=lambda x:  x['_gameloop'])

			# Now we gotta insert the "Start/Begin" events, since starcraft only registers "End/Finish" events
			events = []
			for event in cc_timeline:
				if(event['_event'] == 'NNet.Replay.Tracker.SUnitBornEvent'):
					if(event['m_unitTypeName'] == b'SCV'):
						scv_created_event = self.create_scv_created_event(event['_gameloop'], event['m_unitTypeName'], cc_name)
						events.append(scv_created_event)

				elif(event['_event'] == 'NNet.Replay.Tracker.SUnitTypeChangeEvent'):
					if(event['m_unitTypeName'] == b'OrbitalCommand'):
						orbital_created_event = self.create_orbital_event(event['_gameloop'], event['m_unitTypeName'], cc_name)
						events.append(orbital_created_event)
			
					# if(event['m_unitTypeName'] == b'PlanetaryFortress'):
					# 	orbital_begin_event = self.create_orbital_event()
					# 	begin_events_to_add.append(orbital_begin_event)
			
			rslt.append(events)

		return rslt

	def create_scv_created_event(self, scv_complete_gameloop, unit_type, cc_name):
		unit_created_event = {}
		unit_created_event['event'] = str(unit_type, 'utf-8') + ' Created'

		scv_start_gameloop = scv_complete_gameloop - SCV_BUILD_TIME * 22.4
		unit_created_event["start_time"] = self.data_extractor.gameloopToSeconds(scv_start_gameloop)
		unit_created_event['end_time'] = self.data_extractor.gameloopToSeconds(scv_complete_gameloop)
		# unit_created_event['type'] = unit_type
		unit_created_event['building_name'] = cc_name

		return unit_created_event

	def create_orbital_event(self, orbital_complete_gameloop, unit_type, cc_name):
		orbital_complete_event = {}
		orbital_complete_event['event'] = str(unit_type, 'utf-8') + ' Researched'

		orbital_start_gameloop = orbital_complete_gameloop - ORBITAL_BUILD_TIME * 22.4
		orbital_complete_event["start_time"] = self.data_extractor.gameloopToSeconds(orbital_start_gameloop)
		orbital_complete_event['end_time'] = self.data_extractor.gameloopToSeconds(orbital_complete_gameloop)
		# orbital_complete_event['type'] = unit_type
		orbital_complete_event['building_name'] = cc_name
		return orbital_complete_event
