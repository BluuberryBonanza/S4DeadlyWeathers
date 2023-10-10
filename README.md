# Deadly Weathers
Weather just got a whole lot more dangerous.

A Sim will now have to be aware of the weather and plan for it accordingly, otherwise they could die from Exhaustion and Hunger!
The worse the weather, the worse time a Sim will have.

Changes:
- Energy and Hunger drain while a Sim is outdoors in various weathers.

Precipitations:
Snow Light - Drains Energy and Hunger
Snow Heavy - Drains Energy and Hunger faster than Light Snow
Snow Storm - Drains Energy and Hunger faster than Heavy Snow

Rain Light - Drains Energy and Hunger
Rain Heavy - Drains Energy and Hunger faster than Light Rain
Rain Storm - Drains Energy and Hunger faster than Heavy Rain

Clouds and Wind:
Cloudy Partial - Drains Energy
Cloudy Full - Drains Energy faster than Partial Clouds
Windy - Drains Energy

Temperatures:
Freezing - Drains Energy and Hunger faster than Cold
Cold - Drains Energy and Hunger faster Than Cool
Cool - Drains Energy and Hunger at a slow rate.
Warm - Drains Energy and Hunger at a slow rate.
Hot - Drains Energy and Hunger faster than Warm
Burning - Drains Energy and Hunger faster than Hot

[b]FAQ:[/b]
Will this conflict with other mods?
- No, this mod will not conflict with other mods.



[b]Numbers:[/b]
psm = Per Sim Minute

Precipitations:
Snow Light - Energy 2.0psm and Hunger 1.0psm
Snow Heavy - Energy 4.0psm and Hunger 2.0psm
Snow Storm - Energy 8.0psm and Hunger 4.0psm

Rain Light - Energy 2.0psm and Hunger 1.0psm
Rain Heavy - Energy 4.0psm and Hunger 2.0psm
Rain Storm - Energy 8.0psm and Hunger 4.0psm

Clouds and Wind:
Cloudy Partial - Energy 0.1psm
Cloudy Full - Energy 0.5psm
Windy - Energy 1.0psm


Temperatures:
Freezing - Energy 3.0psm and Hunger 1.5psm
Cold - Energy 1.5psm and Hunger 0.75psm
Cool - Energy 0.2psm and Hunger 0.1psm
Warm - Energy 0.2psm and Hunger 0.1psm
Hot - Energy 1.5psm and Hunger 0.75psm
Burning - Energy 3.0psm and Hunger 1.5psm



[b]Commands:[/b]

"bbl.trigger_weather WeatherId Duration"
WeatherId - The tuning id for a Weather Event to trigger.
Here are some examples from the base game:
Snow_Storm 182331
Snow_Heavy_Freezing 182374
Snow_Light_Freezing 182376
Sunny_Cool 182378
Sunny_Burning 182381
Rain_Heavy_Warm 182368
Rain_Light_Warm 182365
Rain_Light_Cool 182322

Duration:
The number of Sim Hours to trigger the Weather Event for. (Basically how long you want it to last)
