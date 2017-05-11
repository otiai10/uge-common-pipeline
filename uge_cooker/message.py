import sys

__red   = "31"
__green = "32"
__white = "37"

class Printer():


	def __init__(self, dest = sys.stdout):
		self.__dest = dest
		self.__style = "0"
		self.__color = "37"
		self.__background = "40"


	def out(self, s):
		return self.__dest.write(self.__build() + s + self.__reset())


	def style(self, style):
		self.__style = style
		return self

	def color(self, color):
		self.__color = color
		return self


	def bg(self, color):
		self.__background = color
		return self


	def __build(self):
		return "\x1b[" + ";".join([self.__style, self.__color, self.__background]) + "m"

	def __reset(self):
		return "\x1b[0m"


def red(s):
	printer = Printer()
	printer.color(__red)
	return printer.out(s)

def green(s):
	printer = Printer()
	printer.color(__green)
	return printer.out(s)

def white(s):
	printer = Printer()
	printer.color(__white)
	return printer.out(s)
