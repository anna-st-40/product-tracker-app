import backend.json_data as jd
import customtkinter as ctk
import tkinter 

#TODO: Display and be able to delete / add dates

class FrameRadioButtons(ctk.CTkFrame):
    def __init__(self, master, product):
        super().__init__(master, fg_color="transparent")

        self.product = product
        self.master = master

        self.radio_var = tkinter.IntVar(value=0)
        self.radiobutton_size = 15
        self.yes = ctk.CTkRadioButton(self, text="No", radiobutton_height=self.radiobutton_size, 
                                            radiobutton_width=self.radiobutton_size, command=self.radiobutton_event, 
                                            variable=self.radio_var, value=0)
        self.no = ctk.CTkRadioButton(self, text="Yes", radiobutton_height=self.radiobutton_size, 
                                            radiobutton_width=self.radiobutton_size, command=self.radiobutton_event, 
                                            variable=self.radio_var, value=1)
        
        self.delete = ctk.CTkButton(self, text=f"Delete")
        self.delete.bind("<ButtonRelease-1>", self.delete_product)
        
        self.yes.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.no.grid(row=1, column=0, pady=5, padx=5, sticky="w")

    def radiobutton_event(self):
        value = self.radio_var.get()
        if value:
             self.delete.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        else:
            self.delete.grid_forget()

    def delete_product(self, event):
        jd.delete_product(self.product) 
        self.master.master.root_app.frame_products.refresh_products()
        self.master.master.destroy()

class ConfirmDeleteWindow(ctk.CTkToplevel):
    def __init__(self, master, product, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master

        self.label = ctk.CTkLabel(self, text=f"Are you sure you want to delete {product}?")
        self.radio_buttons = FrameRadioButtons(self, product)     

        self.label.pack(padx=10, pady=10)
        self.radio_buttons.pack(anchor="n")


class EditProductWindow(ctk.CTkToplevel):
    def __init__(self, master, product, root_app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.product = product
        self.root_app = root_app

        self.title("Edit product")
        self.geometry("400x400")

        self.test_label = ctk.CTkLabel(self, text=product)
        self.test_label.pack()

        self.delete = ctk.CTkButton(self, text=f"Delete {product}")
        self.delete.bind("<ButtonRelease-1>", self.confirm_delete)
        self.delete.pack()

        self.confirm_delete_window = None


    def confirm_delete(self, event):
        self.confirm_delete_window = ConfirmDeleteWindow(self, self.product)
        self.confirm_delete_window.after(100, self.confirm_delete_window.lift)