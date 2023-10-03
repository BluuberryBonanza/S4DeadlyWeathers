"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from weather.weather_enums import WeatherEffectType


class DWWeatherEffectType(WeatherEffectType):
    ENERGY_DRAIN = 5000


with WeatherEffectType.make_mutable():
    # noinspection PyProtectedMember
    WeatherEffectType._add_new_enum_value(DWWeatherEffectType.ENERGY_DRAIN.name, DWWeatherEffectType.ENERGY_DRAIN)
