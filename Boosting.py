import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageGrab

# Configure Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Administrador\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# List of 4-letter Portuguese words
words = [
	"casa", "vida", "amor", "pato", "gato", "rato", "copo", "lava", "roda", "sopa",
	"mesa", "piso", "nave", "foca", "mato", "bico", "lago", "boca", "polo", "vela",
	"limo", "doce", "bolo", "fogo", "sapo", "lixo", "arco", "fera", "fuga", "telo",
	"bala", "ruga", "aves", "leve", "fino", "muda", "liso", "tira", "lado", "duro",
	"rola", "jogo", "mapa", "selo", "bato", "lupa"
]

# Define the screen area to capture (example coordinates)
screen_area = (932, 623, 1625, 754)  # (left, top, right, bottom)

print("Iniciando o analisador de palavras...")

def get_square_color(img):
	# Open the image
	image = img

	# Assume the image is divided into 4 squares, for simplicity, define the boundaries (this should be adjusted for your image)
	height, width, _ = image.shape
	squares = [
		(0, 0, width // 4, height),  # Leftmost square
		(width // 4, 0, width // 2, height),  # Second square from the left
		(width // 2, 0, 3 * width // 4, height),  # Third square from the left
		(3 * width // 4, 0, width, height)  # Rightmost square
	]

	color_array = []

	# Define color ranges for green and yellow
	def is_green(color):
		r, g, b = color
		return g > r and g > b and (0, 70, 0) <= (r, g, b) <= (100, 255, 100)

	def is_yellow(color):
		r, g, b = color
		return r > g and r > b and (50, 50, 0) <= (r, g, b) <= (255, 255, 150)

	def is_orange(color):
		r, g, b = color
		return r > g and r > b and (20, 50, 70) <= (r, g, b) <= (180, 150, 50)

	# Process each square
	for square in squares:
		# Crop the square from the image
		cropped = img[square[1]:square[3], square[0]:square[2]]
		#cv2.imshow("Captura de Tela", cropped)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()

		# Calculate the bottom section's center pixel
		section_height = cropped.shape[0] // 4
		center_pixel = cropped[section_height * 3 + section_height // 2, cropped.shape[1] // 2]
		center_pixel[0], center_pixel[2] = center_pixel[2], center_pixel[0]
		#print(f'center_pixel: ', center_pixel) # prints the RGB colors of the squares

		# Determine the color
		if is_green(center_pixel):
			color_array.append("g")
		elif is_orange(center_pixel):
			color_array.append("y")
		else:
			color_array.append("_")

	return color_array


while True:
	screenshot = ImageGrab.grab(bbox=screen_area)
	img = np.array(screenshot)
	image = np.array(screenshot)
	# cv2.imshow("Captura de Tela", img)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction

	# Preprocess for better OCR accuracy
	_, roi_thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

	textGray = pytesseract.image_to_string(roi_thresh, config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ').strip()
	print(f'Gray Text: ', textGray)
	letters = [char.lower() for char in textGray if char.isalpha()]
	if len(letters) < 4:
		cv2.waitKey(100)
		continue

	#print(f'Letras detectadas: {letters}')
	# cv2.imshow("Captura de Tela", roi_thresh) # GRAY IMAGE

	# Convert the image from RGB (PIL default) to BGR (OpenCV format)
	img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

	# Convert the image to HSV
	hsv_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

	# Define the range for green color (in HSV space)
	lower_green = np.array([35, 40, 40])
	upper_green = np.array([85, 255, 255])

	# Define the range for yellow color (in HSV space)
	lower_yellow = np.array([20, 40, 40])
	upper_yellow = np.array([35, 255, 255])

	# Create masks for green and yellow
	green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
	yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

	# Combine the two masks
	combined_mask = cv2.bitwise_or(green_mask, yellow_mask)

	# Apply the mask to the original image
	result_image = cv2.bitwise_and(img_bgr, img_bgr, mask=combined_mask)

	# Convert the image to HSV for better color detection
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	#cv2.imshow("Captura de Tela", result_image)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	# Parse the colors of the letters
	# letter_colors = ['_' for _ in letters]  # _ means the letter is not in the word
	letter_colors = get_square_color(result_image)

	#print(f'Cores das letras: {letter_colors}')

	# Filter valid words based on the feedback
	valid_words = []
	for word in words:
		match = True
		for i, (letter, color) in enumerate(zip(letters, letter_colors)):
			if color == 'g' and word[i] != letter:
				match = False
				break
			if color == 'y' and (letter not in word or word[i] == letter):
				match = False
				break
			if color == '_' and letter in word:
				match = False
				break
		if match:
			valid_words.append(word)

	print(f'Palavras mais prováveis: {valid_words}')
	if cv2.waitKey(100) & 0xFF == ord('q'):
		break
	#break