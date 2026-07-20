import time
import ctypes
import threading
from pynput.mouse import Button, Controller, Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode

ON_KEY = KeyCode(char="=")
OFF_KEY = KeyCode(char="-")

mouse = Controller()
clicking = False
exit_program = False
click_event = threading.Event()
winmm = ctypes.windll.winmm

SELECTED_BUTTON = Button.left

# иммитация клика
def clicker():
    while not exit_program:
        if clicking:
            #start_time = time.perf_counter()
            mouse.press(SELECTED_BUTTON)
            mouse.release(SELECTED_BUTTON)
            # while time.perf_counter() - start_time < CLICK_DELAY:
            #     pass
            click_event.wait(timeout=CLICK_DELAY)
        else:
            time.sleep(0.1)

# обработка нажаития клавиш
def on_press_keyboard(key):
    global clicking, exit_program

    if key == Key.home:
        print("Программа завершена.")
        clicking = False
        exit_program = True
        return False
    
    elif key == ON_KEY:
        if not clicking:
            clicking = True
            print(f"Автокликер: Включен ({'ЛКМ' if SELECTED_BUTTON == Button.left else 'ПКМ'})")
        else:
            clicking = False
            print("Автокликер: Выключен(Пауза)")

    elif key == OFF_KEY:
        clicking = False
        print("Автокликер: Остановлен. Возврат к настройкам...")
        return False

# выбор кнопки мыши
def on_click_setup(_, __, button, pressed):
    global SELECTED_BUTTON

    if pressed:
        if button == Button.left:
            SELECTED_BUTTON = Button.left
            print("Выбрана левая кнопка мыши(ЛКМ)")
            return False
        elif button == Button.right:
            SELECTED_BUTTON = Button.right
            print("Выбрана правая кнопка мыши (ПКМ)")
            return False

# устанавливаем минимальный квант времени Windows(1мс)
winmm.timeBeginPeriods(1)
# поток кликов
click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

while not exit_program:
    try:
        print("===========================")
        print("===Настройки Автокликера===")
        print("===========================")
        user_input = input("Введите задержку в секундах или exit для выхода: ")

        if user_input.lower() == "exit":
            exit_program = True
            break

        CLICK_DELAY = float(user_input)
    except ValueError:
        print("Ошибка, введите число. Установлена задержка по умолчанию: 0.1 сек.")
        CLICK_DELAY = 0.1       

    print("Нажмите кнопку мыши(прям на экране) для выбора")

    with MouseListener(on_click=on_click_setup) as mouse_listener:
        mouse_listener.join() # слушатель мыши

    print("\nГотово к работе")
    print("= - Включить кликер")
    print("- - Остановить кликер и изменить задержку")
    print("home - Полный выход из программы\n")

    with KeyboardListener(on_press=on_press_keyboard) as keyboard_listener:
        keyboard_listener.join() # слушатель клавиатуры

# Возвращаем стандартный квант времени Windows(15мс)
winmm.timeEndPeriod(1)
print("Программа успешно закрыта.")
