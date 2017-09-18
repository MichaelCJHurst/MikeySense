"""
Outputs a clock onto the sense hat LEDs, adapted from
https://yjlo.xyz/blog/design-a-digital-clock-on-raspberry-pi-sense-hat/
"""
from datetime import datetime

def _convert_to_colour(array, background, colour):
		""" Converts the array to the correct colours """
		return [background if j == 0 else colour for j in array]

def _set_nums():
	""" Sets the nums array, only needed when initializing """
	return [
		[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]],
		[[0,0,0,1,0,0],[0,0,1,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,1,1,1,0]],
		[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,0,0,1,0],[0,0,0,1,0,0],[0,0,1,0,0,0],[0,1,1,1,1,0]],
		[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]],
		[[0,0,0,0,1,0],[0,0,0,1,1,0],[0,0,1,0,1,0],[0,1,1,1,1,0],[0,0,0,0,1,0],[0,0,0,0,1,0]],
		[[0,1,1,1,1,0],[0,1,0,0,0,0],[0,1,1,1,0,0],[0,0,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]],
		[[0,0,1,1,0,0],[0,1,0,0,0,0],[0,1,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]],
		[[0,1,1,1,1,0],[0,0,0,0,1,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,1,0,0,0],[0,0,1,0,0,0]],
		[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]],
		[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,1,0],[0,0,0,0,1,0],[0,0,1,1,0,0]],
		[[0,1,0,0,1,0],[1,1,0,1,0,1],[0,1,0,1,0,1],[0,1,0,1,0,1],[0,1,0,1,0,1],[0,1,0,0,1,0]],
		[[0,1,0,0,1,0],[1,1,0,1,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0]],
		[[0,1,0,0,1,0],[1,1,0,1,0,1],[0,1,0,0,0,1],[0,1,0,0,1,0],[0,1,0,1,0,0],[0,1,0,1,1,1]]
	]

class MikeySenseClock:
	""" Outputs a clock """
	def __init__(self):
		""" Initialises the clock """
		self.now    = datetime.now()
		self.hour   = 0
		self.minute = 0
		self.nums   = _set_nums()
		self.hour_num_colour = [255,255,255]
		self.hour_back_colour = [0,0,0]
		self.min_dot_colour = [0, 150, 0]
		self.min_back_colour = [0, 0, 0]
		self.unit = 60.0/29
		# Set the correct time
		self.reset_time()

	def reset_time(self):
		""" Resets the time vars """
		self.now    = datetime.now()
		self.hour   = int(self.now.hour)
		self.minute = int(self.now.minute * 1.0)
		# If the hour is in 24-hour format, change it to 12
		if self.hour > 12:
			self.hour = self.hour - 12

	def output_clock(self):
		""" Outputs a clock """
		img = []
		# First reset the time
		self.reset_time()
		# The first row
		row1 = self.row_one()
		img.extend(_convert_to_colour(row1, self.min_back_colour, self.min_dot_colour))
		# Rows 2 to 7
		for index in range(6):
			if self.minute > (self.unit * (24 - index)):
				img.append(self.min_dot_colour)
			else:
				img.append(self.min_back_colour)
			# Hour number
			img.extend(
				_convert_to_colour(
					self.nums[self.hour][index],
					self.hour_back_colour,
					self.hour_num_colour
				)
			)
			if self.minute > (self.unit * (5 + index)):
				img.append(self.min_dot_colour)
			else:
				img.append(self.min_back_colour)
		# Row 8
		row8 = self.row_eight()
		img.extend(_convert_to_colour(row8, self.min_back_colour, self.min_dot_colour))
		# Return the clock
		return img

	def row_one(self):
		""" Outputs the first row """
		result = [0, 0, 0, 0, 0, 0, 0, 0]
		if self.minute > self.unit * 4 and self.minute < self.unit * 25:
			result = [0, 0, 0, 0, 1, 1, 1, 1]
		else:
			if self.minute < self.unit:
				result = [0,0,0,0,0,0,0,0]
			elif self.minute < self.unit*2:
				result = [0,0,0,0,1,0,0,0]
			elif self.minute < self.unit*3:
				result = [0,0,0,0,1,1,0,0]
			elif self.minute < self.unit*4:
				result = [0,0,0,0,1,1,1,0]
			elif self.minute < self.unit*25:
				result = [0,0,0,0,1,1,1,1]
			elif self.minute < self.unit*26:
				result = [1,0,0,0,1,1,1,1]
			elif self.minute < self.unit*27:
				result = [1,1,0,0,1,1,1,1]
			elif self.minute < self.unit*28:
				result = [1,1,1,0,1,1,1,1]
			else:
				result = [1,1,1,1,1,1,1,1]
		return result

	def row_eight(self):
		""" Outputs the eighth row """
		result = [1,1,1,1,1,1,1,1]
		if self.minute < self.unit * 18:
			if self.minute < self.unit * 11:
				result = [0,0,0,0,0,0,0,0]
			elif self.minute < self.unit * 12:
				result = [0,0,0,0,0,0,0,1]
			elif self.minute < self.unit * 13:
				result = [0,0,0,0,0,0,1,1]
			elif self.minute < self.unit * 14:
				result = [0,0,0,0,0,1,1,1]
			elif self.minute < self.unit * 15:
				result = [0,0,0,0,1,1,1,1]
			elif self.minute < self.unit * 16:
				result = [0,0,0,1,1,1,1,1]
			elif self.minute < self.unit * 17:
				result = [0,0,1,1,1,1,1,1]
			else:
				result = [0,1,1,1,1,1,1,1]
		return result
