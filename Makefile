init:
	pip install -r requirements.txt

test:
	python -m unittest discover -p "*_test.py"

demo:
	python demo.py

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.db' -delete
	python ./clean_demo_db.py #deletes demo database!

.PHONY: init test demo clean
