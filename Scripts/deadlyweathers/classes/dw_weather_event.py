"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from deadlyweathers.classes.dw_prescribed_weather_type import DWTuningPrescribedWeatherType
from deadlyweathers.enums.dw_cloud_type import DWCloudType
from deadlyweathers.enums.dw_precipitation_type import DWPrecipitationType
from deadlyweathers.enums.dw_temperature import DWTemperature
from sims4.tuning.tunable import OptionalTunable, TunableTuple, TunableSimMinute, Tunable100ConvertRange, \
    TunableInterval, TunableEnumEntry, TunableMapping
from weather.weather_event import WeatherEvent


class DWWeatherEvent(WeatherEvent):

    class DWTunableWeatherElementTuple(TunableTuple):

        def __init__(self, default_lower=40, default_upper=60, **kwargs):
            super().__init__(
                start_delay=TunableSimMinute(
                    description='\n                    Delay in sim minutes before change starts.  Used if new weather is more\n                    severe than existing weather.\n                    ',
                    default=1,
                    minimum=0
                ),
                start_rate=Tunable100ConvertRange(
                    description='\n                    Rate at which ramp up occurs.  Used if new weather is more\n                    severe than existing weather.\n                    ',
                    default=3.3,
                    minimum=0
                ),
                end_delay=TunableSimMinute(
                    description='\n                    Delay in sim minutes before element ends.  Used if existing weather is more\n                    severe than new weather.\n                    ',
                    default=1,
                    minimum=0
                ),
                end_rate=Tunable100ConvertRange(
                    description='\n                    Rate at which ramp doown occurs.  Used if existing weather is more\n                    severe than new weather.\n                    ',
                    default=3.3,
                    minimum=0
                ),
                range=TunableInterval(
                    description='\n                    Range.\n                    ',
                    tunable_type=Tunable100ConvertRange,
                    minimum=0,
                    maximum=100,
                    default_lower=default_lower,
                    default_upper=default_upper
                ),
                **kwargs
            )

    INSTANCE_TUNABLES = {
        'precipitation': OptionalTunable(
            description='\n            The amount/type of precipitation for this weather event.\n            ',
            tunable=DWTunableWeatherElementTuple(
                precipitation_type=TunableEnumEntry(
                    description='\n                    The type of precipitation.\n                    ',
                    tunable_type=DWPrecipitationType,
                    default=DWPrecipitationType.RAIN
                )
            )
        ),
        'cloud_states': TunableMapping(
            description='\n            The types of clouds for this weather event.\n            ',
            key_type=TunableEnumEntry(
                description='\n                The type of clouds.\n                ',
                tunable_type=DWCloudType,
                default=DWCloudType.PARTLY_CLOUDY,
                invalid_enums=(DWCloudType.STRANGE, DWCloudType.VERY_STRANGE)
            ),
            value_type=DWTunableWeatherElementTuple(
                default_lower=100,
                default_upper=100
            ),
            minlength=1
        ),
        'wind': OptionalTunable(
            description='\n            The amount of wind for this weather event.\n            ',
            tunable=DWTunableWeatherElementTuple()
        ),
        'temperature': TunableEnumEntry(
            description='\n            The temperature.\n            ',
            tunable_type=DWTemperature,
            default=DWTemperature.WARM
        ),
        'thunder': OptionalTunable(
            description='\n            The amount of thunder for this weather event.\n            ',
            tunable=DWTunableWeatherElementTuple()
        ),
        'lightning': OptionalTunable(
            description='\n            The amount of lightning for this weather event.\n            ',
            tunable=DWTunableWeatherElementTuple()
        ),
        'prescribed_weather_type': OptionalTunable(
            description='\n            The types of prescribed weather this forecast counts as\n            ',
            tunable=DWTuningPrescribedWeatherType()
        )
    }
