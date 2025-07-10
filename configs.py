# configs.py

from p_weather.configuration import WLBaseSettings

class WLConfig_BW(WLBaseSettings):
    TITLE = "BW"
    WORK_DIR = "tmp"
    OUT_FILENAME = "landscape_wb"
    OUT_FILEEXT = ".bmp"
    TEMPLATE_FILENAME = "p_weather/template_wb.bmp"
    SPRITES_DIR="p_weather/sprite"
    POSTPROCESS_INVERT = False
    POSTPROCESS_EINKFLIP = False   

    # --- START: Updated dimensions to match display after rotation ---
    # The display is 122x250 (portrait).
    # We want the generated image to be 250x122 (landscape) so that
    # when rotated by 90 degrees, it becomes 122x250, matching the display.
    HEIGHT = 122 # The height of the landscape image
    WIDTH = 250  # The width of the landscape image
    # --- END: Updated dimensions ---

    # --- START: Adjusted DRAWOFFSET to shift content upwards ---
    # This value controls the vertical position of the ground line and elements.
    # Increasing it shifts content upwards, preventing cutoff at the bottom of the 122-pixel height.
    DRAWOFFSET = 50 # Adjusted to a higher value to shift content upwards.
    # --- END: Adjusted DRAWOFFSET ---
    
class WLConfig_EINK(WLConfig_BW):
    TITLE = "BW EINK"
    OUT_FILENAME = "landscape_eink"
    POSTPROCESS_INVERT = False   
    POSTPROCESS_EINKFLIP = True   
    
    
    
class WLConfig_BWI(WLConfig_BW):
    TITLE = "BW inverted"
    OUT_FILENAME = "landscape_wbi"
    POSTPROCESS_INVERT = True
    POSTPROCESS_EINKFLIP = False


    
class WLConfig_RGB_White(WLBaseSettings):   
    TITLE = "Color, white BG"
    WORK_DIR = "tmp"    
    OUT_FILENAME = "landscape_rgb_w"
    OUT_FILEEXT = ".png"    
    SPRITES_DIR="p_weather/sprite_rgb" # Assumes you have RGB versions of sprites here
    TEMPLATE_FILENAME = "p_weather/template_rgb.bmp"

    POSTPROCESS_INVERT = False
    POSTPROCESS_EINKFLIP = False
    SPRITES_MODE = WLBaseSettings.SPRITES_MODE_RGB


    COLOR_SOIL = (148, 82, 1)
    COLOR_SMOKE = (127,127,127) 
    COLOR_BG = (255,255,255)
    COLOR_FG = (0,0,0)   
    COLOR_RAIN = (10, 100, 148)
    COLOR_SNOW = (194, 194, 194)
    
    
class WLConfig_RGB_Black(WLConfig_RGB_White):   
    TITLE = "Color, black BG"
    OUT_FILENAME = "landscape_rgb_b"

    COLOR_SOIL = (148, 82, 1)
    COLOR_SMOKE = (127,127,127) 
    COLOR_BG = (0,0,0)
    COLOR_FG =      (255,255,255)
    COLOR_RAIN = (122, 213, 255)
    COLOR_SNOW = (255,255,255)   

# --- NEW CONFIGURATION FOR BLACK, WHITE, RED E-INK DISPLAY ---
# (Keeping this here for reference, even if not currently used for B/W display)
class WLConfig_BWR(WLConfig_RGB_White):
    TITLE = "Black, White, Red E-Ink"
    OUT_FILENAME = "landscape_bwr" # New output filename
    OUT_FILEEXT = ".png" # PNG is good for intermediate, then convert to display format

    # We still use RGB sprites and drawing, then convert to 3-color palette
    SPRITES_DIR = "p_weather/sprite_rgb" 
    SPRITES_MODE = WLBaseSettings.SPRITES_MODE_RGB

    # Set colors to map effectively to Black, White, or Red
    COLOR_SOIL = (100, 50, 0)       
    COLOR_SMOKE = (150, 150, 150)   
    COLOR_BG = (255, 255, 255)      
    COLOR_FG = (0, 0, 0)            
    COLOR_RAIN = (0, 0, 255)        
    COLOR_SNOW = (255, 255, 255)    

    POSTPROCESS_3COLOR = True
    POSTPROCESS_INVERT = False
    POSTPROCESS_EINKFLIP = False
