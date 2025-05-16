
run:
	uvicorn app.main:app --reload --port 7777

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

lint:
	ruff format app
	ruff check --fix app

db-up:
	docker run --name ium-postgres -e POSTGRES_PASSWORD=ium -e POSTGRES_USER=ium-local -p 5555:5432 -d postgres

db-nuke:
	docker stop ium-postgres
	docker rm ium-postgres
