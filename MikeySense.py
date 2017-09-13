#!/usr/bin/python3
# coding: Latin-1
"""
Mikey Sense
Like Spidey Senses, but with a pi
"""
from sense_hat import SenseHat # pylint: disable=import-error

def main():
	""" Runs when run """
	# Set the sense class up
	sense = SenseHat()
	sense.show_message("Hello :)")
	temperature = sense.get_temperature()
	temperature = str(round(temperature, 1))
	sense.show_message(temperature)

if __name__ == "__main__":
	main()
