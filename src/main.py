#--------------------------------------------------------------------------------------------------------
# Necesasry Imports:
#--------------------------------------------------------------------------------------------------------
from class_image_to_text_GUI import Image_to_Text_GUI as GUI
from class_image_to_text_extractor import Image_To_Text_Extractor as ITT

#--------------------------------------------------------------------------------------------------------
# Making an instace of the GUI Class, this will activate the GUI for the use. 
# Declaring a variable that will get the state of the proceed button and pass the necessary values to 
# their respective variables:
#--------------------------------------------------------------------------------------------------------
my_GUI = GUI()

btn_state = 0

while btn_state == 0:
    btn_state = my_GUI.button_state() # Calling the function to see if the proceed button has been pressed.
    if btn_state == 1:
        print("User has pressed the Proceed button. Running the program now.") # Just some kind of evidence that the button has been pressed.
        file_type, isbn_format, output_path, image_path, tesseract_path = my_GUI.variable_values() # Stores the necessary values to the variables.

#--------------------------------------------------------------------------------------------------------
# Passing the values to the other class which will start the process of extracting the barcodes and 
# ISBNs for each images:
#--------------------------------------------------------------------------------------------------------
my_extractor = ITT(file_type, isbn_format, output_path, image_path, tesseract_path)