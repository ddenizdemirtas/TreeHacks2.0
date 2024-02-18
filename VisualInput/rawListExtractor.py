import pytesseract as tess
from PIL import Image
tess.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'


def write_to_file(file_path, text_data):
    """
    Writes text data to a .txt file.

    Parameters:
    file_path (str): The path to the file where the text will be written.
    text_data (str): The text data to write to the file.
    """
    with open(file_path, 'w') as file:
        file.write(text_data)


def image_to_raw_text(image_loc):

    img = Image.open(image_loc)
    text = tess.image_to_string(img)

    return write_to_file('./EXAMPLETEXT.txt', text)


# print(image_to_raw_text('./WineListImages/wineMenu1.png'))
print(image_to_raw_text('./WineListImages/WineListExample.jpg'))
