import pyautogui

import time

def type(text, delay=0.5):
 
    time.sleep(5)

    for char in text:
        pyautogui.write(char)
        time.sleep(delay)

if __name__=='__main__':

    with open ('research.txt',  'r', encoding='utf-8') as f:
	    sample = f.read()

type(sample, delay=0.5)
