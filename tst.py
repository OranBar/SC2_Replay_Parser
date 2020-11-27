from SC2ReplayData_Extractor import SC2ReplayData_Extractor
import mpyq
import os
import functools
from s2protocol import versions
from zephyrus_sc2_parser import parse_replay
import os


replay = archive.read_file('replay.tracker.events')
rslt = protocol.decode_replay_tracker_events(replay)

print(rslt)
