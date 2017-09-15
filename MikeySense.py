#!/usr/bin/python3
# coding: Latin-1
"""
Mikey Sense
Like Spidey Senses, but with a pi
"""
import time
from sense_hat import SenseHat

x = [255, 255, 255]
O = [0, 0, 0]
BLANK = [
	O, O, O, O, O, O, O, O,
	O, O, O, O, O, O, O, O,
	O, O, O, O, O, O, O, O,
	O, O, O, O, O, O, O, O,
	O, O, O, O, O, O, O, O,
	O, O, O, O, O, O, O, O,
	O, O, O, O, O, O, O, O,
	O, O, O, O, O, O, O, O
]
UNKNOWN = [
	O, O, O, x, x, O, O, O,
	O, O, x, O, O, x, O, O,
	O, O, O, O, O, x, O, O,
	O, O, O, O, x, O, O, O,
	O, O, O, x, O, O, O, O,
	O, O, O, x, O, O, O, O,
	O, O, O, O, O, O, O, O,
	O, O, O, x, O, O, O, O
]

def main():
	""" Runs when run """
	# Set the sense class up
	sense = SenseHat()
	sense.clear()
	# Say hello
	# say_hello(sense)
	# Show the temperature
	# show_temp(sense)

	output_num(sense, 10)

	time.sleep(5)
	sense.clear()

def say_hello(sense):
	""" Says hello, and shows a smiley face """
	sense.show_message("Hello")
	sense.set_rotation(90)
	sense.show_message(":)")
	sense.set_rotation(0)

def show_temp(sense):
	""" Shows the temperature """
	# Get the temp, and intify it
	temperature = int(sense.get_temperature())
	output_num(sense, temperature)

def output_num(sense, num):
	""" Outputs a number, scrolling if greater than 99, otherwise outputting it normally """
	sense.clear()
	if num >= 100:
		sense.show_message(str(num))
	elif num >= 10:
		sense.set_pixels(draw_num(num))
	else:
		sense.set_pixels(draw_digit(num))
	print(10)

def draw_digit(num):
	""" Outputs a number which is 0 >= x < 10 """
	result = UNKNOWN
	# If num is an int and less than 10, output it
	if isinstance(num, int) and num >= 0 and num < 10:
		#		-, X, X, X, X, -, X, 0
		if num == 0:
			result = [
				O, O, O, O, O, O, O, O,
				O, O, x, x, O, O, x, O,
				O, x, O, O, x, O, O, O,
				O, x, O, O, x, O, O, O,
				O, x, O, O, x, O, O, O,
				O, x, O, O, x, O, O, O,
				O, O, x, x, O, O, O, O,
				O, O, O, O, O, O, O, O
			]
		elif num == 1:
			result = [
				O, O, O, O, O, O, O, O,
				O, O, x, x, O, O, x, O,
				O, x, x, x, O, O, O, O,
				O, O, x, x, O, O, O, O,
				O, O, x, x, O, O, O, O,
				O, O, x, x, O, O, O, O,
				O, x, x, x, x, O, O, O,
				O, O, O, O, O, O, O, O
			]
		elif num == 2:
			result = [
				O, O, O, O, O, O, O, O,
				O, O, x, x, O, O, x, O,
				O, x, O, O, x, O, O, O,
				O, O, O, O, x, O, O, O,
				O, O, O, x, O, O, O, O,
				O, O, x, O, O, O, O, O,
				O, x, x, x, x, O, O, O,
				O, O, O, O, O, O, O, O
			]
		elif num == 3:
			result = [
				O, O, O, O, O, O, O, O,
				O, x, x, x, x, O, x, O,
				O, O, O, O, x, O, O, O,
				O, O, x, x, O, O, O, O,
				O, O, O, O, x, O, O, O,
				O, x, O, O, x, O, O, O,
				O, O, x, x, O, O, O, O,
				O, O, O, O, O, O, O, O
			]
		elif num == 4:
			result = [
				O, O, O, O, O, O, O, O,
				O, O, O, x, O, O, x, O,
				O, O, x, x, O, O, O, O,
				O, x, O, x, O, O, O, O,
				O, x, x, x, x, O, O, O,
				O, O, O, x, O, O, O, O,
				O, O, O, x, O, O, O, O,
				O, O, O, O, O, O, O, O
			]
		elif num == 5:
			result = [
				O, O, O, O, O, O, O, O,
				O, x, x, x, x, O, x, O,
				O, x, O, O, O, O, O, O,
				O, x, x, x, O, O, O, O,
				O, O, O, O, x, O, O, O,
				O, x, O, O, x, O, O, O,
				O, O, x, x, O, O, O, O,
				O, O, O, O, O, O, O, O
			]
		elif num == 6:
			result = [
				O, O, O, O, O, O, O, O,
				O, O, x, x, x, O, x, O,
				O, x, O, O, O, O, O, O,
				O, x, x, x, O, O, O, O,
				O, x, O, O, x, O, O, O,
				O, x, O, O, x, O, O, O,
				O, O, x, x, O, O, O, O,
				O, O, O, O, O, O, O, O
			]
		elif num == 7:
			result = [
				O, O, O, O, O, O, O, O,
				O, x, x, x, x, O, x, O,
				O, O, O, O, x, O, O, O,
				O, O, O, O, x, O, O, O,
				O, O, O, x, O, O, O, O,
				O, O, x, O, O, O, O, O,
				O, x, O, O, O, O, O, O,
				O, O, O, O, O, O, O, O
			]
		elif num == 8:
			result = [
				O, O, O, O, O, O, O, O,
				O, O, x, x, O, O, x, O,
				O, x, O, O, x, O, O, O,
				O, O, x, x, O, O, O, O,
				O, x, O, O, x, O, O, O,
				O, x, O, O, x, O, O, O,
				O, O, x, x, O, O, O, O,
				O, O, O, O, O, O, O, O
			]
		elif num == 9:
			result = [
				O, O, O, O, O, O, O, O,
				O, O, x, x, O, O, x, O,
				O, x, O, O, x, O, O, O,
				O, x, O, O, x, O, O, O,
				O, O, x, x, x, O, O, O,
				O, O, O, O, x, O, O, O,
				O, O, O, O, x, O, O, O,
				O, O, O, O, O, O, O, O
			]
	# Returns UNKNOWN if num isn't valid
	return result

def draw_negative_digit(num):
	""" Outputs a number which is 0 > x > -10 """
	return UNKNOWN

def draw_num(num):
	""" Outputs a number which is 10 >= x < 100 """
	result = UNKNOWN
	# if num is valid, output it
	if isinstance(num, int) and num >= 10 and num < 100:
		result = [
			O, O, O, O, O, O, O, O,
			O, O, O, O, O, O, O, O,
			O, O, O, O, O, O, O, O,
			O, O, O, O, O, O, O, O,
			O, O, O, O, O, O, O, O,
			O, O, O, O, O, O, O, O,
			O, O, O, O, O, O, O, O,
			O, O, O, O, O, O, O, O
		]
	return result

def draw_negative_num(num):
	""" Outputs a number which is -10 >= x > -100 """
	return UNKNOWN

if __name__ == "__main__":
	main()
