import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

CONFIG_FILE = "config.txt"

def load_language():
    if not os.path.exists(CONFIG_FILE):
        lang = messagebox.askquestion("Language / Язык", "Use English?\nИспользовать английский язык?")
        with open(CONFIG_FILE, "w") as f:
            f.write("En" if lang == "yes" else "Ru")
    with open(CONFIG_FILE) as f:
        return f.read().strip()

def save_language(code):
    with open(CONFIG_FILE, "w") as f:
        f.write(code)

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

LANG = load_language()

def t(rus, eng):
    return rus if LANG == "Ru" else eng

# Конверсии
def ft_to_m(ft): return float(ft) * 0.3048
def m_to_ft(m): return float(m) / 0.3048
def knots_to_kmh(knots): return float(knots) * 1.852
def kmh_to_knots(kmh): return float(kmh) / 1.852
def miles_to_km(miles): return float(miles) * 1.609344
def km_to_miles(km): return float(km) / 1.609344
def hpa_to_inhg(hpa): return float(hpa) * 0.029529983
def inhg_to_hpa(inhg): return float(inhg) / 0.029529983
def c_to_f(c): return (float(c) * 9/5) + 32
def f_to_c(f): return (float(f) - 32) * 5/9

class ConversionApp:
    def __init__(self, root):
        self.root = root
        self.root.title(t("Ту-154Б-2: Конвертер", "Tu-154B-2: Converter"))
        self.updating = False

        self.create_menu()

        self.add_pair(t("Футы:", "Feet:"), t("Метры:", "Meters:"), ft_to_m, m_to_ft, 0)
        self.add_pair(t("Узлы:", "Knots:"), t("Км/ч:", "Km/h:"), knots_to_kmh, kmh_to_knots, 1)
        self.add_pair(t("Мили:", "Miles:"), t("Км:", "Kilometers:"), miles_to_km, km_to_miles, 2)
        self.add_pair(t("гПа:", "hPa:"), t("inHg:", "inHg:"), hpa_to_inhg, inhg_to_hpa, 3, show_decimal=True)
        self.add_pair(t("°C:", "°C:"), t("°F:", "°F:"), c_to_f, f_to_c, 4)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        lang_menu = tk.Menu(menubar, tearoff=0)
        lang_menu.add_command(label="Русский", command=lambda: self.set_language("Ru"))
        lang_menu.add_command(label="English", command=lambda: self.set_language("En"))
        menubar.add_cascade(label=t("Язык", "Language"), menu=lang_menu)
        self.root.config(menu=menubar)

    def set_language(self, code):
        save_language(code)
        messagebox.showinfo(t("Перезапуск", "Restart"),
                            t("Язык будет изменён после перезапуска.", "Language will change after restart."))
        restart_program()

    def add_pair(self, label_left, label_right, to_right, to_left, row, show_decimal=False):
        left_var = tk.StringVar()
        right_var = tk.StringVar()

        ttk.Label(self.root, text=label_left).grid(row=row, column=0, padx=5, pady=5)
        ttk.Entry(self.root, textvariable=left_var).grid(row=row, column=1, padx=5, pady=5)
        ttk.Label(self.root, text=label_right).grid(row=row, column=2, padx=5, pady=5)
        ttk.Entry(self.root, textvariable=right_var).grid(row=row, column=3, padx=5, pady=5)

        def update_right(*_):
            if self.updating: return
            try:
                self.updating = True
                val = float(left_var.get())
                result = to_right(val)
                if show_decimal:
                    right_var.set(f"{result:.2f}")
                else:
                    right_var.set(str(int(result)))
            except:
                right_var.set("")
            finally:
                self.updating = False

        def update_left(*_):
            if self.updating: return
            try:
                self.updating = True
                val = float(right_var.get())
                result = to_left(val)
                left_var.set(str(int(result)))
            except:
                left_var.set("")
            finally:
                self.updating = False

        left_var.trace_add("write", update_right)
        right_var.trace_add("write", update_left)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversionApp(root)
    root.mainloop()
