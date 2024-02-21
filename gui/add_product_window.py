import backend.json_data as jd
from datetime import date, datetime
import customtkinter as ctk
import tkinter          

dates = []

class FrameDateDropdowns(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.dropdown_color = '#FFFFFF'

        today = date.today()
        self.month_var = ctk.StringVar(value=today.strftime("%b"))
        self.day_var = ctk.StringVar(value=str(int(today.strftime("%d"))))
        self.year_var = ctk.StringVar(value=today.strftime("%Y"))

        self.month_dropdown = ctk.CTkOptionMenu(self, variable=self.month_var,
                                       values=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 
                                       text_color="black", fg_color=self.dropdown_color, width=50,
                                       button_color=self.dropdown_color, button_hover_color=self.dropdown_color)
        self.day_dropdown = ctk.CTkOptionMenu(self, variable=self.day_var, 
                                       values=[str(i) for i in range(1, 32)], width=50,
                                       text_color="black", fg_color=self.dropdown_color, 
                                       button_color=self.dropdown_color, button_hover_color=self.dropdown_color)
        self.year_dropdown = ctk.CTkOptionMenu(self, variable=self.year_var, 
                                       values=[str(i) for i in range(2020, int(today.strftime("%Y"))+1)], 
                                       text_color="black", fg_color=self.dropdown_color, width=50,
                                       button_color=self.dropdown_color, button_hover_color=self.dropdown_color)
        
        self.month_dropdown.grid(row=0, column=0)
        self.day_dropdown.grid(row=0, column=1)
        self.year_dropdown.grid(row=0, column=2)

class FramePickDates(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.frame_dropdowns = FrameDateDropdowns(self)
        self.button_add_date = ctk.CTkButton(self, text="Add Date", width=50)

        self.button_add_date.bind("<ButtonRelease-1>", self.add_date)

        self.frame_dropdowns.grid(row=0, column=0, padx=10, pady=10)
        self.button_add_date.grid(row=0, column=1, padx=10)

        self.next_row = 1

    def add_date(self, event):
        month_text = self.frame_dropdowns.month_var.get()
        day_text = self.frame_dropdowns.day_var.get()
        year_text = self.frame_dropdowns.year_var.get()
        date_text = f"{month_text} {day_text}, {year_text}"

        new_label = ctk.CTkLabel(self, text=date_text)
        new_label.grid(row=self.next_row, column=0, pady=5)

        dates.append(date(int(year_text),int(datetime.strftime(datetime.strptime(month_text, "%b"), '%m')), int(day_text)))
        print(dates)
        
        self.next_row += 1

        datetime.strptime((self.frame_dropdowns.month_var.get()), '%b')

class FrameRadioButtons(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.radio_var = tkinter.IntVar(value=0)
        self.radiobutton_size = 15
        self.dates_q_1 = ctk.CTkRadioButton(self, text="Just started a new bottle today", radiobutton_height=self.radiobutton_size, 
                                            radiobutton_width=self.radiobutton_size, command=master.radiobutton_event, 
                                            variable=self.radio_var, value=0)
        self.dates_q_2 = ctk.CTkRadioButton(self, text="Input previous dates", radiobutton_height=self.radiobutton_size, 
                                            radiobutton_width=self.radiobutton_size, command=master.radiobutton_event, 
                                            variable=self.radio_var, value=1)
        
        self.dates_q_1.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.dates_q_2.grid(row=1, column=0, pady=5, padx=5, sticky="w")

class FramePrice(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.label = ctk.CTkLabel(self, text="Price per bottle/container:     $ ")
        self.entry = ctk.CTkEntry(self, placeholder_text="0.00", width=60)
        self.label_post = ctk.CTkLabel(self, text="     ")

        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.label_post.grid(row=0, column=2)

class FrameVolume(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.label = ctk.CTkLabel(self, text="Volume of bottle/container:      ")
        self.entry = ctk.CTkEntry(self, placeholder_text="0", width=60)
        self.label_post = ctk.CTkLabel(self, text=" ml")

        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.label_post.grid(row=0, column=2)

class FrameRoot(ctk.CTkFrame):
    def __init__(self, master, root_app):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.root_app = root_app

        self.product_entry = ctk.CTkEntry(self, placeholder_text="Product name")
        self.frame_radio_buttons = FrameRadioButtons(self)
        self.frame_pick_dates = FramePickDates(self)
        self.frame_price = FramePrice(self)
        self.frame_volume = FrameVolume(self)

        self.submit = ctk.CTkButton(self, text="Add", width=50)
        self.submit.bind("<ButtonRelease-1>", self.add_product)
        
        self.product_entry.grid(row=0, column=0, pady=10, sticky="N")
        self.frame_radio_buttons.grid(row=1, column=0, pady=10)
        self.frame_price.grid(row=3, column=0, pady=10)
        self.frame_volume.grid(row=4, column=0, pady=10)
        self.submit.grid(row=5, column=0, pady=10)

    def radiobutton_event(self):
        value = self.frame_radio_buttons.radio_var.get()
        if value:
            self.frame_pick_dates.grid(row=2, column=0, pady=10)
        else:
            self.frame_pick_dates.grid_forget()
            self.dates = [date.today()]

    def add_product(self, event):
        product_name = self.product_entry.get()
        product_dates = dates if dates else [date.today()]
        product_price = float(self.frame_price.entry.get()) if self.frame_price.entry.get() else 0
        product_volume = float(self.frame_volume.entry.get()) if self.frame_price.entry.get() else 0

        jd.add_product(product_name, product_dates, product_price, product_volume)
        self.root_app.frame_products.refresh_products()
        self.master.destroy()


class AddProductWindow(ctk.CTkToplevel):
    def __init__(self, root_app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Add new product")
        self.geometry("400x400")

        self.frame_root = FrameRoot(self, root_app)
        self.frame_root.pack()