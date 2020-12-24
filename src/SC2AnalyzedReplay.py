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

		global_timeline = heapq.merge(orbitals_finish_events, scv_finish_events, key=lambda x: x['_gameloop'])
		global_timeline = sorted(global_timeline, key=lambda x:  x['_gameloop'])

		cc_index = 0

		for cc_tag in self.data_extractor.get_my_command_centers_tags():
			cc_index = cc_index + 1
			cc_name = "CC " + str(cc_index)
			events_without_idle = []

			cc_timeline = self.data_extractor.filter_by_tags(cc_tag, global_timeline)
			if(len(cc_timeline) == 0):
				continue
			# cc_timeline = sorted(cc_timeline, key=lambda x:  x['_gameloop'])
			# Now we gotta insert the "Start/Begin" events, since starcraft only registers "End/Finish" events
			events_without_idle = self.timeline_to_graph_events(cc_timeline, cc_name)
			events = self.add_idle_events(events_without_idle, cc_name)

			rslt.append(events)

		return rslt

	def timeline_to_graph_events(self, cc_timeline, cc_name):
		rslt = []
		for event in cc_timeline:
			new_event = None
			if(event['_event'] == 'NNet.Replay.Tracker.SUnitBornEvent'):
				if(event['m_unitTypeName'] == b'SCV'):
					new_event = self.create_scv_created_event(event['_gameloop'], event['m_unitTypeName'], cc_name)
					rslt.append(new_event)

			elif(event['_event'] == 'NNet.Replay.Tracker.SUnitTypeChangeEvent'):
				if(event['m_unitTypeName'] == b'OrbitalCommand'):
					new_event = self.create_orbital_event(event['_gameloop'], event['m_unitTypeName'], cc_name)
					rslt.append(new_event)

				elif(event['m_unitTypeName'] == b'PlanetaryFortress'):
					new_event = self.create_planetary_event(event['_gameloop'], event['m_unitTypeName'], cc_name)
					rslt.append(new_event)

		return rslt

	def add_idle_events(self, events, cc_name):
		prev_event = events[0]
		idle_events = []
		for i in range(1,len(events)-1):
			curr_event = events[i]
			if(curr_event['start_time'] - prev_event['end_time'] > 1):
				event = self.create_idle_event(prev_event['end_time'], curr_event['start_time'], cc_name)
				idle_events.append(event)
			
			prev_event = curr_event
			
		return events + idle_events

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

	def create_planetary_event(self, orbital_complete_gameloop, unit_type, cc_name):
		event = {}
		event['event'] = str(unit_type, 'utf-8') + ' Researched'

		start_gameloop = orbital_complete_gameloop - PLANETARY_BUILD_TIME * 22.4
		event["start_time"] = self.data_extractor.gameloopToSeconds(start_gameloop)
		event['end_time'] = self.data_extractor.gameloopToSeconds(orbital_complete_gameloop)
		# event['type'] = unit_type
		event['building_name'] = cc_name
		return event

	def create_idle_event(self, start, end, cc_name):
		idle_event = {}
		idle_event['event'] = 'Idle'
		idle_event['start_time'] = start
		idle_event['end_time'] = end
		idle_event['building_name'] = cc_name
		
		return idle_event
