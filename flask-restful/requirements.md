### Updating requirements.txt
After importing new package, add it to requirements.in then run `pip-compile --output-file=requirements.txt requirements.in`

### No pip-compile?
`pip-compile` is part of **pip-tools** package. Run `pip install pip-tools`