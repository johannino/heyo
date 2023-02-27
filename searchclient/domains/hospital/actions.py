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

# pos_add and pos_sub are helper methods for performing element-wise addition and subtractions on positions
# Ex: Given two positions A = (1, 2) and B = (3, 4), pos_add(A, B) == (4, 6) and pos_sub(B, A) == (2,2)
from utils import pos_add, pos_sub
from typing import Union, Tuple
import domains.hospital.state as h_state

direction_deltas = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}
direction_deltas_push = {
    ('N', 'N'): ((-1, 0), (-2, 0)),
    ('N', 'E'): ((-1, 0), (-1, 1)),
    ('N', 'W'): ((-1, 0), (-1, -1)),
    ('S', 'S'): ((1, 0), (2, 0)),
    ('S', 'E'): ((1, 0), (1, 1)),
    ('S', 'W'): ((1, 0), (1, -1)),
    ('E', 'N'): ((0, 1), (-1, 1)),
    ('E', 'S'): ((0, 1), (1, 1)),
    ('E', 'E'): ((0, 1), (0, 2)),
    ('W', 'N'): ((0, -1), (-1, -1)),
    ('W', 'S'): ((0, -1), (1, -1)),
    ('W', 'W'): ((0, -1), (0, -2)),
}
direction_deltas_pull = {
    ('N', 'N'): ((-2, 0), (-1, 0)),
    ('N', 'E'): ((-1, 1), (-1, 0)),
    ('N', 'W'): ((-1, -1), (-1, 0)),
    ('S', 'S'): ((2, 0), (1, 0)),
    ('S', 'E'): ((1, 1), (1, 0)),
    ('S', 'W'): ((1, -1), (1, 0)),
    ('E', 'N'): ((-1, 1), (0, 1)),
    ('E', 'S'): ((1, 1), (0, 1)),
    ('E', 'E'): ((0, 2), (0, 1)),
    ('W', 'N'): ((-1, -1), (0, -1)),
    ('W', 'S'): ((1, -1), (0, -1)),
    ('W', 'W'): ((0, -2), (0, -1)),
}


# An action class must implement three types be a valid action:
# 1) is_applicable(self, agent_index, state) which return a boolean describing whether this action is valid for
#    the agent with 'agent_index' to perform in 'state' independently of any other action performed by other agents.
# 2) result(self, agent_index, state) which modifies the 'state' to incorporate the changes caused by the agent
#    performing the action. Since we *always* call both 'is_applicable' and 'conflicts' prior to calling 'result',
#    there is no need to check for correctness.
# 3) conflicts(self, agent_index, state) which returns information regarding potential conflicts with other actions
#    performed concurrently by other agents. More specifically, conflicts can occur with regard to the following
#    two invariants:
#    A) Two objects may not have the same destination.
#       Ex: '0  A1' where agent 0 performs Move(E) and agent 1 performs Push(W,W)
#    B) Two agents may not move the same box concurrently,
#       Ex: '0A1' where agent 0 performs Pull(W,W) and agent 1 performs Pull(E,E)
#    In order to check for these, the conflict method should return two lists:
#       a) destinations which contains all newly occupied cells.
#       b) moved_boxes which contains the current position of boxes moved during the action, i.e. their position
#          prior to being moved by the action.
# Note that 'agent_index' is the index of the agent in the state.agent_positions list which is often but *not always*
# the same as the numerical value of the agent character.


Position = Tuple[int, int] # Only for type hinting

class NoOpAction:

    def __init__(self):
        self.name = "NoOp"

    def is_applicable(self, agent_index: int,  state: h_state.HospitalState) -> bool:
        # Optimization. NoOp can never change the state if we only have a single agent
        return len(state.agent_positions) > 1

    def result(self, agent_index: int, state: h_state.HospitalState):
        pass

    def conflicts(self, agent_index: int, state: h_state.HospitalState) -> tuple[list[Position], list[Position]]:
        current_agent_position, _ = state.agent_positions[agent_index]
        destinations = [current_agent_position]
        boxes_moved = []
        return destinations, boxes_moved

    def __repr__(self) -> str:
        return self.name


class MoveAction:

    def __init__(self, agent_direction):
        self.agent_delta = direction_deltas.get(agent_direction)
        self.name = "Move(%s)" % agent_direction

    def calculate_positions(self, current_agent_position: Position) -> Position:
        return pos_add(current_agent_position, self.agent_delta)

    def is_applicable(self, agent_index: int,  state: h_state.HospitalState) -> bool:
        current_agent_position, _ = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        return state.free_at(new_agent_position)

    def result(self, agent_index: int, state: h_state.HospitalState):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        state.agent_positions[agent_index] = (new_agent_position, agent_char)

    def conflicts(self, agent_index: int, state: h_state.HospitalState) -> tuple[list[Position], list[Position]]:
        current_agent_position, _ = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        # New agent position is a destination because it is unoccupied before the action and occupied after the action.
        destinations = [new_agent_position]
        # Since a Move action never moves a box, we can just return the empty value.
        boxes_moved = []
        return destinations, boxes_moved

    def __repr__(self):
        return self.name

        


AnyAction = Union[NoOpAction, MoveAction,] # Only for type hinting


# An action library for the multi agent pathfinding
DEFAULT_MAPF_ACTION_LIBRARY = [
    NoOpAction(),
    MoveAction("N"),
    MoveAction("S"),
    MoveAction("E"),
    MoveAction("W"),
]


DEFAULT_HOSPITAL_ACTION_LIBRARY = [
    NoOpAction(),
    MoveAction("N"),
    MoveAction("S"),
    MoveAction("E"),
    MoveAction("W"),
    Push("N", "N"),
    Push("N", "E"),
    Push("N", "W"),
    Push("S", "S"),
    Push("S", "E"),
    Push("S", "W"),
    Push("E", "N"),
    Push("E", "S"),
    Push("E", "E"),
    Push("W", "N"),
    Push("W", "S"),
    Push("W", "W"),
    Pull("N", "N"),
    Pull("N", "E"),
    Pull("N", "W"),
    Pull("S", "S"),
    Pull("S", "E"),
    Pull("S", "W"),
    Pull("E", "N"),
    Pull("E", "S"),
    Pull("E", "E"),
    Pull("W", "N"),
    Pull("W", "S"),
    Pull("W", "W")
]



