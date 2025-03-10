import pyautogui
import time
import keyboard

# Define the coordinates of the number buttons on the phone screen
# Example format: 'number': (x, y)
number_coords = {
	'0': (2324, 1180),
	'1': (2228, 880),
	'2': (2328, 880),
	'3': (2426, 880),
	'4': (2228, 980),
	'5': (2328, 980),
	'6': (2426, 980),
	'7': (2228, 1080),
	'8': (2328, 1080),
	'9': (2426, 1080)
}

# Define the best 4-digit passcode options
best_passcodes = ['1234', '5678', '4321', '8765', '0000', '9999', '8888', '7777', '6666', '5555', '4444', '3333', '2222', '1111', '1256', '4589', '8585', '7878', '8989']

# Variable to control the running state of the program
program_running = True

print('5 sec delay to change windows')
time.sleep(5)

# Function to stop the program when F2 is pressed
def stop_program():
	global program_running
	print("Program stopped by user.")
	program_running = False

# Bind the F2 key to stop the program
keyboard.add_hotkey('F2', stop_program)

# Function to simulate clicking on a specific number
def click_number(number):
	x, y = number_coords[number]
	pyautogui.moveTo(x, y, duration=0.2)  # Smooth movement to the number
	pyautogui.click()
	time.sleep(0.1)  # Small delay between clicks

# Main loop to try all the best passcodes
try:
	for code in best_passcodes:
		if not program_running:
			break
		print(f"Trying passcode: {code}")
		for digit in code:
			click_number(digit)
		time.sleep(1)  # Wait before trying the next code
except KeyboardInterrupt:
	print("Program terminated manually.")

print("Program has exited.")
