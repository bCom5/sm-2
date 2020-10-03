import json
import sys
import math

def import_items(file_path):
	return json.loads(open(file_path).read())

def export_items(items, file_path):
	open(file_path, "w").write(json.dumps(items, indent=4))
	return True

def get_next_i_interval(item, reset=False):
	"""Get next inter-repetition interval after the n-th repetition"""
	if reset:
		item["i-interval"] = 1
	else:
		last_i_interval = item.get('i-interval', None)
		if last_i_interval:
			if last_i_interval > 2:
				item["i-interval"] = math.ceil(last_i_interval * item["e-factor"])
			item["i-interval"] = 6
		item["i-interval"] = 1
	return item

def get_quality_of_repetition():
	prompt = "\nPlease enter the number that corresponds with your answer\n" + \
			"5 - perfect response\n" + \
			"4 - correct response after a hesitation\n" + \
			"3 - correct response recalled with serious difficulty\n" + \
			"2 - incorrect response; where the correct one seemed easy to recall\n" + \
			"1 - incorrect response; the correct one remembered\n" + \
			"0 - complete blackout.\n\n"
	while (1):
		q = input(prompt)
		if int(q) or int(q) == 0:
			return int(q)

def change_e_factor(item, q):
	if q < 3:
		get_next_i_interval(item, reset=True)
	if item["e-factor"] >= 1.3:
		item["e-factor"] = item["e-factor"]+(0.1-(5-q)*(0.08+(5-q)*0.02))
	return item

def check_if_init_format(items):
	for k in items.keys():
		item = items[k]
		if not item.get("e-factor", None): 
			item["e-factor"] = 2.5
			items[k]=item
	return items

def main(argv):
	file_path = argv[0]
	items = import_items(file_path)
	items = check_if_init_format(items)
	export_items(items, file_path)
	for k in items.keys():
		item = items[k]
		user_input = input("Question: " + item["question"] +"\nInput your answer: ")
		print("Correct answer: %s \n" % ( item["answer"] ))
		q = get_quality_of_repetition()
		item = change_e_factor(item, q)
		item = get_next_i_interval(item)
		items[k] = item
		export_items(items, file_path)


if __name__ == "__main__":
	main(sys.argv[1:])