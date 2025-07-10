# display_weather_on_eink.py

import os
from PIL import Image
import time

# Import the correct Waveshare e-Paper module for your 2.13-inch Black/White display.
# We will try several common modules for 2.13-inch B/W displays until one works.
epd_class = None # Renamed from epd_module to epd_class for clarity (it will hold the EPD class itself)
# --- START: Reordered module_names_to_try to prioritize V3 ---
module_names_to_try = ["epd2in13_V3", "epd2in13_V2", "epd2in13", "epd2in13_V4"] 
# --- END: Reordered module_names_to_try ---

for module_name in module_names_to_try:
    try:
        # Attempt to import the specific module from waveshare_epd package
        # The 'fromlist' argument is crucial for relative imports within the package.
        # This approach assumes 'waveshare_epd' is a top-level package in sys.path.
        imported_module = __import__(f"waveshare_epd.{module_name}", fromlist=[module_name])
        print(f"INFO: Successfully imported {module_name} module.")
        
        # Now, get the EPD class from the imported module
        epd_class = getattr(imported_module, "EPD")
        print(f"INFO: Found EPD class in {module_name}.")
        break # Exit loop if both module and EPD class are found
    except ImportError as e:
        print(f"INFO: Could not import {module_name} (Error: {e}). Trying next...")
    except AttributeError as e:
        print(f"ERROR: {module_name} module imported, but 'EPD' class not found within it (Error: {e}). Trying next...")
        epd_class = None # Reset epd_class if EPD class is missing

if epd_class is None:
    print("Error: Waveshare e-Paper library not found or incorrect module imported.")
    print("None of the common 2.13-inch B/W modules (epd2in13_V3, epd2in13_V2, epd2in13, epd2in13_V4) could be imported,")
    print("or the 'EPD' class was not found within them.")
    print("Please ensure 'waveshare-epd' is correctly installed in your virtual environment's site-packages.")
    exit()

# --- Configuration for your generated image ---
# This should match the OUT_FILENAME and WORK_DIR from your WLConfig_BW or WLConfig_EINK in configs.py
OUTPUT_DIR = "tmp"
OUTPUT_FILENAME = "landscape_wb.bmp" # Using WLConfig_BW's output filename for Black/White

def main():
    image_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

    if not os.path.exists(image_path):
        print(f"Error: Generated image file not found at {image_path}")
        print("Please ensure your weather_landscape script has run successfully and created the image.")
        return

    epd = None # Initialize epd to None for proper cleanup

    try:
        # Initialize the e-ink display
        epd = epd_class() # Instantiate the EPD class
        print("INFO: Initializing e-ink display...")
        # The init() method requires an 'update' argument (e.g., epd.FULL_UPDATE or 0/1)
        # epd.FULL_UPDATE is a constant defined within the epd module itself.
        epd.init() 
        epd.Clear() # Clear the display before drawing

        # --- START: Print actual display dimensions ---
        print(f"INFO: EPD display native dimensions: {epd.width}x{epd.height}.")
        # --- END: Print actual display dimensions ---

        # Load the generated image
        print(f"INFO: Loading image from {image_path}")
        img = Image.open(image_path)

        # --- START: Added image rotation for portrait display ---
        # Rotate the image 90 degrees clockwise to match the portrait orientation of the display.
        # 'expand=True' ensures the canvas expands to fit the new dimensions after rotation.
        print(f"INFO: Original image size: {img.size}. Rotating 90 degrees clockwise.")
        img = img.rotate(90, expand=True)
        print(f"INFO: Image size after rotation: {img.size}.")
        # --- END: Added image rotation ---

        # --- START: Added image cropping to match display size precisely ---
        # Image is now 128x296 after rotation.
        # Display is 122x250.
        # We need to remove 6 pixels from width (128-122) and 46 pixels from height (296-250).
        # To remove from top and right:
        # For width: crop from 0 to 122 (removes 6 from right)
        # For height: To keep the bottom content and remove from the top,
        # we need to calculate the upper bound.
        # New upper bound = rotated_image_height - target_display_height
        # 296 - 250 = 46. This is what we had.
        # If this is cutting off the bottom, it means we need to shift the window down.
        # Let's try to remove fewer pixels from the top, e.g., 30 instead of 46.
        # This means the new upper bound is 30, and the lower bound is 30 + 250 = 280.
        crop_box = (0, 46, 128, 296) # (left, upper, right, lower)
        print(f"INFO: Cropping image from {img.size} using box {crop_box}.")
        # img = img.crop(crop_box)
        print(f"INFO: Image size after cropping: {img.size}.")
        # --- END: Added image cropping ---

        # --- Prepare image for Black/White display ---
        # Ensure the image is in '1' mode (1-bit pixels, black and white)
        # The WLConfig_BW (or WLConfig_EINK) should already output a BMP in a suitable format.
        # If not, Pillow's convert('1') can quantize it.
        if img.mode != '1':
            print(f"WARNING: Image mode is {img.mode}, converting to '1' (1-bit black/white).")
            img = img.convert('1')

        # After cropping, the image dimensions should now precisely match the display's.
        if img.width != epd.width or img.height != epd.height:
            # This warning should ideally not appear if cropping is correct.
            print(f"WARNING: Image size ({img.width}x{img.height}) still does not match display size ({epd.width}x{epd.height}). Resizing as fallback.")
            img = img.resize((epd.width, epd.height), Image.LANCZOS)
        else:
            print(f"INFO: Image size ({img.width}x{img.height}) matches display size ({epd.width}x{epd.height}). No resizing needed.")


        # Send the 1-bit image to the display
        print("INFO: Sending image data to e-ink display...")
        epd.display(epd.getbuffer(img)) # For B/W displays, typically one buffer is sent

        print("INFO: Image sent to display. Waiting for refresh...")
        time.sleep(5) # Give the display time to refresh (adjust as needed)

        # Put display to sleep to save power
        epd.sleep()
        print("INFO: Display put to sleep.")

    except IOError as e:
        print(f"Error: I/O error with display or image: {e}")
        if epd: epd.exit() # Ensure cleanup on error
    except KeyboardInterrupt:
        print("\nExiting and clearing display.")
        if epd: epd.exit() # Clean up GPIO
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if epd: epd.exit() # Ensure cleanup on error

if __name__ == "__main__":
    main()
