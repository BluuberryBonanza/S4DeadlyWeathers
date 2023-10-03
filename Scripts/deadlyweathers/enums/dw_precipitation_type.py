"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""

from weather.weather_enums import PrecipitationType


class DWPrecipitationType(PrecipitationType):
    ROCKS = 5000


with PrecipitationType.make_mutable():
    # noinspection PyProtectedMember
    PrecipitationType._add_new_enum_value(DWPrecipitationType.ROCKS.name, DWPrecipitationType.ROCKS)

