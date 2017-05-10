import os, sys, getopt
from collections import namedtuple
from cooker import Cooker

class Args:

	def __init__(self, opts):
		self.recipe  = ""
		self.env     = ""
		self.verbose = False
		for opt, arg in opts:
			if   opt in ("-r", "--recipe"):  self.recipe  = arg
			elif opt in ("-E", "--env"):     self.env     = arg 
			elif opt in ("-v", "--verbose"): self.verbose = True
		cwd = os.getcwd()
		self.recipe = os.path.join(cwd, self.recipe)
		self.env    = os.path.join(cwd, self.env)

	def validate(self):
		Err = namedtuple("Err", ("key", "msg"))
		errors = []
		if os.path.isfile(self.recipe) is not True: errors.append(Err("recipe", "recipe must be file"))
		if self.recipe.endswith(".json") is not True: errors.append(Err("recipe", "recipe file must be json"))
		# if os.path.isfile(self.env) is not True: errors.append(Err("env", "env file must be provided"))
		# if self.env.endswith(".json") is not True: errors.append(Err("env", "env file must be json"))
		return errors

def parse_args(argv = []):
	argv = sys.argv[1:] if len(argv) == 0 else argv
	opts, args = getopt.getopt(argv, "r:E:v", [
		"recipe=", "env=", "verbose"
	])
	return Args(opts)

def cooker_main(argv = []):
	args = parse_args(argv)
	errors = args.validate()
	if len(errors) is not 0:
		for err in errors: print("{err.key}:\t{err.msg}".format(err=err))
		return
	cooker = Cooker(args.env, os.getcwd())
	cooker.order(args.recipe)
	# cooker.introduce()
	cooker.cook(args.verbose)
	cooker.report()

if __name__ == "__main__":
	cooker_main(sys.argv[1:])
