build:
	docker compose build

down:
	docker compose down

start:
	docker compose up -d

up: build start migrate statics

statics:
	docker exec -ti api-flask python3 manage.py collectstatic --noinput

migrate:
	docker compose run --rm api python manage.py migrate

deps:
	docker compose run --rm api poetry install

bash:
	docker compose run --rm api /bin/sh

test: build migrate
	docker compose run --rm api python manage.py test

coverage: build migrate
	docker compose run --rm api coverage run --source='api' --omit='api/tests/*' manage.py test
	docker compose run --rm api coverage report
	docker compose run --rm api coverage xml
