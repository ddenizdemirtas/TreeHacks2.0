import pytesseract as tess
from PIL import Image
from parsing import parse_wine_names, filter

tess.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
img = Image.open('4.png')
custom_config = r'--oem 3 --psm 6'
raw_text = tess.image_to_string(img, config=custom_config)

wine_names = filter(parse_wine_names(raw_text))
print(wine_names)