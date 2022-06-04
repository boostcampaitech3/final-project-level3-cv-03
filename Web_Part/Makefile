run_black:
	python3 -m black . -l 119

run_server:
	python3 -m back_fastapi.app

run_client:
	python3 -m streamlit run ./front_streamlit/app.py --server.port 30001 --server.fileWatcherType=none

run_app: run_server run_client

run_assignment_tests:
	poetry run pytest assignments/app_test.py