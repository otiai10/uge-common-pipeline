import json, os
from job import Job

class Cooker:

	def __init__(self, env, cwd):
		if env:
			with open(env, "r") as env_file:
				self.env = json.load(env_file)
		self.jobs = []
		self.cwd = cwd


	def introduce(self):
		print(dir(self))


	def order(self, recipe):
		self.recipe_dir = os.path.dirname(recipe)
		with open(recipe, "r") as recipe_file:
			raw = json.load(recipe_file)
			self.__parse(raw)


	def __parse(self, raw_recipe):
		for raw in raw_recipe["jobs"]:
			self.jobs.append(Job(raw=raw, cwd=self.cwd, recipe_dir=self.recipe_dir))


	def cook(self):
		for i, job in enumerate(self.jobs):
			prev = self.jobs[i - 1] if self.jobs[i - 1].id is not None else None
			job.submit(prev)


	def report(self):
		print("# TODO")
