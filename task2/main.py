import customtkinter as ctk
import tkinter as tk
 

ctk.set_appearance_mode("System")
 

ctk.set_default_color_theme("green")   
 
appWidth, appHeight = 600, 700
 

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def rand():
            self.displayBox.insert("0.0", "aboba")
 
 
        self.title("Forecast")
        self.geometry(f"{appWidth}x{appHeight}")
 

        self.nameLabel = ctk.CTkLabel(self,
                                      text="City")
        self.nameLabel.grid(row=0, column=0,
                            padx=0, pady=0,
                            sticky="ew")
 
        # Name Entry Field
        self.nameEntry = ctk.CTkEntry(self,
                         placeholder_text="Sofia")
        self.nameEntry.grid(row=0, column=1,
                            padx=0,
                            pady=20, sticky="ew")
 
        # Generate Button
        self.generateResultsButton = ctk.CTkButton(self,
                                         text="random", command=button_event)
        self.generateResultsButton.grid(row=5, column=1,
                                        padx=20, pady=20,
                                        sticky="w")
                # Generate Button
        self.generateResultsButton = ctk.CTkButton(self,
                                         text="enter")
        self.generateResultsButton.grid(row=5, column=2,
                                        padx=20, pady=20,
                                        sticky="e")
 
        # Text Box
        self.displayBox = ctk.CTkTextbox(self, width=500,
                                         height=100)
        self.displayBox.grid(row=6, column=0, columnspan=4,
                             padx=30, pady=30, sticky="nsew")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()