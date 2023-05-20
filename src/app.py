import tkinter
import customtkinter
from PIL import Image

import os
import pyautogui
from pynput import mouse, keyboard
import threading

customtkinter.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"

class App(customtkinter.CTk):

    #GUI----------------------------------------------------------------------#
    def __init__(self):
        super().__init__()

        self.left_mouse_button = ["left", 50, None, 0] # [button (0 left, 1 right), cps (50 start value), key (start None), mode (0 hold, 1 switch)]
        self.right_mouse_button =  ["right", 50, None, 0]

        self.selected_button = 0  # 0 left, 1 right

        self.start_clicker()

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")

        # basic config
        self.title("Autoclicker.py")
        self.geometry(f"{600}x{605}")
        self.iconbitmap(os.path.join(image_path, "dark_e_mouse.ico"))

        # when the window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # configure grid layout
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.resizable(width=False, height=False)

        MOUSE_IMAGE_HIGHT = 375
        MOUSE_IMAGE_WIDTH = 250

        self.l_mouse = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "light_l_mouse.png")),
            dark_image=Image.open(os.path.join(image_path, "dark_l_mouse.png")), size=(MOUSE_IMAGE_WIDTH, MOUSE_IMAGE_HIGHT))

        self.r_mouse = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "light_r_mouse.png")),
            dark_image=Image.open(os.path.join(image_path, "dark_r_mouse.png")), size=(MOUSE_IMAGE_WIDTH, MOUSE_IMAGE_HIGHT))

        self.submit_button = customtkinter.CTkButton(
            self, text="Submit", width=100, height=30, fg_color="#0094FF", command=self.start_clicker)
        self.submit_button.grid(column=1, row=3, padx=(0, 120), pady=(0, 0), sticky="se")

        self.submit_button = customtkinter.CTkButton(
            self, text="Exit", width=100, height=30, fg_color="#0094FF", command=self.on_closing)
        self.submit_button.grid(column=1, row=3, padx=(0, 10), pady=(0, 0), sticky="se")


        # mouse frame -------------------------------------------
        self.mouse_frame = customtkinter.CTkFrame(self)
        self.mouse_frame.grid(column=0, row=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.mouse = customtkinter.CTkLabel(master=self.mouse_frame, image=self.l_mouse, text='')
        self.mouse.grid(column=1, row=0, padx=(0, 0), pady=(20, 20), sticky="nsew")
        self.mouse.configure(width=0, height=0)

        self.mouse_radio_var = tkinter.IntVar(value=0)

        self.radio_button_l = customtkinter.CTkRadioButton(
            master=self.mouse_frame, text="left mouse button", variable=self.mouse_radio_var, value=0, fg_color="#0094FF",
            command=self.mouse_select)
        self.radio_button_l.grid(column=0, row=0, padx=(20, 20), pady=(0, 170), sticky="e")
        self.radio_button_l.configure(width=0, height=0)

        self.radio_button_r = customtkinter.CTkRadioButton(
            master=self.mouse_frame, text="right mouse button", variable=self.mouse_radio_var, value=1, fg_color="#0094FF",
            command=self.mouse_select)
        self.radio_button_r.grid(column=2, row=0, padx=(20, 20), pady=(0, 170), sticky="w")
        self.radio_button_r.configure(width=0, height=0)

        # cps frame -------------------------------------------
        self.cps_frame = customtkinter.CTkFrame(self, width=287.5, height=120)
        self.cps_frame.grid(column=0, row=1, padx=(10, 10), pady=(0, 10), sticky="nsew")
        self.cps_frame.grid_columnconfigure((0, 1), weight=1)
        self.cps_frame.grid_rowconfigure((0, 1), weight=1)
        self.cps_frame.grid_propagate(False)

        # cps value frame
        self.cps_value_frame = customtkinter.CTkFrame(master=self.cps_frame, width=100, height=30)
        self.cps_value_frame.grid(column=0, row=0, padx=(20, 0), pady=(20, 0), sticky="se")
        self.cps_value_frame.columnconfigure(0, weight=1)
        self.cps_value_frame.rowconfigure(0, weight=1)
        self.cps_value_frame.grid_propagate(False)

        self.cps_value_label = customtkinter.CTkLabel(self.cps_value_frame, text="50", fg_color="transparent")
        self.cps_value_label.grid(column=0, row=0, padx=(5, 5), pady=(0, 0), sticky="nsew")

        self.cps_label = customtkinter.CTkLabel(self.cps_frame, text="clicks per minute", fg_color="transparent", )
        self.cps_label.grid(column=1, row=0, padx=(10, 20), pady=(20, 0), sticky="sw")

        self.cps_slider = customtkinter.CTkSlider(self.cps_frame, from_=0, to=100, fg_color="#0094FF",
                                                  command=self.cps_value_slider)
        self.cps_slider.grid(column=0, row=1, columnspan=2, padx=(20, 20), pady=(10, 20), sticky="new")

        # hotkey frame -------------------------------------------
        self.activ_frame = customtkinter.CTkFrame(self, width=287.5, height=120)
        self.activ_frame.grid(column=1, row=1, padx=(0, 10), pady=(0, 10), sticky="nsew")
        self.activ_frame.grid_columnconfigure((0, 1), weight=1)
        self.activ_frame.grid_rowconfigure((0, 1), weight=1)
        self.activ_frame.grid_propagate(False)

        # key frame
        self.key_frame = customtkinter.CTkFrame(master=self.activ_frame, width=100, height=30)
        self.key_frame.grid(column=0, row=0, padx=(20, 0), pady=(20, 0), sticky="se")
        self.key_frame.columnconfigure(0, weight=1)
        self.key_frame.rowconfigure(0, weight=1)
        self.key_frame.grid_propagate(False)

        self.key_label = customtkinter.CTkLabel(self.key_frame, text="None", fg_color="transparent")
        self.key_label.grid(column=0, row=0, padx=(5, 5), pady=(0, 0), sticky="nsew")

        self.change_key_button = customtkinter.CTkButton(self.activ_frame, text="Select key", width=100, height=30,
                                                         fg_color="#0094FF", command=self.change_key)
        self.change_key_button.grid(column=1, row=0, padx=(20, 20), pady=(20, 0), sticky="sw")

        self.activ_radio_var = tkinter.IntVar(value=0)

        self.radio_button_hold = customtkinter.CTkRadioButton(master=self.activ_frame, text="hold",
                                                              variable=self.activ_radio_var, value=0,
                                                              fg_color="#0094FF", command=self.change_mode)
        self.radio_button_hold.grid(column=0, row=1, padx=(45, 0), pady=(10, 20), sticky="nw")
        self.radio_button_hold.configure(width=0, height=0)

        self.radio_button_switch = customtkinter.CTkRadioButton(master=self.activ_frame, text="switch",
                                                                variable=self.activ_radio_var, value=1,
                                                                fg_color="#0094FF", command=self.change_mode)
        self.radio_button_switch.grid(column=1, row=1, padx=(0, 45), pady=(10, 20), sticky="ne")
        self.radio_button_switch.configure(width=0, height=0)

#FUNCTIONS----------------------------------------------------------------------#

    def start_clicker(self):
        try:
            self.clicker.stop()
            self.clicker.join()
        except:
            pass

        self.clicker = Clicker()

        self.clicker.clmb = self.left_mouse_button
        self.clicker.crmb = self.right_mouse_button

        self.clicker.start()

        

    def on_closing(self):
        try:
            self.clicker.stop()
            self.clicker.join()
            self.destroy()
        except:
            pass

    #---------------------------#

    def mouse_select(self):
        button = self.mouse_radio_var.get()

        if button == 0:
            img = self.l_mouse
            self.selected_button = 0  # 0 left, 1 right

            self.cps_value_label.configure(text=str(self.left_mouse_button[1]))
            self.cps_slider.set(self.left_mouse_button[1])

            if not self.left_mouse_button[2] == None:
                key = self.left_mouse_button[2].split('.')
                if key[0] == "keyboard":
                    key = key
                elif key[0] == "Button":
                    if key[1] == "x1":
                        key = "Mouse button 4"
                    elif key[1] == "x2":
                        key = "Mouse button 5"
            else:
                key = "None"

            self.key_label.configure(text=str(key))

            if self.left_mouse_button[3] == 0:
                self.radio_button_hold.select()

            elif self.left_mouse_button[3] == 1:
                self.radio_button_switch.select()

        else:
            img = self.r_mouse
            self.selected_button = 1  # 0 left, 1 right

            self.cps_value_label.configure(text=str(self.right_mouse_button[1]))
            self.cps_slider.set(self.right_mouse_button[1])

            if not self.right_mouse_button[2] == None:
                key = self.right_mouse_button[2].split('.')
                if key[0] == "keyboard":
                    key = key
                elif key[0] == "Button":
                    if key[1] == "x1":
                        key = "Mouse button 4"
                    elif key[1] == "x2":
                        key = "Mouse button 5"
            else:
                key = "None"

            self.key_label.configure(text=str(key))

            if self.right_mouse_button[3] == 0:
                self.radio_button_hold.select()

            elif self.right_mouse_button[3] == 1:
                self.radio_button_switch.select()

        self.mouse.destroy()    

        self.mouse = customtkinter.CTkLabel(master=self.mouse_frame, image=img, text='')
        self.mouse.grid(column=1, row=0, padx=(0, 0), pady=(20, 20), sticky="nsew")
        self.mouse.configure(width=0, height=0)

    #---------------------------#

    def cps_value_slider(self, value):
        self.cps_value_label.configure(text=str(round(value)))

        if self.selected_button == 0:  # 0 left, 1 right
            self.left_mouse_button[1] = round(value)

        elif self.selected_button == 1:  # 0 left, 1 right 
            self.right_mouse_button[1] = round(value)

    #---------------------------#

    def change_key(self):
        self.key_label.configure(text="Recording...")
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<Button>", self.on_mouse_click)

    def on_key_press(self, event):
        key = event.keysym

        self.unbind("<KeyPress>")
        self.unbind("<Button>")
        self.key_label.configure(text=key)

        if self.selected_button == 0:  # 0 left, 1 right
            self.left_mouse_button[2] =  key

        elif self.selected_button == 1:  # 0 left, 1 right 
            self.right_mouse_button[2] = key
        
    def on_mouse_click(self, event):
        button = event.num
        if button == 2 or button == 4 or button == 5:

            self.unbind("<KeyPress>")
            self.unbind("<Button>")
            self.key_label.configure(text=f"Mouse button {button}")

            if button == 2:
                key = 'Button.middle'
            elif button == 4:
                key = 'Button.x1'
            elif button == 5:
                key = 'Button.x2'

            if self.selected_button == 0: # 0 left, 1 right
                self.left_mouse_button[2] = key

            elif self.selected_button == 1: # 0 left, 1 right
                self.right_mouse_button[2] = key

    #---------------------------#

    def change_mode(self):
        mode = self.activ_radio_var.get()

        if self.selected_button == 0: # 0 left, 1 right
            self.left_mouse_button[3] = mode

        elif self.selected_button == 1: # 0 left, 1 right
            self.right_mouse_button[3] = mode

#Clicker----------------------------------------------------------------------#

class Clicker(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_running = False
        self.click_loop_thread = None

    def click_loop(self, button, cps):
        # accuracy calculation
        actual_cps = -0.0007301777170198202*cps**2 + 0.9913716678058782*cps + 0.1362499999999756
        proc_diff = round(((actual_cps-cps)/cps), 3)*(-1)
        corr_cps = cps+(cps*proc_diff) 
        pause = 1 / corr_cps

        while self.is_running:
            pyautogui.click(button=button)
            pyautogui.PAUSE = pause
            
    def on_press(self, key):
        key = str(key).replace("'", "")

        if self.clmb[3] == 0:
            if not self.is_running:
                if key == self.clmb[2]:
                    self.is_running = True
                    self.click_loop_thread = threading.Thread(target=self.click_loop, args=("left", self.clmb[1]))
                    self.click_loop_thread.start()

        elif self.clmb[3] == 1:
            if self.is_running:
                if key == self.clmb[2]:
                    self.is_running = False
            
            elif not self.is_running:
                if key == self.clmb[2]:
                    self.is_running = True
                    self.click_loop_thread = threading.Thread(target=self.click_loop, args=("left", self.clmb[1]))
                    self.click_loop_thread.start()

        #---------------------------#

        if self.crmb[3] == 0:
            if not self.is_running:
                if key == self.crmb[2]:
                    self.is_running = True
                    self.click_loop_thread = threading.Thread(target=self.click_loop, args=("right", self.crmb[1]))
                    self.click_loop_thread.start()

        elif self.crmb[3] == 1:
            if self.is_running:
                if key == self.crmb[2]:
                    self.is_running = False

            elif not self.is_running:     
                if key == self.crmb[2]:
                    self.is_running = True
                    self.click_loop_thread = threading.Thread(target=self.click_loop, args=("right", self.crmb[1]))
                    self.click_loop_thread.start()  

    def on_release(self, key):
        key = str(key).replace("'", "")

        if self.clmb[3] == 0:
            if key == self.clmb[2]:
                self.is_running = False

        elif self.crmb[3] == 0:
            if key == self.crmb[2]:
                self.is_running = False

    def on_click(self, x, y, button, pressed):
        if self.clmb[3] == 0:
            if not self.is_running and pressed:
                if str(button) == self.clmb[2]:
                    self.is_running = True
                    self.click_loop_thread = threading.Thread(target=self.click_loop, args=("left", self.clmb[1]))
                    self.click_loop_thread.start()

            elif self.is_running and not pressed:
                if str(button) == self.clmb[2]:
                    self.is_running = False

        elif self.clmb[3] == 1:
            if self.is_running and pressed:
                if str(button) == self.clmb[2]:
                    self.is_running = False

            elif not self.is_running and pressed:
                if str(button) == self.clmb[2]:
                    self.is_running = True
                    self.click_loop_thread = threading.Thread(target=self.click_loop, args=("left", self.clmb[1]))
                    self.click_loop_thread.start()
        
        #---------------------------#

        if self.crmb[3] == 0:
            if not self.is_running and pressed:
                if str(button) == self.crmb[2]:
                        self.is_running = True
                        self.click_loop_thread = threading.Thread(target=self.click_loop, args=("right", self.crmb[1]))
                        self.click_loop_thread.start()

            elif self.is_running and not pressed:
                if str(button) == self.crmb[2]:
                    self.is_running = False

        elif self.crmb[3] == 1:
            if self.is_running and pressed:
                if str(button) == self.crmb[2]:
                    self.is_running = False

            elif not self.is_running and pressed:
                if str(button) == self.crmb[2]:
                    self.is_running = True
                    self.click_loop_thread = threading.Thread(target=self.click_loop, args=("right", self.crmb[1]))
                    self.click_loop_thread.start()

    def stop(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
    
    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.keyboard_listener:
            with mouse.Listener(on_click=self.on_click) as self.mouse_listener:
                self.keyboard_listener.join()
                self.mouse_listener.join()

#----------------------------------------------------------------------#

if __name__ == "__main__":
    app = App()
    app.mainloop()