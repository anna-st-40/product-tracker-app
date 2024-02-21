import sys, os
sys.path.append(os.getcwd())

import backend.json_data as jd
from gui.add_product_window import AddProductWindow
from gui.edit_product_window import EditProductWindow
from PIL import Image

import customtkinter as ctk

class FrameAddProduct(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent") 

        self.addp_button = ctk.CTkButton(self, text="Add a product")
        self.addp_button.bind("<ButtonRelease-1>", self.display_adding_menu)
        self.addp_button.pack(pady=10)

        self.adding_menu_window = None

    def display_adding_menu(self, event):
        
        if self.adding_menu_window is None or not self.adding_menu_window.winfo_exists():
            self.adding_menu_window = AddProductWindow(app, self)
            self.adding_menu_window.after(100, self.adding_menu_window.lift)
            
        else:
            self.adding_menu_window.focus()

class FrameProduct(ctk.CTkFrame):
    def __init__(self, master, name:str, dates:list, avg_duration, ending):
        super().__init__(master, fg_color='#FFFFFF', border_color="#ECEEF1", border_width=2)
        self.name = name

        self.product_name = ctk.CTkLabel(master=self, text=name, width=100)
        self.product_duration = ctk.CTkLabel(master=self, text=f"{avg_duration} days", width=100)
        self.current_started = ctk.CTkLabel(master=self, text=jd.date_to_words(dates[-1]), width=100)
        self.button_start_new = ctk.CTkButton(master=self, text="Start new bottle", width=100)
        self.ending = ctk.CTkLabel(master=self, text=jd.date_to_words(ending), width=100)
        self.my_image = ctk.CTkImage(light_image=Image.open("gui/resources/edit_icon.png"), size=(20, 20))
        self.image_label = ctk.CTkLabel(self, image=self.my_image, text="")

        self.button_start_new.bind("<ButtonRelease-1>", self.start_new_bottle)
        self.image_label.bind("<ButtonRelease-1>", self.edit_product)

        self.product_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.product_duration.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.current_started.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.button_start_new.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.ending.grid(row=0, column=4, padx=10, pady=10, sticky="w")
        self.image_label.grid(row=0, column=5, padx=10, pady=10, sticky="w")

        self.edit_menu_window = None
    
    def start_new_bottle(self, event):
        jd.start_new_container(self.name)
        app.frame_products.refresh_products()

    def edit_product(self, event):
        if self.edit_menu_window is None or not self.edit_menu_window.winfo_exists():
            self.edit_menu_window = EditProductWindow(self, self.name, app)
            self.edit_menu_window.after(100, self.edit_menu_window.lift)
            
        else:
            self.edit_menu_window.focus()

class FrameHeader(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color='transparent')
        
        self.product_name = ctk.CTkLabel(master=self, text="Product", width=100)
        self.product_duration = ctk.CTkLabel(master=self, text=f"Duration", width=100)
        self.current_started = ctk.CTkLabel(master=self, text=f"Current bottle opened", width=100)
        self.space1 = ctk.CTkFrame(master=self, width=90, height=10, fg_color="transparent")
        self.ending = ctk.CTkLabel(master=self, text=f"Set to run out", width=100)
        self.space2 = ctk.CTkFrame(master=self, width=10, height=10, fg_color="transparent")

        self.product_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.product_duration.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.current_started.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.space1.grid(row=0, column=3, padx=10, pady=10)
        self.ending.grid(row=0, column=4, padx=10, pady=10, sticky="w")
        self.space2.grid(row=0, column=5, padx=25, pady=10, sticky="w")

class FrameProducts(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.refresh_products()

    def refresh_products(self):
        for widget in self.winfo_children():
            widget.destroy()

        products = jd.pull_products()

        for k, v in products.items():
            product_frame = FrameProduct(self, k, v["dates"], v["avg_duration"], v["ending"])
            product_frame.pack(pady=2)

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#F6F7F8")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.geometry("700x500")
        self.title("Toiletries Duration Logger")

        self.frame_add = FrameAddProduct(self)
        self.frame_add.pack()

        self.header = FrameHeader(self)
        self.header.pack()

        self.frame_products = FrameProducts(self)
        self.frame_products.pack()
  
app = App()
app.mainloop()