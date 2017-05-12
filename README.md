# uge_cooker

Univa Grid Engine Recipe Cooker

# Why?

- bad to handle envs and options in script files
	- good to separate operations and project-specific things
- bad to execute duplicate commands to follow logs
	- good to just hit the same command for each project to follow logs
- bad to specify job names only to deal `-hold_jid`
	- good to autommatically generate `-hold_jid`

# Installation

```sh
$ pip install git+https://github.com/otiai10/uge_cooker.git
$ which uge_cooker
```

```sh
# Try it first!!
$ git clone https://github.com/otiai10/uge_cooker.git
$ cd uge_cooker/example_project
$ uge_cooker -r recipe.json
```

# Example

```json
{
  "jobs": [
    {
      "name": "hello_01",
      "script": "./hello_01.sh",
      "options": {}
    },
    {
      "name": "hello_02",
      "script": "./hello_02.sh",
      "options": {
        "-hold_jid": "$$PREVIOUS_JOB_ID"
      }
    }
  ]
}
```

then

```sh
$ uge_cooker --recipe your_recipe.json
```

# Basic Usage

```sh
uge_cooker -r recipe.json -E env.json
```

# Tail mode

to follow tails of logs in current directory (where recipe.json is placed)

```sh
uge_cooker -t .
```

# Options

| option | value | description |
|:-------:|:-------:|:-----------:|
| -t,--tail | **required, if provided** | Execute `tail -f logs/**/*/*` to follow logs, would abort any options else |
| -r,--recipe | **required, if provided** | Recipe json file path, which specifies operation details, must be `.json` |
| -E,--env    | optional default ` ` | Specify env json file path, which specifies env vars, must be `.json` if provided |
| -v,--verbose | optional, no value | Turn on verbose logs of what commands are exactly executed |
