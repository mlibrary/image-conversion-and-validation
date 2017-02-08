test:
	bash bin/run_tests.sh

clean:
	touch __pycache__
	find . -name __pycache__ | xargs rm -r

alltests:
	python -m unittest && find . -name '*.bats' | xargs bats
