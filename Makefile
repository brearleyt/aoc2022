lint:
	black --check .
	isort --profile black --check-only .
	mypy .
	pylint solutions tests

test:
	pytest tests

.PHONY: \
	lint \
	test