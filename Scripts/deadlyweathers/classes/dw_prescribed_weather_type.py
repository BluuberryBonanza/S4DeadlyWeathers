"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from weather.weather_tuning import TuningPrescribedWeatherType


class DWTuningPrescribedWeatherType(TuningPrescribedWeatherType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
