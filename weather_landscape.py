import os
from PIL import Image

from p_weather.openweathermap import OpenWeatherMap
from p_weather.draw_weather import DrawWeather
from p_weather.configuration import WLBaseSettings

import secrets


class WeatherLandscape:


    def __init__(self,configuration:WLBaseSettings):
        self.cfg = WLBaseSettings.Fill( configuration, secrets )    
        assert self.cfg.OWM_KEY != "000000000000000000",  "Set OWM_KEY variable to your OpenWeather API key in secrets.py"


    def MakeImage(self)->Image:

        owm = OpenWeatherMap(self.cfg)
        owm.FromAuto()

        # --- START: Modified image creation ---
        # Instead of opening a fixed-size template image, create a new image
        # with the dimensions specified in the configuration (self.cfg.WIDTH, self.cfg.HEIGHT).
        # '1' mode is for 1-bit pixels (black and white), and color=255 sets it to white.
        img = Image.new('1', (self.cfg.WIDTH, self.cfg.HEIGHT), color=255)
        # --- END: Modified image creation ---

        art = DrawWeather(img,self.cfg)
        img = art.Draw(owm)

        return img


    def SaveImage(self)->str:
        img = self.MakeImage() 
        outfilepath = self.cfg.ImageFilePath()
        img.save(outfilepath) 
        return outfilepath
