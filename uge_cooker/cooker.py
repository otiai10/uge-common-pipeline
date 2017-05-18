import json, os, datetime
from job import Job

import message
from templates.final_report import TemplateFinalReport
from templates.sync_spawn import TemplateSyncSpawn

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
		self.log_dir    = os.path.join(self.recipe_dir, "logs", self.birthtime.strftime("%Y_%m%d_%H%M%S"))
		self._gen_script_dir = os.path.join(self.recipe_dir, "_generated")
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
			if job.spawn:
				ids = self.__spawn(parent=job, count=job.spawn, prev=prev)
				syncer_job = self.__create_spawn_sync(job.name, ids)
				syncer_job.submit(prev) # TODO: This syncer job would be lost from cooker management :(
				job.id = syncer_job.id
				job.status = syncer_job.status
			else:
				job.submit(prev)
			if verbose: print(job.inspect())

	def __spawn(self, parent, count, prev):
		ids = []
		for index in range(count):
			child = parent.replicate(index)
			child.submit(prev)
			ids.append(child.id)
		return ids

	def report(self):
		ok = len(filter(lambda j: j.status == 0, self.jobs))
		ng = len(self.jobs) - ok
		s = "REPORT: {} jobs are submitted successfully, with {} error(s).\n".format(ok, ng)
		if ng is 0: message.green(s)
		else: message.red(s)


	def append_slack_report(self, params):
		if not os.path.isdir(self._gen_script_dir):
			os.makedirs(self._gen_script_dir)
		tpl = TemplateFinalReport(cooker=self, token=params.get("token"), channel=params.get("channel"), mention=params.get("mention"))
		scr = os.path.join(self._gen_script_dir, "final_report_slack.sh")
		with open(scr, "w+") as f:
			f.write(tpl.out())
		raw = {
			"name": "final_report",
			"script": "./_generated/final_report_slack.sh",
			"options": {
				"-hold_jid": "$$PREVIOUS_JOB_ID"
			}
		}
		job = Job(raw=raw, log_dir=self.log_dir, recipe_dir=self.recipe_dir, env=self.env)
		self.jobs.append(job)


	def __create_spawn_sync(self, parent_name, ids):
		if not os.path.isdir(self._gen_script_dir):
			os.makedirs(self._gen_script_dir)
		tpl = TemplateSyncSpawn(parent_name=parent_name, ids=ids, sleep=20)
		name = "spawn_sync_{}".format(parent_name)
		scr = os.path.join(self._gen_script_dir, name + ".sh")
		with open(scr, "w+") as f:
			f.write(tpl.out())
		raw = {
			"name":    name,
			"script": "./_generated/{}.sh".format(name),
			"options": {
				"-hold_jid": "$$PREVIOUS_JOB_ID"
			}
		}
		return Job(raw=raw, log_dir=self.log_dir, recipe_dir=self.recipe_dir, env=self.env)
