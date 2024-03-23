#--------------------------------------------------------------------------------------------------------
# Declaring Imports:
#--------------------------------------------------------------------------------------------------------
from glob import glob
from tqdm import trange
from readchar import readkey
from datetime import datetime
from colorama import Fore
import time
import os
import sys
import re
import cv2
import pytesseract
import shutil as sl
import pandas as pd
import numpy as np

#--------------------------------------------------------------------------------------------------------
# Declaring some default values for the meantime:
#--------------------------------------------------------------------------------------------------------
# file_type = 0
# isbn_format = 0
# output_path = "D:/emn33/Downloads/Output"
# image_path = "D:/emn33/Downloads/Images"
# tesseract_path = "C:/Program Files/Tesseract-OCR//tesseract.exe"

#--------------------------------------------------------------------------------------------------------
# Start of the class:
#--------------------------------------------------------------------------------------------------------
class Image_To_Text_Extractor:
    
    #--------------------------------------------------------------------------------------------------------
    # Constructor:
    # Everything in here will run once the class has been called / invoke / instantiate.
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, file_type, isbn_format, output_path, image_path, tesseract_path) -> None:
        self.file_type = file_type
        self.isbn_format = isbn_format
        self.output_path = output_path
        self.image_path = image_path
        self.tesseract_path = tesseract_path
        
        #----------------------------------------------------------------------------------------------------
        # Class Initialization and Tesseract Path Initialization:
        #----------------------------------------------------------------------------------------------------
        self.barcode_detector = cv2.barcode.BarcodeDetector()
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
        
        #----------------------------------------------------------------------------------------------------
        # Storing values to its respective variables:
        #----------------------------------------------------------------------------------------------------
        self.isbn_failed_path, self.barcode_failed_path = self.failed_folder_validator_creator()
        self.isbn = self.isbn_selector()
        self.my_config = r"-c tessedit_char_whitelist=0123456789xX-,.:;=_&^%$#@!`~{}[]()\/?+* --oem 1"
        self.image_list = self.image_file_list()
        self.movies_df = self.movies_empty_dataframe()
        
        #----------------------------------------------------------------------------------------------------
        # Finally, running the loop function:
        #----------------------------------------------------------------------------------------------------
        self.image_list_looping()
        
    #----------------------------------------------------------------------------------------------------
    # Gathering all the images in a list. Returns the final list:
    #----------------------------------------------------------------------------------------------------
    def image_file_list(self) -> list:
        final_image_list = []
        self.image_file_type = [".JPG", ".JPEG"]
        
        for per_type in self.image_file_type:
            handler = glob(f"{self.image_path}/*{str(per_type)}")
            final_image_list.extend(handler)
        
        print(f"Found a total of {len(final_image_list)} images to the selected folder.\n")
        return final_image_list
    
    #----------------------------------------------------------------------------------------------------
    # Creating an empty Dataframe with the required columns:
    #----------------------------------------------------------------------------------------------------
    def movies_empty_dataframe(self) -> pd.DataFrame:
        movies = pd.DataFrame()
        movies["File Name:"] = []
        movies["ISBN:"] = []
        movies["12-Digit UPC:"] = []
        
        return movies
    
    #----------------------------------------------------------------------------------------------------
    # Insert the values to the dataframe:
    #----------------------------------------------------------------------------------------------------
    def insert_to_movies_df(self, movie_name, movie_isbn, movie_barcode):
        new_row = {"File Name:" : movie_name, "ISBN:" : movie_isbn, "12-Digit UPC:" : movie_barcode}
        new_row_df = pd.DataFrame([new_row])
        self.movies_df = pd.concat([self.movies_df, new_row_df], ignore_index=True)
    
    #----------------------------------------------------------------------------------------------------
    # ISBN Pattern selector based on User's Choice:
    #----------------------------------------------------------------------------------------------------
    def isbn_selector(self):
        selected_isbn_format = None
        
        match(self.isbn_format):
            case 0:
                selected_isbn_format = r"\d{1}[^a-zA-Z0-9\n]{1}\d{1}[^a-zA-Z0-9\n]{1}\d{7}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{1}[^a-zA-Z0-9\n]{1}\d{2}[^a-zA-Z0-9\n]{1}\d{6}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{1}[^a-zA-Z0-9\n]{1}\d{3}[^a-zA-Z0-9\n]{1}\d{5}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{1}[^a-zA-Z0-9\n]{1}\d{4}[^a-zA-Z0-9\n]{1}\d{4}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{1}[^a-zA-Z0-9\n]{1}\d{5}[^a-zA-Z0-9\n]{1}\d{3}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{1}[^a-zA-Z0-9\n]{1}\d{6}[^a-zA-Z0-9\n]{1}\d{2}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{1}[^a-zA-Z0-9\n]{1}\d{7}[^a-zA-Z0-9\n]{1}\d{1}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}"
            case 1:
                selected_isbn_format = r"\d{2}[^a-zA-Z0-9\n]{1}\d{1}[^a-zA-Z0-9\n]{1}\d{6}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{2}[^a-zA-Z0-9\n]{1}\d{2}[^a-zA-Z0-9\n]{1}\d{5}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{2}[^a-zA-Z0-9\n]{1}\d{3}[^a-zA-Z0-9\n]{1}\d{4}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{2}[^a-zA-Z0-9\n]{1}\d{4}[^a-zA-Z0-9\n]{1}\d{3}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{2}[^a-zA-Z0-9\n]{1}\d{5}[^a-zA-Z0-9\n]{1}\d{2}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{2}[^a-zA-Z0-9\n]{1}\d{6}[^a-zA-Z0-9\n]{1}\d{1}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}"
            case 2:
                selected_isbn_format = r"\d{3}[^a-zA-Z0-9\n]{1}\d{1}[^a-zA-Z0-9\n]{1}\d{5}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{3}[^a-zA-Z0-9\n]{1}\d{2}[^a-zA-Z0-9\n]{1}\d{4}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{3}[^a-zA-Z0-9\n]{1}\d{3}[^a-zA-Z0-9\n]{1}\d{3}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{3}[^a-zA-Z0-9\n]{1}\d{4}[^a-zA-Z0-9\n]{1}\d{2}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{3}[^a-zA-Z0-9\n]{1}\d{5}[^a-zA-Z0-9\n]{1}\d{1}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}"
            case 3:
                selected_isbn_format = r"\d{4}[^a-zA-Z0-9\n]{1}\d{1}[^a-zA-Z0-9\n]{1}\d{4}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{4}[^a-zA-Z0-9\n]{1}\d{2}[^a-zA-Z0-9\n]{1}\d{3}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{4}[^a-zA-Z0-9\n]{1}\d{3}[^a-zA-Z0-9\n]{1}\d{2}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{4}[^a-zA-Z0-9\n]{1}\d{4}[^a-zA-Z0-9\n]{1}\d{1}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}"
            case 4:
                selected_isbn_format = r"\d{5}[^a-zA-Z0-9\n]{1}\d{1}[^a-zA-Z0-9\n]{1}\d{3}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{5}[^a-zA-Z0-9\n]{1}\d{2}[^a-zA-Z0-9\n]{1}\d{2}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}|\d{5}[^a-zA-Z0-9\n]{1}\d{3}[^a-zA-Z0-9\n]{1}\d{1}[^a-zA-Z0-9\n]{1}[0-9a-zA-Z]{1}"
        
        return selected_isbn_format
    
    #----------------------------------------------------------------------------------------------------
    # DateTime formatter used for naming the output file so that there will be no same file name:
    #----------------------------------------------------------------------------------------------------
    def datetime_formatter(self) -> str:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("-%Y%m%d-%H%M%S")
        
        return formatted_datetime
    
    #----------------------------------------------------------------------------------------------------
    # Output file base on the user's choice: This is where the output (Excel / CSV) file will be stored. 
    # This function also opens the folder afterwards. Call this function after the for loop function.
    #----------------------------------------------------------------------------------------------------
    def file_type_output_path(self) -> None:
        datetime_string = self.datetime_formatter()
        
        if self.file_type == 0:
            self.movies_df.to_excel(f"{self.output_path}/movies{datetime_string}.xlsx", index = False)
            os.startfile(self.output_path)
        else:
            self.movies_df.to_csv(f"{self.output_path}/movies{datetime_string}.csv", index = False)
            os.startfile(self.output_path)
    
    #----------------------------------------------------------------------------------------------------
    # Method that checks if a "Failed" folder already exist within the designated output folder. 
    # Creates the folder if it doesn't exist yet.
    #----------------------------------------------------------------------------------------------------
    def failed_folder_validator_creator(self) -> str:
        isbn_failed_folder_path = f"{self.output_path}/Failed-ISBN"
        barcode_failed_folder_path = f"{self.output_path}/Failed-Barcode"
        
        if glob(isbn_failed_folder_path):
            pass
        else:
            os.mkdir(isbn_failed_folder_path)
        
        if glob(barcode_failed_folder_path):
            pass
        else:
            os.mkdir(barcode_failed_folder_path)
        
        return isbn_failed_folder_path, barcode_failed_folder_path
    
    #----------------------------------------------------------------------------------------------------
    # Method that copies the failed image to the "Failed-ISBN" folder. 
    #----------------------------------------------------------------------------------------------------
    def failed_isbn_copier(self, image) -> None:
        image_path_split = image.split("\\")
        image_path = f"{str(image_path_split[0])}/{str(image_path_split[1])}"
        
        print(Fore.RED, "Did not found any match. The file will be copied to the failed folder inside the output folder.\n")
        sl.copy2(image_path, self.isbn_failed_path)
    
    #----------------------------------------------------------------------------------------------------
    # Method that copies the failed image to the "Failed-Barcode" Folder:
    #----------------------------------------------------------------------------------------------------
    def failed_barcode_copier(self, image):
        image_path_split = image.split("\\")
        image_path = f"{str(image_path_split[0])}/{str(image_path_split[1])}"
        
        sl.copy2(image_path, self.barcode_failed_path)
    
    #----------------------------------------------------------------------------------------------------
    # File name extraction:
    #----------------------------------------------------------------------------------------------------
    def file_name_extraction(self, per_image) -> str:
        self.image_file_type.extend([".jpg", ".jpeg"])
        
        image_file_name_split = per_image.split("\\")
        image_file_name = str(image_file_name_split[1])
        
        for per_type in self.image_file_type:
            if per_type in image_file_name:
                movie_split = image_file_name.split(per_type)
                movie_name = str(movie_split[0])
                return movie_name
    
    #----------------------------------------------------------------------------------------------------
    # Barcode reader:
    #----------------------------------------------------------------------------------------------------
    def barcode_reader(self, per_image) -> str:
        upc_digits = ""
        
        image_barcode = cv2.imread(per_image)
        retval, _, _= self.barcode_detector.detectAndDecode(image_barcode)
        
        if retval == "":
            self.failed_barcode_copier(per_image)
            upc_digits = "Did not found"
            return upc_digits
        else:
            per_barcode = list(retval)
            per_barcode.insert(6, " ")
            per_barcode.insert(1, " ")
            per_barcode.insert(-1, " ")
            upc_digits = "".join(per_barcode)
            return upc_digits
    
    #----------------------------------------------------------------------------------------------------
    # Method that converts the total time it takes for the program to finished the task to a formatted 
    # way: Days, Hours, Minutes, Seconds.
    #----------------------------------------------------------------------------------------------------
    def total_time_formatter(self, total_time):
        left_time = 0
        
        days = 0
        hours = 0
        minutes = 0
        seconds = 0
        
        if total_time >= 86400:
            days = total_time // 86400
            left_time = total_time % 86400
        else:
            days = 0
            left_time = total_time
        
        if left_time >= 3600:
            hours = left_time // 3600
            left_time = left_time % 3600
        else:
            hours = 0
        
        if left_time >= 60:
            minutes = left_time // 60
            left_time = left_time % 60
        else:
            minutes = 0
        
        if left_time >= 1:
            seconds = left_time
        else:
            seconds = 0
        
        total_time_statement = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds"
        return total_time_statement
    
    #----------------------------------------------------------------------------------------------------
    # Method for exiting the app after the job has been done. "Press any key to exit". Waits for the user 
    # to press any key then exit the program. Will be using this at the end of the program to properly 
    # display the summary of the program:
    #----------------------------------------------------------------------------------------------------
    def press_key_exit(self):
        key_input = False

        print("Please press any key to exit...")

        while key_input is False:
            k = readkey()
            if k is not None:
                key_input = True

        sys.exit(0)
    
    #----------------------------------------------------------------------------------------------------
    # Image Cropper. -> This crops the current image in the for loop into 72 sections / crop images. This 
    # function returns the crop images as a list that will be used to a loop to scan using Tesseract with 
    # different variations on how to scan for a text in the image.
    #----------------------------------------------------------------------------------------------------
    def per_image_cropper(self, image) -> list:
        img = cv2.imread(image)
        image_180 = cv2.rotate(img, cv2.ROTATE_180)
        image_crop_list = []
        
        max_height, max_width, _ = img.shape

        desired_height = max_height // 6
        desired_width = max_width // 2

        height_variations = (1, 1.5, 2, 2.5)
        width_variations = (1, 1.5, 2)
        
        for x in height_variations:
            for y in width_variations:
                if x == 1 and y == 1:
                    image_top = img[ : desired_height, : desired_width]
                    image_bottom_180 = image_180[ : desired_height, : desired_width]
                    
                elif x == 1 and y == 2:
                    new_start_width = int(desired_width * (y - 1))
                    
                    image_top = img[ : desired_height, new_start_width : max_width]
                    image_bottom_180 = image_180[ : desired_height, new_start_width : max_width]
                    
                elif x != 1 and y == 2:
                    new_start_height = int(desired_height * (x - 1))
                    new_start_width = int(desired_width * (y - 1))
                    new_end_height = int(desired_height * x)
                    
                    image_top = img[new_start_height : new_end_height, new_start_width : max_width]
                    image_bottom_180 = image_180[new_start_height : new_end_height, new_start_width : max_width]
                    
                elif x == 1 and y != 1:
                    new_start_width = int(desired_width * (y - 1))
                    new_end_width = int(desired_width * y)
                    
                    image_top = img[ : desired_height, new_start_width : new_end_width]
                    image_bottom_180 = image_180[ : desired_height, new_start_width : new_end_width]
                    
                elif x != 1 and y == 1:
                    new_start_height = int(desired_height * (x - 1))
                    new_end_height = int(desired_height * x)
                    
                    image_top = img[new_start_height : new_end_height, : desired_width]
                    image_bottom_180 = image_180[new_start_height : new_end_height, : desired_width]
                    
                else:
                    new_start_height = int(desired_height * (x - 1))
                    new_start_width = int(desired_width * (y - 1))
                    new_end_height = int(desired_height * x)
                    new_end_width = int(desired_width * y)
                    
                    image_top = img[new_start_height : new_end_height, new_start_width : new_end_width]
                    image_bottom_180 = image_180[new_start_height : new_end_height, new_start_width : new_end_width]
                
                image_bottom = cv2.rotate(image_bottom_180, cv2.ROTATE_180)
                image_top_90_cw = cv2.rotate(image_top, cv2.ROTATE_90_CLOCKWISE)
                image_top_90_ccw = cv2.rotate(image_top, cv2.ROTATE_90_COUNTERCLOCKWISE)
                image_bottom_90_cw = cv2.rotate(image_bottom, cv2.ROTATE_90_CLOCKWISE)
                image_bottom_90_ccw = cv2.rotate(image_bottom, cv2.ROTATE_90_COUNTERCLOCKWISE)
                
                image_crop_list.extend([image_top, image_bottom, image_top_90_cw, image_top_90_ccw, image_bottom_90_cw, image_bottom_90_ccw])
    
        return image_crop_list
        
    #----------------------------------------------------------------------------------------------------
    # The following methods are Tesseract with different methods for scanning the text to an image:
    #----------------------------------------------------------------------------------------------------
    def tesseract_default(self, image):
        matched_pattern = None
        
        texts_default = pytesseract.image_to_string(image=image, lang="eng", config=self.my_config)
        matched_default = re.findall(self.isbn, texts_default)
        if matched_default:
            handler = "//".join(matched_default)
            matched_pattern = self.isbn_formatter(handler)
            return matched_pattern
        
        if matched_pattern is None:
            return matched_pattern
    
    def tesseract_with_filters(self, image):
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_noise_reduc = cv2.medianBlur(image_gray, 1)
        image_sharp = cv2.filter2D(image_noise_reduc, -1, np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]))
        
        matched_pattern = None
        
        matched_pattern = self.tesseract_default(image=image_gray)
        if matched_pattern is not None:
            return matched_pattern
        
        matched_pattern = self.tesseract_default(image=image_noise_reduc)
        if matched_pattern is not None:
            return matched_pattern
        
        matched_pattern = self.tesseract_default(image=image_sharp)
        if matched_pattern is not None:
            return matched_pattern
        
        if matched_pattern is None:
            return matched_pattern
    
    def tesseract_contours(self, image):
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, threshold1 = cv2.threshold(image_gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 
        dilation = cv2.dilate(threshold1, rect_kernel, iterations = 1)
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        im2 = image.copy()
        
        text_list = []
        matched_pattern = None
        
        # First loop for default Tesseract.
        for per_contour in contours:
            
            x, y, w, h = cv2.boundingRect(per_contour)
            
            _ = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            cropped = im2[y:y + h, x:x + w]
            
            text = pytesseract.image_to_string(image=cropped, lang="eng", config=self.my_config)
            text_list.append(text)
        
        texts = "".join(text_list)
        matched_default = re.findall(self.isbn, texts)
        if matched_default:
            handler = "//".join(matched_default)
            matched_pattern = self.isbn_formatter(handler)
            return matched_pattern
        
        # Finally, if contours didn't work, will return an empty value.
        if matched_pattern is None:
            return matched_pattern
    
    #----------------------------------------------------------------------------------------------------
    # Found ISBN Formatter: This is needed since not all detected / found ISBN values are formatted in 
    # the correct way.
    #----------------------------------------------------------------------------------------------------
    def isbn_formatter(self, isbn_value) -> str:
        isbn_value_list = list(isbn_value)
        new_isbn_value_list = []
        
        for per_value in isbn_value_list:
            if per_value.isdigit() or per_value.isalpha():
                new_isbn_value_list.append(per_value)
            else:
                new_isbn_value_list.append("-")
        
        formatted_isbn_value = "".join(new_isbn_value_list)
        return formatted_isbn_value
    
    #----------------------------------------------------------------------------------------------------
    # This method calls the image cropper function to create a list containing crops (different parts) 
    # of the original image resulting to smaller field to scan IF the first Tesseract (Tesseract scans 
    # the whole image) didn't found a match:
    #----------------------------------------------------------------------------------------------------
    def image_cropper_looping(self, per_image):
        print("Cropping the current image to different parts.")
        image_cropped_list = self.per_image_cropper(per_image)
        print(f"Looping through {len(image_cropped_list)} cropped images.\n")
        
        matched_pattern = None
        cropped_cout = 1
        with trange(len(image_cropped_list), desc="Scanning cropped image #", bar_format="|{bar}| {desc} {n_fmt} of {total_fmt}", leave=False) as t:    
            for per_cropped in image_cropped_list:
                
                matched_pattern = self.tesseract_default(image=per_cropped)
                if matched_pattern is not None:
                    print(Fore.GREEN, "\nFound a match!\n")
                    return matched_pattern
                
                matched_pattern = self.tesseract_with_filters(image=per_cropped)
                if matched_pattern is not None:
                    print(Fore.GREEN, "\nFound a match using a filtered image!\n")
                    return matched_pattern
                
                matched_pattern = self.tesseract_contours(image=per_cropped)
                if matched_pattern is not None:
                    print(Fore.GREEN, "\nFound a match using a contoured image!\n")
                    return matched_pattern
                
                cropped_cout += 1
                t.update()
        
        if matched_pattern is None:
            self.failed_isbn_copier(image=per_image)
        
    #----------------------------------------------------------------------------------------------------
    # Loop method for the image list. Will call multiple functions here base on what is the current
    # task (File name extraction, Barcode Reader, ISBN extraction):
    #----------------------------------------------------------------------------------------------------
    def image_list_looping(self) -> None:
        whole_image_count = 1 # Will be use to display the current count of the image in the loop.
        failed_isbn_count = 0 # A counter for failed isbn extraction
        failed_barcode_count = 0 # A counter for failed barcode extraction
        
        #----------------------------------------------------------------------------------------------------
        # Starts a timer.
        #----------------------------------------------------------------------------------------------------
        start_time = time.time()
        
        for per_image in self.image_list:
            print(f"Image #{whole_image_count} of {len(self.image_list)}")
            
            #----------------------------------------------------------------------------------------------------
            # Extracts the File name:
            #----------------------------------------------------------------------------------------------------
            current_movie_name = self.file_name_extraction(per_image=per_image)
            print(f"File name: {current_movie_name}\n")
            
            #----------------------------------------------------------------------------------------------------
            # Read the barcode. If failed, set the variable value to "Did not found", copy the file to the failed 
            # folder, and increment the failed barcode counter:
            #----------------------------------------------------------------------------------------------------
            current_movie_barcode = self.barcode_reader(per_image=per_image)
            if current_movie_barcode == "Did not found":
                failed_barcode_count += 1
            
            #----------------------------------------------------------------------------------------------------
            # Try to extract the ISBN -> Scans the whole image first. If successfull, insert to the dataframe. If 
            # not, throw to another method where it crops the current image to a total of 72 images. Those 72 
            # images then will be loop through with another method applied such as applying filters and contours.
            #----------------------------------------------------------------------------------------------------
            current_movie_isbn = self.tesseract_default(image=per_image)
            
            if current_movie_isbn is not None:
                print(Fore.GREEN, "Found a match using the whole image!")
                print("Inserting values to the Dataframe.\n")
                print("--------------------------------------------------------", Fore.RESET)
                self.insert_to_movies_df(current_movie_name, current_movie_isbn, current_movie_barcode)
            else:
                print("Did not found the ISBN using the whole image.")
                current_movie_isbn = self.image_cropper_looping(per_image=per_image)
                
                if current_movie_isbn is not None:
                    print("Inserting values to the Dataframe.\n")
                    print("--------------------------------------------------------", Fore.RESET)
                    self.insert_to_movies_df(current_movie_name, current_movie_isbn, current_movie_barcode)
                else:
                    current_movie_isbn = "Did not found"
                    print("Inserting values to the Dataframe with missing ISBN.\n")
                    print("--------------------------------------------------------", Fore.RESET)
                    self.insert_to_movies_df(current_movie_name, current_movie_isbn, current_movie_barcode)
                    failed_isbn_count += 1 # Increments the failed isbn counter
            
            whole_image_count += 1 # Increments the image counter.
        
        #----------------------------------------------------------------------------------------------------
        # End the timer once the looping has finished. Converts it to a format: 
        # Days, Hours, Minutes, Seconds.
        #----------------------------------------------------------------------------------------------------
        total_time = round(time.time() - start_time, 2)
        total_time_statement = self.total_time_formatter(total_time)
        
        #----------------------------------------------------------------------------------------------------
        # Clears the CLI. Calls the press_key_exit to prints a summary persistently and open the output folder.
        #----------------------------------------------------------------------------------------------------
        os.system("cls")
        print(f"Program has finished scanning all the images in the selected folder.\nNumber of scanned images: {len(self.image_list)}\nNumber of failures:\n\tISBN: {failed_isbn_count}\n\tBarcode: {failed_barcode_count}\n")
        print(f"The program took {total_time_statement} to finished.\n")
        self.file_type_output_path()
        self.press_key_exit()
        
if __name__ == "__main__":
    # Image_To_Text_Extractor(file_type, isbn_format, output_path, image_path, tesseract_path)
    Image_To_Text_Extractor()