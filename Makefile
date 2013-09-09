upload: clean
	python setup.py sdist upload

clean:
	find . -name *.pyc -delete
	find . -name .DS_Store -delete
