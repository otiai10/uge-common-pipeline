import os, sys, getopt, re, subprocess
from collections import namedtuple
from cooker import Cooker

class Args:

	def __init__(self, opts):
		self.recipe  = ""
		self.env     = ""
		self.verbose = False
		self.tail    = None
		for opt, arg in opts:
			if   opt in ("-r", "--recipe"):  self.recipe  = arg
			elif opt in ("-E", "--env"):     self.env     = arg 
			elif opt in ("-v", "--verbose"): self.verbose = True
			elif opt in ("-t", "--tail"):    self.tail    = arg
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
	opts, args = getopt.getopt(argv, "r:E:vt:", [
		"recipe=", "env=", "verbose", "tail="
	])
	return Args(opts)

def follow_logs(project_path = "."):
	project_path = os.getcwd() if project_path == "." else project_path
	if "logs" not in os.listdir(project_path): raise Exception("Need to `cd` to location where your recipe.json exists")
	dirs = filter(lambda d: re.match("[0-9]{4}_[0-9]{4}_[0-9]{4}", d) is not None, os.listdir(os.path.join(project_path, "logs")))
	dirs.sort()
	latest_dir = dirs.pop()
	file_list = []
	for name in os.listdir(os.path.join(project_path, "logs", latest_dir)):
		file_list.append(os.path.join(project_path, "logs", latest_dir, name, "stderr.log"))
		file_list.append(os.path.join(project_path, "logs", latest_dir, name, "stdout.log"))
	try:
		subprocess.call(["tail", "-f"] + file_list)	
	except:
		print("\nExit from tail mode of uge_cooker.\n")
	return

def cooker_main(argv = []):
	args = parse_args(argv)

	if args.tail is not None: return follow_logs(args.tail)

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
