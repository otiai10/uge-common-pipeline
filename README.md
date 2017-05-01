# uge_cooker

Univa Grid Engine Recipe Cooker

# Installation

```sh
$ pip install git+https://github.com/otiai10/uge_cooker.git
$ which uge_cooker
```

# Usage

```sh
$ uge_cooker --recipe your_recipe.json
```

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
