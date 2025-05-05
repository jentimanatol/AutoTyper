import pyautogui
import time

def auto_type(text, delay=0.5):
    print("Typing will start in 5 seconds... Move your cursor to a text field.")
    time.sleep(5)  # Give time to focus a text field
    for char in text:
        pyautogui.write(char)
        time.sleep(delay)

# Example usage
if __name__ == "__main__":
   # sample_text = "This is an automated typing example."

    with open('text_data.txt', 'r', encoding='utf-8') as f:
        sample_text = f.read()



    auto_type(sample_text, delay=0.5)


