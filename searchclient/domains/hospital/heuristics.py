# coding: utf-8
#
# Copyright 2021 The Technical University of Denmark
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations
import sys
import itertools
from utils import pos_add, pos_sub, APPROX_INFINITY

import domains.hospital.state as h_state
import domains.hospital.goal_description as h_goal_description
import domains.hospital.level as h_level

class HospitalGoalCountHeuristics:

    def __init__(self):
        pass

    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass

    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        count = 0
        for (position, char, is_positive) in goal_description.agent_goals:
            if not state.agent_at(position):
                count += 1
        return count


class HospitalAdvancedHeuristics:

    def __init__(self):
        pass

    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass


    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:

        # Your heuristic goes here...
        count = 0
        for (position, char, is_positive) in goal_description.agent_goals:
            if not state.agent_at(position):
                count += 1

        agentDistances = 0

        for i in range(0, len(goal_description.agent_goals)):
            (x1, y1), _, _ = goal_description.agent_goals[i]
            (x2, y2), _ = state.agent_positions[i]
            distance = abs(x2 - x1) + abs(y2 - y1)
            agentDistances += distance

        return agentDistances + (count*5)
