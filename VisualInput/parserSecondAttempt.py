import numpy as np
import cv2
import pytesseract

# Function to write OCR results to a file


def write_to_file(file_path, data):
    with open(file_path, 'a') as file:
        file.write(data + '\n')


# Define the path for the output text file
output_file = 'output.txt'

fileName = './WineListImages/wineMenu1.png'

# Open the output file and clear any existing content
with open(output_file, 'w') as file:
    file.write('')

inputImage = cv2.imread(fileName)
grayImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
_, binaryImage = cv2.threshold(
    grayImage, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Calculate the horizontal projection by summing up the value of pixels along rows
horizontal_projection = np.sum(binaryImage, axis=1)

# Find where the lines start and end
height, width = binaryImage.shape
line_start = None
for y in range(height):
    if horizontal_projection[y] > 0 and line_start is None:
        line_start = y
    elif horizontal_projection[y] == 0 and line_start is not None:
        line_end = y
        # Extract the line
        line = binaryImage[line_start:line_end, :]

        # Run OCR on the extracted line
        text = pytesseract.image_to_string(line, config='--psm 7')
        print(text)

        # Write the OCR result to the output file
        write_to_file(output_file, text)

        # Draw a rectangle on the original image (not the binary one) to show the line being read
        line_highlighted = cv2.rectangle(
            np.copy(inputImage), (0, line_start), (width, line_end), (0, 255, 0), 2)

        # Show the highlighted line on the original image
        cv2.imshow('Line Highlighted', line_highlighted)

        # Wait for the 'a' key to be pressed to move to the next line
        while True:
            if cv2.waitKey(1) & 0xFF == ord('a'):
                break

        line_start = None

cv2.destroyAllWindows()
