import tkinter as tk
import customtkinter as ctk
from .config import get_config
from .forecast import WeatherService
from tabulate import tabulate
import pandas as pd
import sys
import os
import tkinter.font as tkFont

class WeatherAppGUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config = get_config()
        self.weather_service = WeatherService(
            self.config["url"],
            self.config["apikey"],
        )
        try:
            filepath = os.path.join(
                os.path.dirname(__file__), self.config["cities_csv"]
            )
            self.weather_service.load_available_cities(filepath)
        except Exception as exc:
            print(
                "Sorry, could not load cities from file: ",
                self.config["cities_csv"],
                "\nPlease, try to edit config file. Error:",
                str(exc),
            )
            sys.exit(1)
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        self.city_label = ctk.CTkLabel(self, text="City")
        self.city_entry = ctk.CTkEntry(self, placeholder_text="Sofia")
        self.random_button = ctk.CTkButton(self, text="Random", command=self.generate_random)
        self.enter_button = ctk.CTkButton(self, text="Enter", command=self.generate_results)
        self.display_box = ctk.CTkTextbox(self, width=800, height=400)

        self.grid_columnconfigure(1, weight=1)
        self.city_label.grid(row=0, column=0, sticky="w")
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)
        self.random_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.enter_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.display_box.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


    def generate_random(self):
        self.display_box.delete("1.0", "end")
        cities = self.weather_service.get_random_cities(5)

        forecast, errors = self.weather_service.get_forecast(cities)
        for error in errors:
            print(error)

        df = pd.DataFrame(forecast)
        df_str = tabulate(df, headers="keys", tablefmt="orgtbl")

        self.display_box.insert("1.0", df_str)

        agg_field = "Temperature (C)"
        aggregated = self.weather_service.calculate_stats(forecast, agg_field)
        stat = "\nAggregated values for cities by {}".format(agg_field)
        self.display_box.insert("end", stat)

        for title, measure in aggregated.items():
            self.display_box.insert("end", f"\n{title} : {measure}")
        
        self.display_box.tag_add("center", "1.0", "end")
        self.display_box.configure(font=("Courier", 12))


    def generate_results(self):
        entered_city = self.city_entry.get()
        
        self.display_box.delete("1.0", "end")

        forecast, errors = self.weather_service.get_forecast([entered_city])
        for error in errors:
            print(error)

        df = pd.DataFrame(forecast)

        df_str = tabulate(df, headers="keys", tablefmt="orgtbl")

        self.display_box.insert("1.0", df_str)
        self.display_box.tag_add("center", "1.0", "end")
        self.display_box.configure(font=("Courier", 12))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Weather Forecast")
    root.geometry("810x500")
    app = WeatherAppGUI(root)
    app.pack(fill="both", expand=True)
    root.mainloop()