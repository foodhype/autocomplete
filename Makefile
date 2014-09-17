# Run test console.
run:
	python console.py

# Clear cache files.
clean:
	rm *.p
	rm *.pyc

# Run pylint on all Python files.
lint:
	pylint *.py

# Prepare project for committing.
prepare:
	rm *.pyc
