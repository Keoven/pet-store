lint:
	flake8 .

test:
	pytest -s

pip-compile:
	pip-compile --generate-hashes requirements.in
	pip-compile --generate-hashes dev-requirements.in

pip-sync:
	pip-sync requirements.txt dev-requirements.txt

dev-start:
	uvicorn pet_store.main:app --reload

start:
	uvicorn pet_store.main:app

migration:
	alembic revision --autogenerate

db-upgrade:
	alembic upgrade head
