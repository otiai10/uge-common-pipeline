import os
import subprocess
import re

class Job:


	def __init__(self, raw, log_dir, recipe_dir, env):
		self.script = os.path.join(recipe_dir, raw["script"])
		self.work_dir = os.path.join(log_dir, raw["name"])
		self.options = {
			"-cwd": None,
			"-o": self.__work_path("stdout.log"),
			"-e": self.__work_path("stderr.log"),
		}
		self.name    = raw["name"]
		self.options.update(raw["options"])
		self.env = env if env is not None else {}
		self.status  = None
		self.error   = ""
		self.id      = None
		self.prev    = None
		self.__process = None


	def __work_path(self, file_name):
		return os.path.join(self.work_dir, file_name)


	def build(self, cmd="qsub", prev=None):
		if prev is not None: self.prev = prev
		return [cmd] + self.__build_options(prev) + self.__build_envs() + [self.script]


	def __build_options(self, prev=None):
		prev = prev if prev is not None else self.prev
		replace = (lambda s: s.replace("$$PREVIOUS_JOB_ID", prev.id)) if prev is not None else (lambda s: s)
		pool = []
		for key, val in self.options.iteritems():
			opt = " ".join([key, replace(val)]) if val is not None else key
			pool.append(opt)
		return pool


	def __build_envs(self):
		pool = []
		if self.env == {}: return pool
		for key, val in self.env.iteritems():
			pool.append("-v {}={}".format(key, val))
		return pool


	def submit(self, prev=None):
		if prev is not None: self.prev = prev
		self.__process = subprocess.Popen(self.build(prev=prev), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(out, err) = self.__process.communicate()
		self.status = self.__process.returncode
		self.error  = err
		m = re.search(" (?P<job_id>[0-9]+)[.0-9:\-]* ", out)
		self.id = m.group("job_id") if m is not None else None

	def inspect(self):
		return "\n".join([
			"# {} (id:{})".format(self.name, self.id),
			"",
			"> STATUS: {} {}".format(self.status, self.error.strip()),
			"",
			"```",
			" \\\n".join(self.build()),
			"```"
		]) + "\n"
