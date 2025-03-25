import sys

def ask_for_total_bonus():
	while True:
		try:
			total_bonus = float(input("Enter the total bonus amount to distribute: "))
			if total_bonus <= 0:
				raise ValueError
			return total_bonus
		except ValueError:
			print("Please enter a valid positive number.")

def ask_for_worker_data():
	workers = []
	while True:
		input_data = input('Enter worker name and deliveries made (e.g., John 10) or type "done" to finish: ').strip()
		if input_data.lower() == "done":
			break
		try:
			name, deliveries = input_data.split()
			delivery_count = int(deliveries)
			if delivery_count < 0:
				raise ValueError
			workers.append({"name": name, "deliveries": delivery_count})
		except (ValueError, IndexError):
			print("Invalid input. Please use the format: Name Deliveries")
	return workers

def calculate_bonuses(total_bonus, workers):
	total_deliveries = sum(worker["deliveries"] for worker in workers)
	if total_deliveries == 0:
		print("No deliveries made. No bonuses to distribute.")
		return

	print("\nBonus Distribution:")
	for worker in workers:
		bonus = (worker["deliveries"] / total_deliveries) * total_bonus
		print(f"{worker['name']}: €{bonus:.2f}")

def main():
	total_bonus = ask_for_total_bonus()
	workers = ask_for_worker_data()
	calculate_bonuses(total_bonus, workers)

if __name__ == "__main__":
	main()
