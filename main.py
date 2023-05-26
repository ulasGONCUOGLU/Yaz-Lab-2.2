import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time

# Ana tkinter penceresi
root = tk.Tk()
root.title("Sıralama Uygulaması")
root.geometry("800x400")

# Sol panel
left_frame = ttk.Frame(root)
left_frame.pack(side="left", padx=10)

# Sağ panel
right_frame = ttk.Frame(root)
right_frame.pack(side="right", padx=10)

# Sol panel bileşenleri

# Dizi Boyutu
size_label = ttk.Label(left_frame, text="Dizi Boyutu:")
size_label.grid(column=0, row=0, sticky="W")

def update_size_label(dizi_boyutu):
    size_label.config(text="Dizi Boyutu: " + str(int(float(dizi_boyutu))))

size_slider = ttk.Scale(left_frame, from_=0, to=100, orient="horizontal", command=update_size_label)
size_slider.grid(column=1, row=0, sticky="W")

current_value_label = ttk.Label(left_frame, text="Mevcut Değer: 0")
current_value_label.grid(column=2, row=0, sticky="W")

def update_current_value(value):
    current_value_label.config(text="Mevcut Değer: " + str(int(float(value))))

size_slider.config(command=update_current_value)

# Sıralama Türü
sorting_label = ttk.Label(left_frame, text="Sıralama Türü:")
sorting_label.grid(column=0, row=2, sticky="W")

sorting_combo = ttk.Combobox(left_frame, values=["Selection Sort", "Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort"])
sorting_combo.grid(column=1, row=2, sticky="W")
sorting_combo.current(0)

# Grafik Türü
chart_type_label = ttk.Label(left_frame, text="Grafik Türü:")
chart_type_label.grid(column=0, row=3, sticky="W")

chart_type_combo = ttk.Combobox(left_frame, values=["Dağılım (Scatter)", "Sütun (Bar)", "Kök (Stem)"])
chart_type_combo.grid(column=1, row=3, sticky="W")
chart_type_combo.current(0)

# Grafik Hızı
chart_speed_label = ttk.Label(left_frame, text="Grafik Hızı:")
chart_speed_label.grid(column=0, row=4, sticky="W")

def update_chart_speed_label(hiz):
    chart_speed_label.config(text="Hız ayarı: " + str(int(float(hiz))))

speed_slider = ttk.Scale(left_frame, from_=1, to=60, orient="horizontal", command=update_chart_speed_label)
speed_slider.grid(column=1, row=4, sticky="W")

current_speed_label = ttk.Label(left_frame, text="Mevcut Değer: 1")
current_speed_label.grid(column=2, row=4, sticky="W")

def update_current_speed(value):
    current_speed_label.config(text="Mevcut Değer: " + str(int(float(value))))

speed_slider.config(command=update_current_speed)

# Matplotlib figürü 
fig = plt.figure(figsize=(6, 6))
chart_canvas = FigureCanvasTkAgg(fig, master=right_frame)
chart_canvas.get_tk_widget().pack()

# Sağ panel fonksiyonları

def draw_chart(data):
    chart_type = chart_type_combo.get()
    plt.clf()
    if chart_type == "Dağılım (Scatter)":
        plt.scatter(range(len(data)), data, color="b", marker="o")
    elif chart_type == "Sütun (Bar)":
        plt.bar(range(len(data)), data, color="b")
    elif chart_type == "Kök (Stem)":
        plt.stem(range(len(data)), data, use_line_collection=True)
    chart_canvas.draw()

def swap(data, i, j):
    data[i], data[j] = data[j], data[i]
    draw_chart(data)
    time.sleep(1 / int(speed_slider.get()))
    root.update()

# Sıralama algoritması - Bubble Sort
def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                swap(data, j, j + 1)
                if sorting_paused:
                    return

# Sıralama algoritması - Insertion Sort
def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
        draw_chart(data)
        time.sleep(1 / int(speed_slider.get()))
        root.update()
        if sorting_paused:
            return

# Sıralama algoritması - Selection Sort
def selection_sort(data):
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
        swap(data, i, min_idx)
        if sorting_paused:
            return

# Sıralama algoritması - Merge Sort
def merge_sort(data):
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                data[k] = left_half[i]
                i += 1
            else:
                data[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            data[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            data[k] = right_half[j]
            j += 1
            k += 1
        draw_chart(data)
        time.sleep(1 / int(speed_slider.get()))
        root.update()
        if sorting_paused:
            return

# Sıralama algoritması - Quick Sort
def quick_sort(data, low, high):
    if low < high:
        pi = partition(data, low, high)
        quick_sort(data, low, pi - 1)
        quick_sort(data, pi + 1, high)
        if sorting_paused:
            return

def partition(data, low, high):
    i = low - 1
    pivot = data[high]
    for j in range(low, high):
        if data[j] <= pivot:
            i = i + 1
            swap(data, i, j)
    swap(data, i + 1, high)
    return i + 1

# Sıralama işlemini başlat
def create_sort():
    dizi_boyutu = int(size_slider.get())
    data = random.sample(range(1, dizi_boyutu + 1), dizi_boyutu)
    draw_chart(data)
    
def start_sort():
    dizi_boyutu = int(size_slider.get())
    sira = sorting_combo.get()
    data = random.sample(range(1, dizi_boyutu + 1), dizi_boyutu)
    draw_chart(data)
    
    global sorting_paused
    sorting_paused = False
    if sira == "Selection Sort":
        selection_sort(data)
    elif sira == "Bubble Sort":
        bubble_sort(data)
    elif sira == "Insertion Sort":
        insertion_sort(data)
    elif sira == "Merge Sort":
        merge_sort(data)
    elif sira == "Quick Sort":
        quick_sort(data, 0, len(data) - 1)

# Sıralama işlemini duraklat
def pause_sort():
    global sorting_paused
    sorting_paused = True

    
# Sıralama işlemini sıfırla
def reset_sort():
    size_slider.set(0)
    sorting_combo.current(0)
    chart_type_combo.current(0)
    speed_slider.set(1)
    update_size_label(0)
    update_current_speed(1)
    draw_chart([])

# Sıralama butonları

reset_button = ttk.Button(left_frame, text="Oluştur", command=create_sort)
reset_button.grid(column=0, row=5, pady=10, sticky="W")

start_button = ttk.Button(left_frame, text="Başlat", command=start_sort)
start_button.grid(column=1, row=5, pady=10, sticky="W")

pause_button = ttk.Button(left_frame, text="Duraklat", command=pause_sort)
pause_button.grid(column=2, row=5, pady=10, sticky="W")

reset_button = ttk.Button(left_frame, text="Sıfırla", command=reset_sort)
reset_button.grid(column=3, row=5, pady=10, sticky="W")

root.mainloop()
