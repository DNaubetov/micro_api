import requests
import tkinter as tk
from tkinter import scrolledtext, Label, Entry, Button

from utilets.ip import get_local_ip

ip = get_local_ip()
url_soil = f"http://{ip}:8000/api/v2/get/all/pin/soil"
url_pomp = f"http://{ip}:8000/api/v2/get/all/pin/pomp"
url_write = f"http://{ip}:8000/api/v2/write/1/"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32 Data Viewer")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.create_buttons()
        self.load_data()
        self.update_data()

    def create_buttons(self):

        self.label_pin_num = Label(self.root, text="Pin Number:")
        self.label_pin_num.pack(pady=5)
        self.entry_pin_num = Entry(self.root)
        self.entry_pin_num.pack(pady=5)

        self.label_pin_value = Label(self.root, text="Pin Value (True/False):")
        self.label_pin_value.pack(pady=5)
        self.entry_pin_value = Entry(self.root)
        self.entry_pin_value.pack(pady=5)

        self.button_load_data = Button(self.root, text="Load Data", command=self.load_data)
        self.button_load_data.pack(pady=5)

        self.button_send_data = Button(self.root, text="Send Data", command=self.send_data)
        self.button_send_data.pack(pady=5)

    def update_data(self):
        try:
            response_soil = requests.get(url_soil)
            json_data_soil = response_soil.json()
            response_soil.close()

            formatted_data_soil = "\n".join(
                [f"Pin {entry['pin_num']}: {entry['pin_value']}" for entry in json_data_soil])
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, formatted_data_soil)
        except Exception as e:
            print("Error:", e)

        self.root.after(5000, self.update_data)  # Обновление каждые 5 секунд

    def load_data(self):
        try:
            response_pomp = requests.get(url_pomp)
            json_data_pomp = response_pomp.json()
            response_pomp.close()

            formatted_data_pomp = "\n".join(
                [f"Pin {entry['pin_num']}: {entry['pin_value']}" for entry in json_data_pomp])
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, formatted_data_pomp)
        except Exception as e:
            print("Error:", e)

    def send_data(self):
        try:
            pin_num = int(self.entry_pin_num.get())
            pin_value = self.entry_pin_value.get().lower() == 'true'

            data = {"pin_value": pin_value}
            response = requests.post(url_write + str(pin_num), json=data)

            if response.status_code == 200:
                print(f"Data sent successfully for Pin {pin_num}")
            else:
                print(f"Error sending data for Pin {pin_num}. Status code: {response.status_code}")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.geometry("400x500")  # Начальные размеры окна
    root.mainloop()
