import easyocr
import pyautogui
import time
from mouse import get_position

def move_text_on_screen(text, delay=1):
    def find_text_coordinates(image_path, text):
        # Create an EasyOCR reader
        reader = easyocr.Reader(['en'])

        # Perform OCR on the image
        results = reader.readtext(image_path)

        # Loop through the OCR results and find the coordinates of the specified text
        for (bbox, word, confidence) in results:
            if word.lower() == text.lower():
                # bbox contains the coordinates of the bounding box
                (top_left, top_right, bottom_right, bottom_left) = bbox
                return (top_left, top_right, bottom_right, bottom_left)
        return None

    # Capture the screen and save it to a file
    screenshot = pyautogui.screenshot()
    screenshot_path = 'screenshot.png'
    screenshot.save(screenshot_path)

    # Get the screen resolution
    screen_width, screen_height = pyautogui.size()

    # Find the coordinates of the specified text on the screenshot
    coordinates = find_text_coordinates(screenshot_path, text)

    if coordinates:
        # Calculate the center of the bounding box
        (top_left, top_right, bottom_right, bottom_left) = coordinates
        center_x = int((top_left[0] + bottom_right[0]) / 2)
        center_y = int((top_left[1] + bottom_right[1]) / 2)

        # Debugging: Print bounding box coordinates
        print(f"Bounding box: {top_left}, {top_right}, {bottom_right}, {bottom_left}")
        print(f"Initial center coordinates: {center_x}, {center_y}")

        # Adjust for scaling (assumes no scaling if not specified)
        scaling_factor_x = pyautogui.size()[0] / screenshot.width
        scaling_factor_y = pyautogui.size()[1] / screenshot.height
        center_x = int(center_x * scaling_factor_x)
        center_y = int(center_y * scaling_factor_y)

        # Debugging: Print adjusted center coordinates
        print(f"Adjusted center coordinates: {center_x}, {center_y}")

        # Check if the coordinates are within the screen bounds
        if 0 <= center_x <= screen_width and 0 <= center_y <= screen_height:
            # Move the mouse to the center of the bounding box and click
            pyautogui.moveTo(center_x, center_y, duration=delay)
            # pyautogui.click()

            print(f"'{text}' found at coordinates: {center_x}, {center_y}")
            print("Current mouse position:", get_position())
        else:
            print(f"'{text}' found at coordinates: {center_x}, {center_y}, but it is outside the screen bounds")
    else:
        print(f"'{text}' not found on the screen")