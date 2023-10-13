# Test script for creating html pages from json CIS check results

Script parser of a json file obtained as a result of a system audit using technology
https://github.com/ansible-lockdown/RHEL8-CIS-Audit

# Installation

```
python -m venv venv

source ./venv/bin/activate

pip install -r requirements.txt
```

# Launch

## Put the ``.json`` files in the reports directory

```
python ./cis/main.py
```

## The result will be available in the results folder
