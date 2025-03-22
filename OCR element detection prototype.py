import easyocr
import pyautogui
import time

def click_text_on_screen(text, delay=1):
    def find_text_coordinates(image, text):
        # Create an EasyOCR reader
        reader = easyocr.Reader(['en'])

        # Perform OCR on the image
        results = reader.readtext(image)

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

    # Find the coordinates of the string 'Next' on the screenshot
    coordinates = find_text_coordinates(screenshot_path, text)

    if coordinates:
        # Calculate the center of the bounding box
        (top_left, top_right, bottom_right, bottom_left) = coordinates
        center_x = int((top_left[0] + bottom_right[0]) / 2)
        center_y = int((top_left[1] + bottom_right[1]) / 2)

        # Move the mouse to the center of the bounding box and click
        pyautogui.moveTo(center_x, center_y, duration=delay)
        pyautogui.click()

        print(f"'{text}' button clicked at coordinates: {center_x}, {center_y}")
    else:
        print(f"'{text}' not found on the screen")

# Example usage
time.sleep(5)
click_text_on_screen('Next')

