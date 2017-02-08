test:
	find . -name '*.bats' | xargs bats -p

clean:
	touch __pycache__
	find . -name __pycache__ | xargs rm -r
