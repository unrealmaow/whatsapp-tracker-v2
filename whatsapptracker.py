
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import math
import datetime
from discord_webhook import DiscordWebhook
import pyfiglet
import os


def send_discord_hook(hook_url, message_content):
	try:
		webhook = DiscordWebhook(url=hook_url, content=message_content)
		response = webhook.execute()
		return
	except Exception:
		return print(Exception)


def study_user(driver, user, language, contact_name, discord_webhook):
	# First, go to their chat
	try:
		contact = f'https://web.whatsapp.com/send?phone={str(user)}&text&app_absent=1'
		driver.get(contact)
	except Exception:
		print('{} is not found. Returning...'.format(user))
		return

	time.sleep(10)
	try:
		focus_xpath = str()
		focus_xpath = '//div[@title=\'{}\']'.format('Type a message')
		driver.find_element(By.XPATH, focus_xpath).click()
	except NoSuchElementException:
		return print(NoSuchElementException)

	x_arg = str()
	# Now, we continuously check for their online status:
	if language == 'en':
		x_arg = '//span[@title=\'{}\']'.format('online')
	elif language == 'es':
		x_arg = '//span[@title=\'{}\']'.format('en línea')
	print('Trying to find: {} in user {}'.format(x_arg, user))
	previous_state = 'OFFLINE' # by default, we consider the user to be offline. The first time the user goes online,
	first_online = time.time()
	cumulative_session_time = 0
	# it will be printed.
	while True:
		try:
			element = driver.find_element(By.XPATH, x_arg)
			if previous_state == 'OFFLINE':
				print('[{}][ONLINE] {}'.format(
					datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
					user))
				first_online = time.time()
				previous_state = 'ONLINE'
				now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				
				message = str()
				message = f'[{now_time}] [ONLINE] - [{user}][{contact_name}] is Online'

				send_discord_hook(discord_webhook, message)
		except NoSuchElementException:
			if previous_state == 'ONLINE':
			# calculate approximate real time of WhatsApp being online
				total_online_time = time.time() - first_online - 12 # approximately what it takes onPause to send signal
				if total_online_time < 0: # This means that the user was typing instead of going offline.
					continue # Skip the rest of this iteration. Do nothing.
				cumulative_session_time += total_online_time
				now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				print('[{}][DISCONNECTED] {} was online for {} seconds. Session total: {} seconds'.format(
					datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
					user,
					math.floor(total_online_time),
					math.floor(cumulative_session_time)))
				previous_state = 'OFFLINE'
				online_time_s = math.floor(total_online_time)
				message = str()
				message = f'[{now_time}] [Disconnected] - [{user}][{contact_name}] Was Online For {online_time_s} seconds.'
				
				send_discord_hook(discord_webhook, message)

		time.sleep(1)



def inf_sleep():
	while True:
		time.sleep(1)



def whatsapp_login():
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options=options)
	driver.get('https://web.whatsapp.com')
	assert 'WhatsApp' in driver.title 
	input('Scan the code and press any key...')
	print('QR scanned successfully!')
	return driver



def main():

	os.system("cls") #use this for windows. change to os.system("clear") for linux

	ascii_banner = pyfiglet.figlet_format("Whatsapp Logger By UnReal Maow")
	print(ascii_banner)

	
	discord_webhook = input('Enter Discord Hook URL: ')
	phone = input('Enter Phone with Country Code: ')
	contact_name = input('Enter Contact Name: ')
	language = 'en'

	print('Logging in...')
	print('Please, scan your QR code.')
	driver = whatsapp_login()
	study_user(driver, phone, language, contact_name, discord_webhook)



if __name__ == '__main__':
	main()
