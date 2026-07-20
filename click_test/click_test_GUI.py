import time
import threading
from tkinter import *
from pygame.mixer import init, Sound

click_count = 0
test_started = False
start_time = 0
pressed = False
ready_for_test = False

init()
click_sound = Sound("click_sound.mp3")
clean_sound = Sound("clean_sound.mp3")

root = Tk()
root.title("Счётчик CPS")
root.geometry("700x600")
root.minsize(500, 400)
root.config(bg="black")

BG_MAIN = "#121212"       # Глубокий «угольный» фон для всего окна
BG_FRAME = "#1A1A1A"      # Графитовый фон для рабочего фрейма
MATRIX_GREEN = "#00FF66"  # Сочный неоновый зелёный (цвет активности)
DARK_GREEN = "#1A3322"    # Темно-зелёный для фона кнопок
ALERT_RED = "#FF3333"     # Сдержанный красный для кнопки сброса

main_frame = Frame(root, 
                   width=450, 
                   height=350, 
                   bg="#1A1A1A",
                   relief="groove",
                   borderwidth=3,
                   highlightbackground="black")
main_frame.pack(expand=True)
main_frame.pack_propagate(False)

count = 0

def on_click():
    global click_count, test_started, start_time, ready_for_test, pressed
    while True:
        if pressed:
            pressed = False
            if not test_started:
                test_started = True
                start_time = time.perf_counter()
                print("Тест запущен, считаем клики за секунду...")
            
            click_count += 1

        if test_started:
            if time.perf_counter() - start_time >= 1.0:
                result.config(text=f"Сокрость: {click_count} CPS")
                print("РЕЗУЛЬТАТ ТЕСТА: ")
                print(f"Сокрость: {click_count} CPS")
                button_click.config(state="disabled")

                click_count = 0
                test_started = False

        if test_started:
            time.sleep(0.001)
        else:
            time.sleep(0.1)

def clicker():
    global count, ready_for_test, pressed
    count += 1
    click.config(text=count)
    click_sound.play()
    pressed = True
    ready_for_test = True

def clean():
    global count, text_of_clicks
    count = 0
    click.config(text=count)
    text_of_clicks = "Ожидание кликов..."
    result.config(text=text_of_clicks)
    button_click.config(state="normal")
    click_sound.play()

click = Label(main_frame, 
              text="0",
              font="Arial 30",
              relief="ridge",
              borderwidth=3,
              highlightbackground="black",
              bg=BG_FRAME,
              fg=MATRIX_GREEN
              )
click.pack(pady="10")

button_click = Button(main_frame, 
             text="Кликай!", 
             padx="20",
             pady="20",
             font="Arial 20",
             fg=MATRIX_GREEN,
             bg=DARK_GREEN,
             activebackground=MATRIX_GREEN,
             activeforeground=BG_FRAME,
             command=clicker)
button_click.pack(pady="10")

result = Label(main_frame,
               text="Ожидание кликов...",
               font="Arial 20",
               relief="solid",
               borderwidth=3,
               highlightbackground="#2A2A2A",
               bg="#151515",
               fg=MATRIX_GREEN
               )
result.pack(pady="10")

button_clean = Button(main_frame, 
             text="Очистить", 
             padx="20",
             pady="10",
             font="Arial 16",
             bg=ALERT_RED,
             fg="white",
             command=clean
             )
button_clean.pack(pady="10")

click_thread = threading.Thread(target=on_click, daemon=True)
click_thread.start()

root.mainloop()