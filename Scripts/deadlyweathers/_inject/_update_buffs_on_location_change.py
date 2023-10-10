from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from deadlyweathers.bb_lib.utils.bb_sim_buff_utils import BBSimBuffUtils
from deadlyweathers.enums.dw_buff_ids import DWBuffId
from deadlyweathers.enums.dw_string_ids import DWStringId
from deadlyweathers.enums.dw_weather_type import DWWeatherType
from deadlyweathers.mod_identity import DWModIdentity
from deadlyweathers.bb_lib.utils.bb_weather_utils import BBWeatherUtils
from event_testing.resolver import SingleSimResolver
from weather.weather_aware_component import WeatherAwareComponent
from weather.weather_event import WeatherEvent

log = BBLogRegistry().register_log(DWModIdentity(), 'dw_location_change_log')


class DWLocationChangeHandler:
    @classmethod
    def handle_location_change(cls, weather_aware_component: WeatherAwareComponent, is_inside_override: bool = False, disabling: bool = False, **__):
        was_outside = weather_aware_component._is_outside
        weather_aware_component_owner = weather_aware_component.owner
        if not weather_aware_component_owner.is_sim:
            return

        if weather_aware_component_owner.sim_info.is_npc:
            log.debug('Sim is an NPC, we will ignore adding a buff to them.', owner_sim_info=weather_aware_component_owner.sim_info)
            return
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

        owner_sim_info = BBSimUtils.to_sim_info(weather_aware_component_owner)

        if is_outside == was_outside:
            # If the object/Sim is still either outside or inside, we do nothing.
            log.debug('Sim is still in the same outside state, we change nothing.', owner_sim_info=owner_sim_info, is_outside=is_outside, was_outside=was_outside)
            return

        weather_service = BBWeatherUtils.get_weather_service()
        if weather_service is not None:
            weather_types = weather_service.get_current_weather_types()
            weather_service.update_weather_aware_message(weather_aware_component_owner)
        else:
            weather_types = {DWWeatherType.UNDEFINED}

        resolver = SingleSimResolver(weather_aware_component_owner.sim_info)

        current_weather_event: WeatherEvent = weather_service._current_event

        # noinspection PyUnresolvedReferences
        weather_types_to_buffs = {
            DWWeatherType.Rain_Light: DWBuffId.WEATHER_DRAIN_RAIN_LIGHT,
            DWWeatherType.Rain_Heavy: DWBuffId.WEATHER_DRAIN_RAIN_HEAVY,
            DWWeatherType.Rain_Storm: DWBuffId.WEATHER_DRAIN_RAIN_STORM,
            DWWeatherType.Snow_Light: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            DWWeatherType.Snow_Heavy: DWBuffId.WEATHER_DRAIN_SNOW_HEAVY,
            DWWeatherType.Snow_Storm: DWBuffId.WEATHER_DRAIN_SNOW_STORM,
            DWWeatherType.Cloudy_Partial: DWBuffId.WEATHER_DRAIN_CLOUDY_PARTIAL,
            DWWeatherType.Cloudy_Full: DWBuffId.WEATHER_DRAIN_CLOUDY_FULL,
            DWWeatherType.Windy: DWBuffId.WEATHER_DRAIN_WINDY,
            # DWWeatherType.Sun_Shower: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.Sunny: DWBuffId.WEATHER_DRAIN_SUNNY,
            # DWWeatherType.Heatwave: DWBuffId.WEATHER_DRAIN_HEATWAVE,
            DWWeatherType.Thunder: DWBuffId.WEATHER_DRAIN_THUNDER,
            # DWWeatherType.Min_Snow_Accumulation: DWBuffId.WEATHER_DRAIN_SNOW_ACCUMULATION_MIN,
            # DWWeatherType.Med_Snow_Accumulation: DWBuffId.WEATHER_DRAIN_SNOW_ACCUMULATION_MED,
            # DWWeatherType.High_Snow_Accumulation: DWBuffId.WEATHER_DRAIN_SNOW_ACCUMULATION_HIGH,
            # DWWeatherType.Vampire_Safe_CloudLevel: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.Clear_Skies: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.Thundersnow: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.Sunsnow: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.Dry_Lightning: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.Windy_Hot: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.Cloudy_Warm: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.StrangeWeather: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.Sunbathing_Weather: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.Icy: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            # DWWeatherType.Frozen_Water: DWBuffId.WEATHER_DRAIN_SNOW_LIGHT,
            DWWeatherType.Freezing: DWBuffId.WEATHER_DRAIN_TEMPERATURE_FREEZING,
            DWWeatherType.Cold: DWBuffId.WEATHER_DRAIN_TEMPERATURE_COLD,
            DWWeatherType.Cool: DWBuffId.WEATHER_DRAIN_TEMPERATURE_COOL,
            DWWeatherType.Warm: DWBuffId.WEATHER_DRAIN_TEMPERATURE_WARM,
            DWWeatherType.Hot: DWBuffId.WEATHER_DRAIN_TEMPERATURE_HOT,
            DWWeatherType.Burning: DWBuffId.WEATHER_DRAIN_TEMPERATURE_BURNING,
        }

        # If "is_outside" is True, it means the Sim is currently outside.
        if is_outside:
            buffs_to_add = list()
            buffs_to_remove = list()

            for (weather_type, buff_id) in weather_types_to_buffs.items():
                if weather_type in weather_types:
                    buffs_to_add.append(buff_id)
                else:
                    buffs_to_remove.append(buff_id)

            for buff_to_remove in buffs_to_remove:
                log.debug(f'Removing buff {buff_to_remove} from Sim {owner_sim_info}.')
                BBSimBuffUtils.remove_buff(owner_sim_info, buff_to_remove)

            for buff_to_add in buffs_to_add:
                log.debug(f'Adding buff {buff_to_add} to Sim {owner_sim_info}.')
                result = BBSimBuffUtils.add_buff(owner_sim_info, buff_to_add, DWStringId.FROM_DEADLY_WEATHER)
                if not result:
                    log.debug(f'Failed to add buff {buff_to_add} to {owner_sim_info} because reason', result=result)
        # If "was_outside" is True, it means the Sim went inside.
        elif was_outside:
            buffs_to_remove = list(weather_types_to_buffs.values())
            for buff_to_remove in buffs_to_remove:
                # Remove buffs
                BBSimBuffUtils.remove_buff(owner_sim_info, buff_to_remove)

        # "weather_Snow_Heavy_Freezing" s="182374"
        # {<WeatherType.Freezing = -3>,
        # <WeatherType.AnySnow = 11>,
        # <WeatherType.Min_Snow_Accumulation = 77>,
        # <WeatherType.Sunsnow = 83>,
        # <WeatherType.Frozen_Water = 90>}}

        # {<WeatherType.Cold = -2>,
        # <WeatherType.AnyRain = 12>,
        # <WeatherType.Max_Rain_Accumulation = 14>,
        # <WeatherType.Rain_Light = 64>,
        # <WeatherType.Min_Snow_Accumulation = 77>,
        # <WeatherType.Vampire_Safe_CloudLevel = 80>}
        log.debug('Got weather types.', weather_types=weather_types, is_outside=is_outside, was_outside=was_outside, owner_sim_info=str(owner_sim_info), owner=weather_aware_component_owner)
        if DWWeatherType.AnySnow in weather_types:
            # Add drain energy buff.
            if is_outside:
                # Add buff
                pass
            else:
                # Remove buff
                pass
        if DWWeatherType.AnySnow in weather_types:
            # Add drain energy buff.
            if is_outside:
                # Add buff
                pass
            else:
                # Remove buff
                pass

        # Drain energy if
        # Weather has Snow
        # Weather has Lightning
        # Weather has Wind
        # Temperature is Freezing

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
