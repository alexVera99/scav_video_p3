lint:
	./venv/bin/pylint src test
	./venv/bin/pydocstyle src test
	./venv/bin/pycodestyle --select E,W src test
	./venv/bin/mypy src test