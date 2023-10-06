"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

import services
from buffs.buff import Buff
from sims4.resources import Types


class BBBuffUtils:
    """Utilities for managing Buffs."""
    @classmethod
    def load_buff_by_guid(cls, buff: int) -> Union[Buff, None]:
        """load_buff_by_guid(buff)

        Load a Buff by its GUID

        :param buff: The GUID of the Buff to load.
        :type buff: int
        :return: The loaded Buff or None if not found.
        :rtype: Buff or None
        """
        if isinstance(buff, Buff) or buff is Buff:
            return buff

        instance_manager = services.get_instance_manager(Types.BUFF)
        return instance_manager.get(buff)
