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
		zero_event['_gameloop'] = '0'
		zero_event['time'] = '0'
		zero_event['_event'] = 'Zero Event'

		global_timeline = heapq.merge(orbitals_finish_events, scv_finish_events, key=lambda x: x['_gameloop'])
		global_timeline = sorted(global_timeline, key=lambda x:  x['_gameloop'])

		self.data_extractor.get_my_command_centers_tags()
		for cc_tag in self.data_extractor.get_my_command_centers_tags():
			cc_timeline = self.data_extractor.filter_by_tags(cc_tag, global_timeline)
			cc_timeline.insert(0, zero_event)

			rslt.append(cc_timeline)

		return rslt
