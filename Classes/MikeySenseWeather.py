"""
Outputs the current weather to the sense hat LEDs. The weather is courtesy of
https://home.openweathermap.org
"""
import os
import pyowm

class MikeySenseWeather:
	""" Outputs the weather """
	def __init__(self, api_key, location, is_pro = False):
		""" Initialises the weather """
		self.location = location
		if is_pro is True:
			self.owm = pyowm.OWM(API_key=api_key, subscription_type='pro')
		else:
			self.owm = pyowm.OWM(api_key)

	def current_weather(self):
		""" Returns the current weather's icon """
		observation = self.owm.weather_at_place(self.location)
		weather     = observation.get_weather()
		print(weather)
		big_icon = weather.get_weather_icon_name()
		icon     = "unknown.png"
		# Get the name of the smaller icon from the big one
		if big_icon in ["01d", "01n"]:
			icon = "sunny.png"
		elif big_icon in ["02d", "02n", "03d", "03n", "04d", "04n"]:
			icon = "cloudy.png"
		elif big_icon in ["09d", "09n"]:
			icon = "showers.png"
		elif big_icon in ["10d", "10n"]:
			icon = "rainy.png"
		elif big_icon in ["11d", "11n"]:
			icon = "stormy.png"
		elif big_icon in ["13d", "13n"]:
			icon = "snow.png"
		elif big_icon in ["50d", "50n"]:
			icon = "mist.png"
		# Return the icon
		return os.path.abspath(
			os.path.join(
				os.path.dirname(__file__),
				"..",
				"WeatherIcons",
				icon
			)
		)
