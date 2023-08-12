import pyperclip
import time
import keyboard
from LanguageMapping import en_to_th, th_to_en, ambiguous_map
from CapslockMapping import en_uncapslocked, en_capslocked, th_uncapslocked, th_capslocked, ambiguous_capslock_map

HAS_NUMPAD = True
numpad_keys = set('0123456789/*-+.=')

# =================== LANGUAGE =================== #

def determine_language(s, prev_char, next_char):
    th_count = 0
    en_count = 0
    for c in s:
        if c in en_to_th:
            en_count += 1
        elif c in th_to_en:
            th_count += 1

    if prev_char == " " or prev_char in ambiguous_map:
        if next_char in en_to_th:
            return "en"
        elif next_char in th_to_en:
            return "th"

    if next_char == " " or next_char in ambiguous_map:
        if prev_char in en_to_th:
            return "en"
        elif prev_char in th_to_en:
            return "th"

    return "th" if th_count > en_count else "en"

def is_numpad(input_string, index):
    start_index = index
    while start_index >= 0 and input_string[start_index] in numpad_keys:
        start_index -= 1
    end_index = index
    while end_index < len(input_string) and input_string[end_index] in numpad_keys:
        end_index += 1
    startb = input_string[start_index] if start_index >= 0 else " "
    endb = input_string[end_index] if end_index < len(input_string) else " "
    return startb == " " and endb == " "


def correct_language(input_string):
    output_string = ""
    i = 0
    while i < len(input_string):
        char = input_string[i]
        if char in numpad_keys and is_numpad(input_string, i):
            while i < len(input_string) and input_string[i] in numpad_keys:
                output_string += input_string[i]
                i += 1
            continue

        prev_char = input_string[i-1] if i > 0 else " "
        next_char = input_string[i+1] if i < len(input_string)-1 else " "
        if char in ambiguous_map:
            lang = determine_language(char, prev_char, next_char)
            output_string += en_to_th.get(char, char) if lang == "en" else th_to_en.get(char, char)
        else:
            output_string += en_to_th.get(char, th_to_en.get(char, char))
        i += 1
    return output_string


# =================== CAPS LOCK =================== #
def is_english(char):
    return char in en_uncapslocked or char in en_capslocked

def is_thai(char):
    return char in th_uncapslocked or char in th_capslocked

def determine_context(input_string, index):
    extended_window_size = 10
    thai_count = 0
    english_count = 0
    for i in range(max(0, index - extended_window_size), min(len(input_string), index + extended_window_size + 1)):
        if is_thai(input_string[i]):
            thai_count += 1
        elif is_english(input_string[i]):
            english_count += 1
    if thai_count > english_count:
        return "thai"
    elif english_count > thai_count:
        return "english"
    elif is_thai(input_string[index]):
        return "thai"
    elif is_english(input_string[index]):
        return "english"
    else:
        return "unknown"

def correct_capslock(input_string):
    corrected_string = ""
    i = 0
    while i < len(input_string):
        char = input_string[i]
        if char in numpad_keys and is_numpad(input_string, i):
            while i < len(input_string) and input_string[i] in numpad_keys:
                corrected_string += input_string[i]
                i += 1
            continue

        context = determine_context(input_string, i)
        if char in ambiguous_capslock_map:
            if context == "english":
                corrected_string += en_capslocked.get(char, char)
            elif context == "thai":
                corrected_string += th_capslocked.get(char, char)
            else:
                corrected_string += char
        elif context == "english":
            corrected_string += en_capslocked.get(char, en_uncapslocked.get(char, char))
        elif context == "thai":
            corrected_string += th_capslocked.get(char, th_uncapslocked.get(char, char))
        else:
            corrected_string += char
        i += 1
    return corrected_string

# =================== MAIN FUNCTION =================== #

LANGUAGE_SWITCH_KEY1 = 'win'
LANGUAGE_SWITCH_KEY2 = 'space'
AUTO_SWITCH_LANGUAGE = True
AUTO_SWITCH_CAPSLOCK = True


def main():
    print("Program started... Press Ctrl + C or Ctrl + Z to stop.")
    print("")

    try:
        while True:
            if keyboard.is_pressed('shift+alt+d'):     
                print("# =========== SWITCH_LANGUAGE =========== #")

                time.sleep(0.2)
                original_clipboard_content = pyperclip.paste()
                time.sleep(0.8)
                keyboard.press('ctrl')
                keyboard.press('c')
                keyboard.release('c')
                keyboard.release('ctrl')
                print("Captured original text.")
                copied_text = pyperclip.paste()
                print(f"Input: {copied_text}")

                corrected_text = correct_language(copied_text)
                print(f"Output: {corrected_text}")
                pyperclip.copy(corrected_text)
                print("Corrected text copied to clipboard.")
                time.sleep(0.8)
                keyboard.press('ctrl')
                keyboard.press('v')
                keyboard.release('v')
                keyboard.release('ctrl')
                print("Replaced with corrected text.")
                time.sleep(0.2)
                pyperclip.copy(original_clipboard_content)
                print("Restored original clipboard content.")
                if AUTO_SWITCH_LANGUAGE: 
                    if LANGUAGE_SWITCH_KEY2 != '':  
                        keyboard.press(LANGUAGE_SWITCH_KEY1)
                        keyboard.press(LANGUAGE_SWITCH_KEY2)
                        keyboard.release(LANGUAGE_SWITCH_KEY1)
                        keyboard.release(LANGUAGE_SWITCH_KEY2)
                    else:  
                        keyboard.press(LANGUAGE_SWITCH_KEY1)
                        keyboard.release(LANGUAGE_SWITCH_KEY1)
                
                print("# ======================================= #")
                print("")

                

            elif keyboard.is_pressed('shift+alt+c'):
                print("# =========== SWITCH_CAPSLOCK =========== #")

                time.sleep(0.2)
                original_clipboard_content = pyperclip.paste()
                time.sleep(0.8)
                keyboard.press('ctrl')
                keyboard.press('c')
                keyboard.release('c')
                keyboard.release('ctrl')
                print("Captured original text.")
                copied_text = pyperclip.paste()
                print(f"Input: {copied_text}")
                corrected_text = correct_capslock(copied_text)
                print(f"Output: {corrected_text}")
                pyperclip.copy(corrected_text)
                print("Corrected text copied to clipboard.")
                time.sleep(0.8)
                keyboard.press('ctrl')
                keyboard.press('v')
                keyboard.release('v')
                keyboard.release('ctrl')
                print("Replaced with corrected text.")
                time.sleep(0.2)
                pyperclip.copy(original_clipboard_content)
                print("Restored original clipboard content.")
                if AUTO_SWITCH_CAPSLOCK:
                    keyboard.press('caps lock')
                    keyboard.release('caps lock')

                print("# ======================================= #")
                print("")

    except KeyboardInterrupt:
        print("Program has been stopped.")

if __name__ == '__main__':
    main()
