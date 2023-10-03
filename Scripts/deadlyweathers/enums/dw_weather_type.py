"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from weather.weather_enums import WeatherType


class DWWeatherType(WeatherType):
    DWAcid = 5000
    DeadlyWeather = 5001


with WeatherType.make_mutable():
    # noinspection PyProtectedMember
    WeatherType._add_new_enum_value(DWWeatherType.DWAcid.name, DWWeatherType.DWAcid)
    # noinspection PyProtectedMember
    WeatherType._add_new_enum_value(DWWeatherType.DeadlyWeather.name, DWWeatherType.DeadlyWeather)
