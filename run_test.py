import os


from weather_landscape import WeatherLandscape
# --- START: Modified import statement ---
from configs import * # Changed from p_weather.configs to directly import configs
# --- END: Modified import statement ---


# --- START: Modified configurations list ---
# We are focusing on WLConfig_BW as it's configured for the correct B/W dimensions
# and its output filename (landscape_wb.bmp) is used by display.py.
cfgs = [
    WLConfig_BW(),
    # WLConfig_BWI(), # Commented out other configs
    # WLConfig_EINK(), # Commented out other configs
    # WLConfig_RGB_Black(), # Commented out other configs
    # WLConfig_RGB_White(), # Commented out other configs
]
# --- END: Modified configurations list ---

for cfg in cfgs:
    print("Using configuration %s" % cfg.TITLE)
    w = WeatherLandscape(cfg)
    fn = w.SaveImage()
    print("Saved",fn)
