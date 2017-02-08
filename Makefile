test:
	find . -name '*.bats' | xargs bats -p
	python3 -m unittest 2>&1 | tail -n 3

clean:
	touch __pycache__
	find . -name __pycache__ | xargs rm -r
