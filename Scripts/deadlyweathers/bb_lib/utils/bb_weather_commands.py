from deadlyweathers.bb_lib.utils.bb_weather_utils import BBWeatherUtils
from sims4.commands import CommandType, Command


@Command(
    'bbl.trigger_weather',
    command_type=CommandType.Live
)
def _bbl_command_trigger_weather_event(weather_event: int, duration: int = 1, _connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output(f'Triggering weather {weather_event} for {duration} Sim hours')
    BBWeatherUtils.trigger_weather_event(weather_event, duration)

