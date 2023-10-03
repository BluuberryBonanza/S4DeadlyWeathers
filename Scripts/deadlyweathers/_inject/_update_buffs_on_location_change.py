from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from deadlyweathers.enums.dw_weather_type import DWWeatherType
from deadlyweathers.mod_identity import DWModIdentity
from deadlyweathers.utils.bb_weather_utils import BBWeatherUtils
from event_testing.resolver import SingleSimResolver, SingleObjectResolver
from weather.weather_aware_component import WeatherAwareComponent

log = BBLogRegistry().register_log(DWModIdentity(), 'dw_location_change_log')


class DWLocationChangeHandler:
    @classmethod
    def handle_location_change(cls, weather_aware_component: WeatherAwareComponent, is_inside_override: bool = False, disabling: bool = False, **__):
        weather_aware_component_owner = weather_aware_component.owner
        if disabling:
            is_outside = None
        elif is_inside_override:
            is_outside = False
        elif weather_aware_component_owner.is_in_inventory():
            is_outside = None
        elif not weather_aware_component._inside_sensitive:
            is_outside = True
        else:
            is_outside = weather_aware_component_owner.is_outside
        if is_outside == weather_aware_component._is_outside:
            # If the object/Sim is still either outside or inside, we do nothing.
            return
        was_outside = weather_aware_component._is_outside

        weather_service = BBWeatherUtils.get_weather_service()
        if weather_service is not None:
            weather_types = weather_service.get_current_weather_types()
            weather_service.update_weather_aware_message(weather_aware_component_owner)
        else:
            weather_types = {DWWeatherType.UNDEFINED}

        is_sim = weather_aware_component_owner.is_sim
        if is_sim:
            resolver = SingleSimResolver(weather_aware_component_owner.sim_info)
        else:
            resolver = SingleObjectResolver(weather_aware_component_owner)

        current_weather_event = weather_service._current_event

        if DWWeatherType.AnySnow in weather_types:
            # Add drain energy buff.
            if is_outside:
                # Add buff
                pass
            else:
                # Remove buff
                pass

        # Drain energy if

        # If the weather has Rain, we want to apply a Deadly Weathers buff that drains energy.
        # If the weather has Snow, we want to apply a Deadly Weathers buff that drains energy and hunger.
        # If the weather has Lightning, we want to drain Energy faster. (Additional buff)
        # If the weather has Wind, we want to drain Energy faster. (Additional buff)
        # If the weather is Freezing, drain Energy faster

        if was_outside is not None:
            if was_outside:
                # If Sim was outside, but is now inside. Remove buffs related to being outside.
                if is_outside:
                    pass
                # If Sim was outside, but is still outside. Do nothing
                else:
                    pass

        if is_outside is not None:
            if is_outside:
                pass

        # if was_outside is not None:
        #     if was_outside:
        #         # If Sim WAS outside, that means they no longer are, so we give loots related to going inside.
        #         weather_aware_component._give_loot(weather_types, weather_aware_component.outside_loot, resolver, False)
        #         if weather_service is not None:
        #             weather_service.deregister_object(weather_aware_component_owner, weather_aware_component.outside_loot.keys())
        #     else:
        #         # If Sim was not outside, that means we want to give loots related to going inside.
        #         weather_aware_component._give_loot(weather_types, weather_aware_component.inside_loot, resolver, False)
        #         if weather_service is not None:
        #             weather_service.deregister_object(weather_aware_component_owner, weather_aware_component.inside_loot.keys())
        #
        # if is_outside is not None:
        #     if is_outside:
        #         weather_aware_component._give_loot(weather_types, weather_aware_component.outside_loot, resolver, True)
        #         if weather_service is not None:
        #             weather_service.register_object(weather_aware_component_owner, weather_aware_component.outside_loot.keys())
        #             weather_service.register_object(weather_aware_component_owner, weather_aware_component.anywhere_loot.keys())
        #     else:
        #         weather_aware_component._give_loot(weather_types, weather_aware_component.inside_loot, resolver, True)
        #         if weather_service is not None:
        #             weather_service.register_object(weather_aware_component_owner, weather_aware_component.inside_loot.keys())
        #             weather_service.register_object(weather_aware_component_owner, weather_aware_component.anywhere_loot.keys())
        #     if was_outside is None:
        #         weather_aware_component._give_loot(weather_types, weather_aware_component.anywhere_loot, resolver, True)
        # else:
        #     weather_aware_component._give_loot(weather_types, weather_aware_component.anywhere_loot, resolver, False)
        #     if weather_service is not None:
        #         weather_service.deregister_object(weather_aware_component_owner, weather_aware_component.anywhere_loot.keys())


@BBInjectionUtils.inject(DWModIdentity(), WeatherAwareComponent, WeatherAwareComponent._update_location.__name__)
def _dw_update_loots_on_location_changed(original, self, is_inside_override: bool = False, disabling: bool = False, **__):
    log.debug(f'Object {self.owner} is changing locations', owner=self.owner, is_inside_override=is_inside_override, disabling=disabling)
    DWLocationChangeHandler.handle_location_change(self, is_inside_override=is_inside_override, disabling=disabling, **__)
    return original(self, is_inside_override=is_inside_override, disabling=disabling, **__)
