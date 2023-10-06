"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from buffs.buff import Buff
from deadlyweathers.bb_lib.utils.bb_buff_utils import BBBuffUtils
from event_testing.resolver import SingleSimResolver
from event_testing.results import TestResult
from sims.sim_info import SimInfo


class BBSimBuffUtils:
    """Utilities for managing Buffs on Sims."""
    @classmethod
    def add_buff(cls, sim_info: SimInfo, buff: Union[int, Buff], reason: int) -> TestResult:
        """add_buff(sim_info, buff, reason)

        Add a Buff to a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param buff: The Buff to add.
        :type buff: int or Buff
        :param reason: The reason the Buff is added. (This will appear under the Buff header when hovering over it in-game.)
        :type reason: int
        :return: The result of adding or failing to add the buff. True, if successful. False, if not.
        :rtype: TestResult
        """
        if sim_info is None:
            raise AssertionError('Cannot add a buff to a None Sim.')
        buff_instance = BBBuffUtils.load_buff_by_guid(buff)
        if buff_instance is None:
            return TestResult(False, f'No buff existed with GUID {buff}.')
        can_add_result = cls.can_add_buff(sim_info, buff)
        if not can_add_result:
            return can_add_result
        from sims4.localization import _create_localized_string
        reason_string = _create_localized_string(reason)
        added = sim_info.add_buff_from_op(buff_instance, buff_reason=reason_string)
        if added is None:
            return TestResult(False, f'Failed to add buff {buff_instance} to Sim {sim_info}.')
        return TestResult(True, f'Successfully added buff {buff_instance} to Sim {sim_info}.')

    @classmethod
    def can_add_buff(cls, sim_info: SimInfo, buff: Union[int, Buff]) -> TestResult:
        """can_add_buff(sim_info, buff)

        Determine if a Buff can be added to the Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param buff: The Buff to check.
        :type buff: int or Buff
        :return: True, if the Buff can be added to the Sim. False, if not.
        :rtype: TestResult
        """
        if sim_info is None:
            raise AssertionError('Cannot add a buff to a None Sim.')
        buff_instance = BBBuffUtils.load_buff_by_guid(buff)
        if buff_instance is None:
            return TestResult(False, f'Cannot add buff to Sim {sim_info}. No buff existed with GUID {buff}.')
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return TestResult(False, f'Cannot add buff {buff_instance} to Sim {sim_info} because they are not currently spawned.')
        # noinspection PyUnresolvedReferences
        buff_add_test_set = buff_instance._add_test_set
        if buff_add_test_set is not None:
            resolver = SingleSimResolver(sim)
            result: TestResult = buff_add_test_set.run_tests(resolver)
            if not result:
                return TestResult(False, f'Cannot add buff {buff_instance}. The tests on it failed for Sim {sim_info} because reason "{result.reason}".')
        # noinspection PyUnresolvedReferences
        mood = buff_instance.mood_type
        if mood is not None and mood.excluding_traits is not None and sim_info.trait_tracker.has_any_trait(mood.excluding_traits):
            return TestResult(False, f'Cannot add buff {buff_instance}. The Mood {mood} on the buff is not allowed for the Sim {sim_info}. Mood Excluding Traits: {mood.excluding_traits}')
        if buff_instance.exclusive_index is None:
            return TestResult(True, f'Can add buff {buff_instance} to Sim {sim_info} it has no conflicts.')
        for conflicting_buff_type in sim_info.buff_component._active_buffs:
            if conflicting_buff_type is buff_instance:
                continue

            if conflicting_buff_type.exclusive_index == buff_instance.exclusive_index:
                if buff_instance.exclusive_weight < conflicting_buff_type.exclusive_weight:
                    return TestResult(False, f'Cannot add buff {buff_instance} because it conflicts with buff {conflicting_buff_type} on Sim {sim_info}.')
        return TestResult(True, f'Can add buff {buff_instance} to Sim {sim_info}.')

    @classmethod
    def remove_buff(cls, sim_info: SimInfo, buff: int) -> TestResult:
        """remove_buff(sim_info, buff)

        Remove a buff from a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param buff: The Buff to remove.
        :type buff: int
        :return: True, if the Buff was successfully removed. False, if not.
        :rtype: TestResult
        """
        if sim_info is None:
            raise AssertionError('Cannot remove a buff from a None Sim.')
        buff_instance = BBBuffUtils.load_buff_by_guid(buff)
        if buff_instance is None:
            return TestResult(False, f'Cannot remove buff from Sim {sim_info}. No buff existed with GUID {buff}.')
        sim_info.remove_buff_by_type(buff_instance)
        return TestResult(True, f'Successfully removed Buff {buff_instance} from Sim {sim_info}.')
