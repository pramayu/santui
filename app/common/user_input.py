def user_input():
	rs 			= {'status': False}
	print("--Select option--")
	print("Input 1 for update service")
	print("-or-")
	print("Input 2 for check bulk status")
	print("--------------------------------")
	option 		= input("Option: ")
	if option == '1':
		print("--Select panel--")
		panel = input("Input panel 1 or 2: ")
	if option == '2':
		date_bulk = input("Input bulk date, exp: 18-Feb-2020: ")
		push_resl = open("app/assets/result.json", "a+")
	if option:
		rs = {
			'status'	: True,
			'option'	: option,
			'panel'		: panel if option == '1' else '',
			'date_bulk'	: date_bulk if option == '2' else '',
			'push_resl'	: push_resl if option == '2' else ''
		}
		return rs
	else:
		return rs