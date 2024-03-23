from tkinter import messagebox as mb
from tkinter import ttk
from glob import glob
import tkinter as tkt
import tkinter.filedialog as fd
import os
import sys

class Image_to_Text_GUI:
    
    def __init__(self) -> None:
        
        self.window = tkt.Tk()
        
        #----------------------------------------------------------------------------------------------------
        # Centering the window dynamically to different sizes of screens:
        #----------------------------------------------------------------------------------------------------
        window_height = 300
        window_width = 600
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        
        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
        
        #----------------------------------------------------------------------------------------------------
        # Applicatin title and closing question:
        #----------------------------------------------------------------------------------------------------
        self.window.title("Image to Text App")
        self.window.protocol("WM_DELETE_WINDOW", self.closing_question)
        self.window.resizable(False, False)
        self.proceed_btn_clicked = False
        
        #----------------------------------------------------------------------------------------------------
        # First Group - First Floor - File Type:
        # Label: Please select the output file format:
        # Radio Buttons: .xslx File || .csv File
        #----------------------------------------------------------------------------------------------------
        self.label_file_type_text = tkt.Label(self.window, text="Please select the output file format:", font=("Arial", 13))
        self.label_file_type_text.grid(row=0, column=0, columnspan=5, sticky= tkt.W + tkt.E)
        
        self.rb_file_type_value = tkt.IntVar()
        
        self.rb_xlsx = tkt.Radiobutton(self.window, text=".xlsx", variable= self.rb_file_type_value, value= 0, font=("Arial", 11))
        self.rb_xlsx.grid(row=1, column=1,  columnspan=2, sticky= tkt.W)
        
        self.rb_csv = tkt.Radiobutton(self.window, text=".csv", variable= self.rb_file_type_value, value= 1, font=("Arial", 11))
        self.rb_csv.grid(row=1, column=3,  columnspan=2, sticky= tkt.W)
        
        #--------------------------------------------------------------------------------------------------------
        # Separator for First Floor and Second Floor (Horizontal) and to the next building (Vertical):
        #--------------------------------------------------------------------------------------------------------
        self.separator = ttk.Separator(self.window, orient="horizontal", style="blue.TSeparator")
        self.separator.grid(row=2, column=0, columnspan=5, sticky= tkt.W + tkt.E)
        
        self.separator = ttk.Separator(self.window, orient="vertical", style="blue.TSeparator")
        self.separator.grid(row=0, column=5, rowspan=6, sticky= tkt.N + tkt.S)
        
        #----------------------------------------------------------------------------------------------------
        # Second Group - Second Floor - Left - Output Path:
        # Label: Output file location:
        # Check Box: Default || Button: Browse
        # Label: Reflect the current selected path.
        #----------------------------------------------------------------------------------------------------
        self.label_output_path_text = tkt.Label(self.window, text="Output file location:", font=("Arial", 13))
        self.label_output_path_text.grid(row=3, column=0, columnspan=2, sticky= tkt.W + tkt.E, padx=15)
        
        self.cb_output_path_value = tkt.IntVar()
        self.cb_output_path = tkt.Checkbutton(self.window, text="Default", variable= self.cb_output_path_value, command=self.output_path_cb, font=("Arial", 11))
        self.cb_output_path.grid(row=4, column=0, sticky= tkt.W)
        self.cb_output_path.select()
        
        self.btn_output_path = tkt.Button(self.window, text="Browse", command=self.output_path_btn, font=("Arial", 11))
        self.btn_output_path.grid(row=4, column=1, sticky= tkt.W, padx=15)
        
        self.label_output_path = tkt.Label(self.window, font=("Arial", 9))
        self.label_output_path.grid(row=5, column=0, columnspan=2, sticky= tkt.W)
        
        #--------------------------------------------------------------------------------------------------------
        # Separator for Second Floor - Left and Right (Vertical):
        #--------------------------------------------------------------------------------------------------------
        self.separator = ttk.Separator(self.window, orient="vertical", style="blue.TSeparator")
        self.separator.grid(row=3, column=2, rowspan=6, sticky= tkt.N + tkt.S)
        
        #----------------------------------------------------------------------------------------------------
        # Second Group - Second Floor - Right - Image Path:
        # Label: Image location:
        # Check Box: Default || Button: Browse
        # Label: Reflect the current selected path.
        #----------------------------------------------------------------------------------------------------
        self.label_image_path_text = tkt.Label(self.window, text="Image location:", font=("Arial", 13))
        self.label_image_path_text.grid(row=3, column=3, columnspan=2, sticky= tkt.W + tkt.E, padx=15)
        
        self.cb_image_path_value = tkt.IntVar()
        self.cb_image_path = tkt.Checkbutton(self.window, text="Default", variable= self.cb_image_path_value, command=self.image_path_cb, font=("Arial", 11))
        self.cb_image_path.select()
        self.cb_image_path.grid(row=4, column=3, sticky= tkt.W)
        
        self.btn_image_path = tkt.Button(self.window, text="Browse", command=self.image_path_btn, font=("Arial", 11))
        self.btn_image_path.grid(row=4, column=4, sticky= tkt.W, padx=15)
        
        self.label_image_path = tkt.Label(self.window, font=("Arial", 9))
        self.label_image_path.grid(row=5, column=3, columnspan=2, sticky= tkt.W)
        
        #--------------------------------------------------------------------------------------------------------
        # Separator for Second Floor and Third Floor (Horizontal):
        #--------------------------------------------------------------------------------------------------------
        self.separator = ttk.Separator(self.window, orient="horizontal", style="blue.TSeparator")
        self.separator.grid(row=6, column=0, columnspan=9, sticky= tkt.W + tkt.E)
        
        #----------------------------------------------------------------------------------------------------
        # Third Floor - Proceed Button:
        #----------------------------------------------------------------------------------------------------
        self.btn_proceed = tkt.Button(self.window, text="Proceed", font=("Arial", 14), command=self.handle_proceed)
        self.btn_proceed.grid(row=7, column=0, rowspan=3, columnspan=2)
        
        #----------------------------------------------------------------------------------------------------
        # Second Building - First Floor - ISBN Formats:
        #----------------------------------------------------------------------------------------------------
        self.label_isbn_format_text = tkt.Label(self.window, text="Please select the ISBN format:", font=("Arial", 13))
        self.label_isbn_format_text.grid(row=0, column=6, columnspan=3, sticky= tkt.W + tkt.E, padx=15)

        self.rb_isbn_format_value = tkt.IntVar()

        self.rb_isbn_one = tkt.Radiobutton(self.window, text="1-2345-6789-X\n(1 digit at the front)", variable=self.rb_isbn_format_value, value=0, font=("Arial", 9))
        self.rb_isbn_one.grid(row=1, column=7)

        self.rb_isbn_two = tkt.Radiobutton(self.window, text="12-3456-789-X\n(2 digits at the front)", variable=self.rb_isbn_format_value, value=1, font=("Arial", 9))
        self.rb_isbn_two.grid(row=2, column=7)

        self.rb_isbn_three = tkt.Radiobutton(self.window, text="123-456-789-X\n(3 digits at the front)", variable=self.rb_isbn_format_value, value=2, font=("Arial", 9))
        self.rb_isbn_three.grid(row=3, column=7)

        self.rb_isbn_four = tkt.Radiobutton(self.window, text="1234-567-89-X\n(4 digits at the front)", variable=self.rb_isbn_format_value, value=3, font=("Arial", 9))
        self.rb_isbn_four.grid(row=4, column=7)

        self.rb_isbn_five = tkt.Radiobutton(self.window, text="12345-67-89-X\n(5 digits at the front)", variable=self.rb_isbn_format_value, value=4, font=("Arial", 9))
        self.rb_isbn_five.grid(row=5, column=7)
        
        #----------------------------------------------------------------------------------------------------
        # Second Building - Second Floor - Tesseract Path:
        # Label: Tesseract location:
        # Label: Shows the path for the .exe file.
        #----------------------------------------------------------------------------------------------------
        self.label_tesseract_path_text = tkt.Label(self.window, text="Tesseract location:", font=("Arial", 13))
        self.label_tesseract_path_text.grid(row=7, column=3, columnspan=6, sticky= tkt.W + tkt.E)
        
        self.label_tesseract_path_one = tkt.Label(self.window, font=("Arial", 9))
        self.label_tesseract_path_one.grid(row=8, column=3, columnspan=6, sticky= tkt.W + tkt.E,)
        self.label_tesseract_path_two = tkt.Label(self.window, font=("Arial", 9))
        self.label_tesseract_path_two.grid(row=9, column=3, columnspan=6, sticky= tkt.W + tkt.E,)
        
        #----------------------------------------------------------------------------------------------------
        # Dynamic location paths and default paths:
        # NOTE:
        # The path for the "Downloads" is for my computer for now. Need to change this once this is for sale.
        # Change this to conventional Path:
        # f"C:/Users/{self.username}/Downloads"
        #----------------------------------------------------------------------------------------------------
        self.username = os.getlogin()
        self.downloads_folder = f"D:/{self.username}/Downloads"
        self.selected_folder_output = str(self.string_len_validation_one(self.downloads_folder))
        self.selected_folder_image = str(self.string_len_validation_one(self.downloads_folder))
        
        self.output_path_cb() # Displays the default path.
        self.image_path_cb() # Displays the default path.
        self.tesseract_find_path_at_start() # Displays the path if found and shows the path browsing if not found.
        
        
        self.window.mainloop()
        
    #----------------------------------------------------------------------------------------------------
    # Closing method. This method will trigger when the user click in the "x" button of the window:
    #----------------------------------------------------------------------------------------------------
    def closing_question(self):
        if mb.askyesno(title="Quit", message="Do you really want to quit the application?") is True:
            sys.exit(0)
    
    #----------------------------------------------------------------------------------------------------
    # Two methods used for the Output file location:
    #----------------------------------------------------------------------------------------------------
    def output_path_btn(self):
        self.selected_folder_output = fd.askdirectory()
        if self.selected_folder_output:
            handler = self.string_len_validation_one(self.selected_folder_output)
            self.label_output_path.config(text=handler)
            self.cb_output_path_value.set(0)
        else:
            self.selected_folder_output = self.downloads_folder
            handler = self.string_len_validation_one(self.selected_folder_output)
            self.label_output_path.config(text=handler)
            self.cb_output_path_value.set(1)
    
    def output_path_cb(self):
        self.selected_folder_output = self.downloads_folder
        if self.cb_output_path_value.get() == 1:
            handler = self.string_len_validation_one(self.selected_folder_output)
            self.label_output_path.config(text=handler)
        else:
            handler = self.string_len_validation_one(self.selected_folder_output)
            self.label_output_path.config(text=handler)
    
    #----------------------------------------------------------------------------------------------------
    # Two methods used for the Image file location:
    #----------------------------------------------------------------------------------------------------
    def image_path_btn(self):
        self.selected_folder_image = fd.askdirectory()
        if self.selected_folder_image:
            handler = self.string_len_validation_one(self.selected_folder_image)
            self.label_image_path.config(text=handler)
            self.cb_image_path_value.set(0)
        else:
            self.selected_folder_image = self.downloads_folder
            self.cb_image_path_value.set(1)
            handler = self.string_len_validation_one(self.selected_folder_image)
            self.label_image_path.config(text=handler)
    
    def image_path_cb(self):
        self.selected_folder_image = self.downloads_folder
        if self.cb_image_path_value.get() == 1:
            handler = self.string_len_validation_one(self.selected_folder_image)
            self.label_image_path.config(text=handler)
        else:
            handler = self.string_len_validation_one(self.selected_folder_image)
            self.label_image_path.config(text=handler)
    
    #----------------------------------------------------------------------------------------------------
    # Methods used for Tesseract location:
    #----------------------------------------------------------------------------------------------------
    def tesseract_find_path_at_start(self):
        username = os.getlogin()
        found = False
        tesseract_candidate_folders = ["C:/Program Files/Tesseract-OCR/",
            "C:/Program Files (x86)/Tesseract-OCR/",
            f"C:/Users/{username}/AppData/Local/Tesseract-OCR/",
            f"C:/Users/{username}/AppData/Local/Programs/Tesseract-OCR/"]
        
        for per_folder in tesseract_candidate_folders:
            get_tesseract_exe = glob(fr"{per_folder}/tesseract.exe")
            if len(get_tesseract_exe) != 0:
                found = True
                mb.showinfo(title="Success!", message="Found \"tesseract.exe\" within the default folders!")
                self.tesseract_path_formatter(str(get_tesseract_exe[0]))
                break
        
        if found is False:
            response = mb.askyesno(title="Failed", message="Did not found \"tesseract.exe\" in any of the default folders.\n\nDo you want to locate the folder manually or exit the app?\n\nClick \"Yes\" to manually locate the folder or \"No\" to Exit the app.")
            if response is True:
                self.tesseract_path_browse()
            else:
                sys.exit(0)
    
    def tesseract_path_formatter(self, found_path):
        self.selected_folder_tesseract = found_path
        if len(found_path) > 45:
            one, two = self.string_len_validation_two(found_path)
            self.label_tesseract_path_one.config(text=str(one))
            self.label_tesseract_path_two.config(text=str(two))
        else:
            one = self.string_len_validation_two(found_path)
            self.label_tesseract_path_one.config(text=str(one))
            self.label_tesseract_path_two.config(text="")
    
    def tesseract_path_browse(self):
        self.selected_folder_tesseract = fd.askdirectory() + "/tesseract.exe"
        if self.selected_folder_tesseract:
            self.tesseract_validate_path()
            self.tesseract_path_formatter(self.selected_folder_tesseract)
    
    def tesseract_validate_path(self):
        tesseract_folder_split = self.selected_folder_tesseract.split("/tesseract.exe")
        tesseract_file_list = glob(f"{tesseract_folder_split[0]}/tesseract.exe")
        found = False
        
        if len(tesseract_file_list) != 0:
            found = True
            mb.showinfo(title="Success!", message="\"tesseract.exe\" found in the selected folder!")
            self.tesseract_path_formatter(str(tesseract_file_list[0]))
        
        if found is False:
            response = mb.askyesno(title="Error", message="\"tesseract.exe\" not found in the selected folder.\nPlease select the correct path.\n\nDo you want to locate the folder manually or exit the app?\n\nClick \"Yes\" to manually locate the folder and \"No\" to Exit the app.")
            if response is True:
                self.tesseract_path_browse()
            else:
                sys.exit(0)
    
    #----------------------------------------------------------------------------------------------------
    # Two methods that validates string lenghts:
    # One for Output Folder and Images Folder.
    # One for Tesseract Folder.
    #----------------------------------------------------------------------------------------------------
    def string_len_validation_one(self, path_string_one):
        if len(path_string_one) > 20:
            return path_string_one[:20] + "..."
        else:
            return path_string_one
    
    def string_len_validation_two(self, path_string_two):
        if len(path_string_two) > 45:
            return path_string_two[:45], path_string_two[45:]
        else:
            return path_string_two
    
    #----------------------------------------------------------------------------------------------------
    # Methods for Proceed button:
    #----------------------------------------------------------------------------------------------------
    def button_state(self):
        btn_state = 0
        if self.proceed_btn_clicked is True:
            btn_state = 1
            return btn_state
        else:
            btn_state = 0
            return btn_state
            
    def variable_values(self):
        file_type = self.rb_file_type_value.get()
        isbn_format = self.rb_isbn_format_value.get()
        output_path = self.selected_folder_output
        image_path = self.selected_folder_image
        tesseract_path = self.selected_folder_tesseract
        
        return file_type, isbn_format, output_path, image_path, tesseract_path
    
    def handle_proceed(self):
        if mb.askyesno(title="Confirm", message="Proceed with this settings?"):
            self.proceed_btn_clicked = True
            self.variable_values()
            self.window.destroy()
    
if __name__ == "__main__":
    Image_to_Text_GUI()