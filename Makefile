clean:
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	find . -type f -name "*.py[co]" -exec rm -rf {} +
	find . -type f -name ".coverage" -exec rm -rf {} +

# ================================================================================
# R E Q U I R E M E N T S
# ================================================================================
install-pre-commit:
	@pre-commit install && pre-commit install --hook-type commit-msg

requirements:
	pip install --upgrade pip
	poetry install --remove-untracked
	make install-pre-commit

requirements-update:
	poetry update

# ================================================================================
# FORMAT
# ================================================================================
format: install-pre-commit
	pre-commit run --all-files --hook-stage manual


# ================================================================================
# TESTS
# ================================================================================
test:
	pytest .

test-coverage:
	coverage run -m pytest .

coverage-report: test-coverage
	coverage report

test-with-coverage-xml:
	pytest --cov=./bitbanker-sdk --cov-report=xml
