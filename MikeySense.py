#!/usr/bin/python3
# coding: Latin-1
"""
Mikey Sense
Like Spidey Senses, but with a pi
"""
import os
import time
from configparser    import SafeConfigParser
from multiprocessing import Process, Value
from sense_hat       import SenseHat
from Classes.MikeySenseClock import MikeySenseClock

def blank_grid():
	""" Returns a blank grid """
	blank = [0, 0, 0]
	return [
		blank, blank, blank, blank, blank, blank, blank, blank,
		blank, blank, blank, blank, blank, blank, blank, blank,
		blank, blank, blank, blank, blank, blank, blank, blank,
		blank, blank, blank, blank, blank, blank, blank, blank,
		blank, blank, blank, blank, blank, blank, blank, blank,
		blank, blank, blank, blank, blank, blank, blank, blank,
		blank, blank, blank, blank, blank, blank, blank, blank,
		blank, blank, blank, blank, blank, blank, blank, blank
	]

def unknown_grid():
	""" Returns a large '?' """
	return fill_blocks(blank_grid(), [11, 12, 18, 21, 29, 36, 44, 60])

def cpu_temperature():
	""" Return the CPU temp as a float """
	result = os.popen("vcgencmd measure_temp").readline()
	return float(result.replace("temp=","").replace("'C\n",""))

def generate_filepath(path):
	""" Generates a direct path to files in this directory """
	return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

def main():
	""" Runs when run """
	# Set the sense class up
	sense = SenseHat()
	sense.low_light = True
	sense.clear()
	# Say hello
	say_hello(sense)
	# Start the getting and outputing daemons
	try:
		sense_values = Value("i", 0)
		get_sense_vars_process = Process(target=get_sense_vars, args=(sense, sense_values))
		output_process         = Process(target=output,         args=(sense, sense_values))
		get_sense_vars_process.daemon = True
		output_process.daemon      = True
		get_sense_vars_process.start()
		output_process.start()
		get_sense_vars_process.join()
		output_process.join()
	except KeyboardInterrupt:
		print("Cancelled")
	print("Program Finished")
	sense.clear()

def say_hello(sense):
	""" Says hello, and shows a smiley face """
	sense.show_message("Hello")
	sense.set_rotation(90)
	sense.show_message(":)")
	sense.set_rotation(0)

def read_config():
	""" Reads the config file """
	parser = SafeConfigParser()
	config = {}
	parser.read(generate_filepath("MikeySense.ini"))
	# pyowm stuff
	config["pyowm_api_key"]  = parser.get("pyowm", "apiKey")
	config["pyowm_location"] = parser.get("pyowm", "location")

def output(sense, sense_values):
	""" Outputs what needs to be output """
	# Sets what each 'page' does
	sense_page  = "time"
	sense_pages = {
		"left":   "weather",
		"right":  "blank",
		"up":     "time",
		"down":   "temperature",
		"middle": "????"
	}
	# Set the clock up
	clock = MikeySenseClock()
	# Show the pages
	try:
		while True:
			for event in sense.stick.get_events():
				# If the page exists for this direction, change to it
				if event.direction in sense_pages and sense_page != sense_pages[event.direction]:
					sense_page = sense_pages[event.direction]
					sense.show_message(sense_page.capitalize(), 0.05)
			# Output the correct page
			if sense_page == "weather":
				sense.set_pixels(unknown_grid())
			elif sense_page == "time":
				clock.reset_time()
				sense.set_pixels(clock.output_clock())
			elif sense_page == "temperature":
				output_num(sense, sense_values.value)
			elif sense_page == "blank":
				sense.clear()
			else:
				sense.set_pixels(unknown_grid())
	except KeyboardInterrupt:
		sense.clear()
	sense.clear()

def get_sense_vars(sense, sense_values):
	""" Sets the temperature every 5 seconds """
	try:
		while True:
			# Get the temp
			temperature = sense.get_temperature()
			# Calibrate the temperature
			cpu_temp = cpu_temperature()
			temperature = int(temperature - ((cpu_temp - temperature)/5.466))
			# set the temperature
			sense_values.value = temperature
			time.sleep(10)
	except KeyboardInterrupt:
		print("cancelled")

def output_num(sense, num):
	""" Outputs a number, scrolling if -100 <= x >= 100, otherwise outputting it normally """
	# sense.clear()
	if num >= 100 or num <= -100:
		sense.show_message(str(num))
	else:
		sense.set_pixels(draw_num(num))

def draw_num(num):
	""" Outputs a number which is 10 >= x < 100 """
	result = unknown_grid()
	# if num is valid, output it
	if isinstance(num, int):
		result = blank_grid()
		# If negative, draw the '-', and then make it positive
		if num < 0:
			result = fill_blocks(result, [24], [255, 0, 0])
			num = num * -1
		# Draw the actual number
		if num >= 10:
			# Draw the tens
			result = draw_tens(result, int(str(num)[0]))
			# And the units
			result = draw_units(result, int(str(num)[1]))
		elif num < 10 and num >= 0:
			# Draw just the units
			result = draw_units(result, num)
	return result

def fill_blocks(blocks, nums, colour = [255, 255, 255]):
	""" Fills the provided blocks """
	for num in nums:
		blocks[num] = colour
	return blocks

def draw_tens(light_grid, digit):
	""" Outputs the tens of the number """
	if isinstance(digit, int) and digit > 0 and digit < 10:
		if digit == 1:
			light_grid = fill_blocks(light_grid, [10, 17, 18, 26, 34, 42, 49, 50, 51])
		elif digit == 2:
			light_grid = fill_blocks(light_grid, [10, 17, 19, 27, 34, 41, 49, 50, 51])
		elif digit == 3:
			light_grid = fill_blocks(light_grid, [9, 10, 19, 25, 26, 35, 43, 49, 50])
		elif digit == 4:
			light_grid = fill_blocks(light_grid, [11, 18, 19, 25, 27, 33, 34, 35, 43, 51])
		elif digit == 5:
			light_grid = fill_blocks(light_grid, [9, 10, 11, 17, 25, 26, 35, 43, 49, 50])
		elif digit == 6:
			light_grid = fill_blocks(light_grid, [11, 10, 17, 25, 33, 41, 50, 43, 35, 26])
		elif digit == 7:
			light_grid = fill_blocks(light_grid, [9, 10, 11, 19, 27, 34, 42, 49])
		elif digit == 8:
			light_grid = fill_blocks(light_grid, [10, 17, 19, 26, 33, 35, 41, 43, 50])
		elif digit == 9:
			light_grid = fill_blocks(light_grid, [10, 11, 17, 19, 25, 27, 34, 35, 43, 51])
	return light_grid

def draw_units(light_grid, digit):
	""" Outputs the digit of the number """
	if isinstance(digit, int) and digit >= 0 and digit < 10:
		if digit == 0:
			light_grid = fill_blocks(light_grid, [14, 21, 23, 29, 31, 37, 39, 45, 47, 54])
		elif digit == 1:
			light_grid = fill_blocks(light_grid, [14, 21, 22, 30, 38, 46, 53, 54, 55])
		elif digit == 2:
			light_grid = fill_blocks(light_grid, [14, 21, 23, 31, 38, 45, 53, 54, 55])
		elif digit == 3:
			light_grid = fill_blocks(light_grid, [13, 14, 23, 29, 30, 39, 47, 53, 54])
		elif digit == 4:
			light_grid = fill_blocks(light_grid, [15, 22, 23, 29, 31, 37, 38, 39, 47, 55])
		elif digit == 5:
			light_grid = fill_blocks(light_grid, [13, 14, 15, 21, 29, 30, 39, 47, 53, 54])
		elif digit == 6:
			light_grid = fill_blocks(light_grid, [15, 14, 21, 29, 37, 45, 54, 47, 39, 30])
		elif digit == 7:
			light_grid = fill_blocks(light_grid, [13, 14, 15, 23, 31, 38, 46, 53])
		elif digit == 8:
			light_grid = fill_blocks(light_grid, [14, 21, 23, 30, 37, 39, 45, 47, 54])
		elif digit == 9:
			light_grid = fill_blocks(light_grid, [14, 15, 21, 23, 29, 31, 38, 39, 47, 55])
	return light_grid

if __name__ == "__main__":
	main()
