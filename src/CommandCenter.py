SCV_BUILD_TIME = 12
ORBITAL_BUILD_TIME = 25
PLANETARY_BUILD_TIME = 36

class CommandCenter:

	def __init__(self, data_extractor):
		self.data_extractor = data_extractor

	def get_command_centers_timeline(self):
		orbitals_finish_events = self.data_extractor.get_orbitals_created()
		data = self.data_extractor.get_command_centers_production_queue()

		ccTag_to_timeline = {}
		for cc_tag, cc_prod in data.items():
			tmp = self.data_extractor.filter_by_tags(
				cc_tag, orbitals_finish_events)
			cc_orbital_time = int(tmp[0]['_gameloop']
                         ) if tmp != [] else -1

			print("cc orbital time: " + str(cc_orbital_time))
			cc_timeline = []
			ccTag_to_timeline[cc_tag] = cc_timeline

			for i in range(len(cc_prod) - 2):
				scv_curr_finish = self.data_extractor.gameloopToSeconds(cc_prod[i])
				scv_next = self.data_extractor.gameloopToSeconds(cc_prod[i + 1])

				idleTimeBetweenScvs = scv_next['_gameloop'] - \
					scv_curr_finish['_gameloop'] - SCV_BUILD_TIME*22.4

				idleTimeBetweenScvs = self.data_extractor.gameloopToSeconds(idleTimeBetweenScvs)
				# scv_curr_finish = self.data_extractor.gameloopToSeconds(scv_curr_finish)

				scv_curr_start = scv_curr_finish - 12

				#if orbitale tra scv_curr e scv_next
				orbital_was_made_between_scvs = (
					scv_curr_finish['_gameloop'] < cc_orbital_time
					and scv_next['_gameloop'] > cc_orbital_time)

				if (orbital_was_made_between_scvs):
					idleTimeBetweenScvs = idleTimeBetweenScvs - ORBITAL_BUILD_TIME * 22.4
					orbital_start = scv_curr_finish
					orbital_finish = scv_next

				if (idleTimeBetweenScvs >= 1):
					idle_time_start = scv_curr_start - idleTimeBetweenScvs

				idleTimeBetweenScvs = self.data_extractor.gameloopToSeconds(idleTimeBetweenScvs)

				cc_timeline.append(idleTimeBetweenScvs)

		return ccTag_to_timeline

	def get_command_center_idle_time(self):
		orbitals_finish_events = self.data_extractor.get_orbitals_created()
		data = self.data_extractor.get_command_centers_production_queue()

		idleSCVtimeline = {}
		for cc_tag, cc_prod in data.items():
			cc_orbital_time = self.data_extractor.filter_by_tags(
				cc_tag, orbitals_finish_events)
			cc_orbital_time = int(cc_orbital_time[0]['_gameloop']
                         ) if cc_orbital_time != [] else -1

			print("cc orbital time: " + str(cc_orbital_time))
			scv_time_deltas = []
			idleSCVtimeline[cc_tag] = scv_time_deltas

			for i in range(len(cc_prod) - 2):
				scv_curr = cc_prod[i]
				scv_next = cc_prod[i + 1]
				idleTimeBetweenScvs = scv_next['_gameloop'] - \
					scv_curr['_gameloop'] - SCV_BUILD_TIME*22.4

				# if orbitale tra scv_curr e scv_next
				orbital_was_made_between_scvs = (
					scv_curr['_gameloop'] < cc_orbital_time
					and scv_next['_gameloop'] > cc_orbital_time)

				if (orbital_was_made_between_scvs):
					idleTimeBetweenScvs = idleTimeBetweenScvs - ORBITAL_BUILD_TIME * 22.4

				idleTimeBetweenScvs = self.data_extractor.gameloopToSeconds(
					idleTimeBetweenScvs)
				if (idleTimeBetweenScvs <= 0.1):
					idleTimeBetweenScvs = 0

				scv_time_deltas.append(idleTimeBetweenScvs)

		return idleSCVtimeline

	
