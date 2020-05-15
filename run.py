import os
from selenium import webdriver
from dotenv import load_dotenv
from app.common.user_input import user_input
from app.common.load_file import load_file
from app.common.user_login import user_login
from app import SetupCreateFile
from app import SetupCheckUser

load_dotenv()


rs = user_input()
if rs['status'] == True:
	files = load_file()
	if files:
		# path = os.getcwd()+'app\assets\geckodriver.exe'
		path = 'app\\assets\\chromedriver.exe'
		# driver = webdriver.Firefox(executable_path=path)
		driver = webdriver.Chrome(path)
		driver.maximize_window()
		rs_log = user_login(driver, rs['username'], rs['password'])
		if rs_log == True:
			if rs['option'] == '1':
				setup = SetupCreateFile(files, driver, rs['panel'])
				setup.process_file()
			else:
				path_result = open('app\\assets\\result.json', "a+")
				setup = SetupCheckUser(driver, files, path_result, rs['date_bulk'])
				setup.check_file()
		else:
			print("Something wrong")
	else:
		print("Something wrong")
else:
	print("Something wrong")