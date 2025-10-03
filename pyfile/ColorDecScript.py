import pyautogui
import numpy as np
from mss import mss
import time


TARGET_COLOR = np.array([121, 121, 122])
COLOR_TOLERANCE = 30


def color_distance(color1, color2):

    return np.sqrt(np.sum((color1 - color2) ** 2))


def scan_screen_for_color(target_color, tolerance):

    with mss() as sct:

        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)


        img_array = np.array(screenshot)


        rgb_array = img_array[:, :, [2, 1, 0]]


        height, width, _ = rgb_array.shape

        for y in range(0, height, 5):
            for x in range(0, width, 5):
                pixel_color = rgb_array[y, x]


                distance = color_distance(pixel_color, target_color)

                if distance <= tolerance:
                    return True, (x, y), pixel_color

        return False, None, None


def main():
    print("Color Detection Auto-Clicker Started")
    print(f"Target Color: #{TARGET_COLOR[0]:02x}{TARGET_COLOR[1]:02x}{TARGET_COLOR[2]:02x}")
    print(f"Tolerance: {COLOR_TOLERANCE}")
    print("Scanning every 5 minutes, performing 15 clicks if color detected")
    print("Press Ctrl+C to stop\n")

    last_scan_time = 0
    scan_interval = 300
    clicks_per_detection = 15

    try:
        while True:
            current_time = time.time()


            if current_time - last_scan_time >= scan_interval:
                print(f"[{time.strftime('%H:%M:%S')}] Scanning screen for color...")
                color_found, position, detected_color = scan_screen_for_color(TARGET_COLOR, COLOR_TOLERANCE)

                if color_found:
                    print(f"✓ Color detected at position {position}")
                    print(f"  Detected color: RGB{tuple(detected_color)}")
                    print(f"  Performing {clicks_per_detection} clicks...")


                    for i in range(clicks_per_detection):
                        pyautogui.click()
                        print(f"  Click {i + 1}/{clicks_per_detection}")
                        time.sleep(3)

                    print("✓ Clicking complete!")
                else:
                    print(f"✗ Color not found on screen")

                last_scan_time = current_time


            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nAuto-clicker stopped by user")


if __name__ == "__main__":

    pyautogui.FAILSAFE = True
    main()