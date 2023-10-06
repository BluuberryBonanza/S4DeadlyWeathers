"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import TYPE_CHECKING, Union

import services
from sims4.resources import Types

if TYPE_CHECKING:
    from weather.weather_service import WeatherService
    from weather.weather_event import WeatherEvent


class BBWeatherUtils:
    @classmethod
    def trigger_weather_event(cls, weather_event: int, duration: int):
        """trigger_weather_event(weather_event, duration)

        Trigger a weather event to occur. This will change the currently active weather.

        :param weather_event: The weather event to trigger.
        :type weather_event: int
        :param duration: The duration in Sim hours the weather should last.
        :type duration: int
        """
        weather_service = cls.get_weather_service()
        if weather_service is None:
            return
        weather_event = cls.load_weather_event_by_guid(weather_event)
        if weather_event is None:
            return
        weather_service.start_weather_event(weather_event, duration)

    @classmethod
    def load_weather_event_by_guid(cls, weather_event: int) -> Union['WeatherEvent', None]:
        """load_weather_event_by_guid(weather_event)

        Load a Weather Event by its GUID

        :param weather_event: The GUID of the Weather Event to load.
        :type weather_event: int
        :return: The loaded Weather Event or None if not found.
        :rtype: WeatherEvent or None
        """
        from weather.weather_event import WeatherEvent
        if isinstance(weather_event, WeatherEvent):
            return weather_event
        instance_manager = services.get_instance_manager(Types.WEATHER_EVENT)
        return instance_manager.get(weather_event)

    @classmethod
    def get_weather_service(cls) -> Union['WeatherService', None]:
        """get_weather_service()

        Get the service that handles weather functions.

        :return: The weather service or None if not available.
        :rtype: WeatherService or None
        """
        import services
        if not hasattr(services, 'weather_service'):
            return None
        return services.weather_service()
