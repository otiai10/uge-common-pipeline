import json, os, datetime
from job import Job

class Cooker:

	def __init__(self, env, cwd):
		self.env = {}
		if os.path.isfile(env) and env.endswith(".json"):
			with open(env, "r") as env_file:
				self.env = json.load(env_file)
		self.jobs = []
		self.cwd = cwd
		self.birthtime = datetime.datetime.now()

	def introduce(self):
		print(dir(self))


	def order(self, recipe):
		self.recipe_dir = os.path.dirname(recipe)
		self.log_dir    = os.path.join(self.recipe_dir, "logs", self.birthtime.strftime("%Y_%m%d_%H%M"))
		with open(recipe, "r") as recipe_file:
			raw = json.load(recipe_file)
			self.__parse(raw)


	def __parse(self, raw_recipe):
		for raw in raw_recipe["jobs"]:
			job = Job(raw=raw, log_dir=self.log_dir, recipe_dir=self.recipe_dir, env=self.env)
			self.jobs.append(job)


	def cook(self, verbose=False):
		for i, job in enumerate(self.jobs):
			prev = self.jobs[i - 1] if self.jobs[i - 1].id is not None else None
			job.submit(prev)
			if verbose: print(job.inspect())


	def report(self):
		ok = len(filter(lambda j: j.status == 0, self.jobs))
		ng = len(self.jobs) - ok
		print("REPORT: {} jobs are submitted successfully, with {} error(s).".format(ok, ng))
		print("FYI-> uge_cooker -t {}".format(self.recipe_dir.replace(self.cwd, ".")))
