from setuptools import setup, find_packages

setup(
	name='uge_cooker',
	version='0.0.8',
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'uge_cooker = uge_cooker.main:cooker_main',
		]
	},
)
