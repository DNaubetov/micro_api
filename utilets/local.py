import requests
import tkinter as tk
from tkinter import scrolledtext, Label, Entry, Button, Checkbutton

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

        self.buttons_soil = []
        self.buttons_pomp = []

        # self.create_buttons(url_soil, self.buttons_soil)
        self.create_buttons(url_pomp, self.buttons_pomp)

        self.update_data()

    def create_buttons(self, url, buttons):
        try:
            response = requests.get(url)
            json_data = response.json()
            response.close()

            for entry in json_data:
                pin_num = entry['pin_num']
                pin_value = entry['pin_value']

                check_button = Checkbutton(self.root, text=f"Pin {pin_num}",
                                           command=lambda num=pin_num: self.send_data(url_write, num))
                check_button.pack(pady=5)
                buttons.append({"pin_num": pin_num, "button": check_button, "pin_value": pin_value})
        except Exception as e:
            print("Error:", e)

    def update_data(self):
        try:
            self.update_buttons_data(url_soil, self.buttons_soil)
            self.update_buttons_data(url_pomp, self.buttons_pomp)

        except Exception as e:
            print("Error:", e)

        self.root.after(5000, self.update_data)  # Обновление каждые 5 секунд

    def update_buttons_data(self, url, buttons):
        response = requests.get(url)
        json_data = response.json()
        response.close()

        for entry in json_data:
            pin_num = entry['pin_num']
            pin_value = entry['pin_value']

            for button in buttons:
                if button["pin_num"] == pin_num:
                    button["pin_value"] = pin_value
                    button["button"].deselect() if not pin_value else button["button"].select()

        formatted_data = "\n".join([f"Pin {entry['pin_num']}: {entry['pin_value']}" for entry in json_data])
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, formatted_data)

    def send_data(self, url, pin_num):
        try:
            data = {"pin_value": not self.get_pin_value(pin_num, url)}
            response = requests.post(url + str(pin_num), json=data)

            if response.status_code == 200:
                print(f"Data sent successfully for Pin {pin_num}")
            else:
                print(f"Error sending data for Pin {pin_num}. Status code: {response.status_code}")

        except Exception as e:
            print("Error:", e)

    def get_pin_value(self, pin_num, url):
        for button in self.get_buttons_by_url(url):
            if button["pin_num"] == pin_num:
                return button["pin_value"]
        return None

    def get_buttons_by_url(self, url):
        if url == url_soil:
            return self.buttons_soil
        elif url == url_pomp:
            return self.buttons_pomp
        else:
            return []


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.geometry("400x500")  # Начальные размеры окна
    root.mainloop()
