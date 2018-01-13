#!/usr/bin/env python-3
# coding: Latin-1
"""
MikeySense Installation File
Installs the MikeySense requirements
Version: 0.1
Created: 13/01/2018
Modified: -
Changelog:
1.0 - 13/01/2018
	Added installing pip3, sense-hat, and pyowm. Also adds the .ini file
"""
import getopt
import os
import subprocess
import sys
from   shutil import copyfile
if os.name == "posix":
	import apt

APTS        = ["python3-pip", "sense-hat"]
PIPS        = ["pyowm"]
PIPS_DEV    = []
DIRECTORIES = []
FILES       = []
CONFIGS     = ["MikeySense"]

def main():
	""" Runs the actual installation """
	print("Installing MikeyEntity")
	#  If on linux, check that the user has root access.
	if os.name == "posix":
		check_sudo()
	#  Set the default settings
	pip_packages = PIPS
	files_only   = False
	#  Check any options provided
	try:
		opts, args = getopt.getopt(sys.argv[1:], "d:f", ["dev", "files_only"])
		args = args
	except getopt.GetoptError:
		print("Invalid arguments")
	#  Loop through the options, checking them
	for opt, arg in opts:
		arg = arg
		#  If enabling dev options
		if opt in ("-d", "-dev"):
			#  Add the dev options
			pip_packages = PIPS + PIPS_DEV
		#  If setting files_only to True
		if opt in ("-f", "-files_only"):
			files_only = True
	#  If not files only, add the required packages
	if not files_only:
		#  Install the apt packages
		install_apt(APTS)
		#  Install the pip packages
		install_pip(pip_packages)
	#  Add any missing directories and files
	check_directory(DIRECTORIES)
	check_file(FILES)
	#  Finally, add the config files if any are missing
	check_config(CONFIGS)

def install_apt(packages):
	""" Installs the required apt packages """
	#  Checks if this is linux. If it isn't, return
	if not os.name == "posix":
		print("This machine isn't linux, skipping adding APT packages")
		return
	#  This is linux
	require_commit = False
	#  Update the apt packages
	print("Updating the apt packages")
	cache = apt.Cache()
	cache.update()
	#  Loop through the packages, adding them
	print("Installing the required packages")
	for pkg_name in packages:
		pkg = cache[pkg_name]
		if pkg.is_installed:
			if pkg.is_upgradable:
				print("Updating %r " % pkg_name)
				pkg.mark_upgrade()
				require_commit = True
			print("%r is already installed" % pkg_name)
		else:
			print("Installing %r " % pkg_name)
			require_commit = True
			pkg.mark_install()
	if require_commit:
		try:
			cache.commit()
		except Exception as arg:
			print("An apt package couldn't be installed: %r" % str(arg))

def install_pip(packages):
	""" Installs the required pip packages """
	for pkg_name in packages:
		print("Installing %r", pkg_name)
		try:
			subprocess.call(["sudo", "pip3", "install", pkg_name])
		except Exception as arg:
			print("Couldn't install " + pkg_name + ": " + str(arg))

def check_directory(directories):
	""" Adds the required directories """
	print("Adding Directories")
	#  Add the Classes and Config directories
	directories = directories + ["Classes", "Config"]
	#  Run through the directories, checking them
	for directory in directories:
		#  If the folder exists, say so
		if os.path.exists(directory):
			print("%r exists" % directory)
		#  Otherwise create it
		else:
			os.makedirs(directory)
			print("Added %r " % directory)
	print("Added Directories")

def check_file(files):
	""" Adds the required files """
	print("Adding Files")
	#  Run through the files, adding them if needed
	for file in files:
		#  If the file exists, say so
		if os.path.exists(file):
			print("%r exists" % file)
		# Otherwise add the file
		else:
			open(file, "a") # pylint: disable=I0011,E1101
			print("Added %r " % file)
	print("Added Files")

def check_config(configs):
	""" Adds the required config files """
	print("Adding Config Files")
	for config in configs:
		ini_path     = "Config/" + config + ".ini"
		example_path = "Config/" + config + ".ini.example"
		#  If the config exists, say so
		if os.path.exists(ini_path):
			print("%s.ini exists" % config)
		#  Otherwise add it
		else:
			#  If an example config file exists, copy it over
			if os.path.exists(example_path):
				try:
					copyfile(example_path, ini_path)
					print("Copied %s " % config)
				except IOError as exc:
					print("Couldn't copy %s: %s" % (config, exc))
			#  Otherwise just add it
			else:
				os.mknod(ini_path) # pylint: disable=I0011,E1101
	print("Added Config Files")

def check_sudo():
	""" Exits if the user doesn't have sudo access """
	#  Checks if this is linux. If it isn't, return
	if not os.name == "posix":
		print("This machine isn't linux, skipping checking sudo privileges")
		return
	if not os.geteuid() == 0: # pylint: disable=I0011,E1101
		print("This needs to be run with sudo.")
		exit()

if __name__ == "__main__":
	main()
