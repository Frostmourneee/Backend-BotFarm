ENV_FILE := $(if $(wildcard .env),.env)
ifneq ($(ENV_FILE),)
include $(ENV_FILE)
export $(shell sed 's/=.*//' $(ENV_FILE))
endif

REVISION_ARG = $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

env: ##@Environment Создание .env файла с переменными
	cat example.env > .env

up: ##@Docker Запуск всего приложения
	docker compose up backend postgres -d --build

down: ##@Docker Остановка приложения
	docker compose down

psql: ##@Database Подключение к базе с помощью утилиты psql
	docker exec -it $(POSTGRES_HOST) psql --pset pager=off -U $(POSTGRES_USER) -d $(POSTGRES_DB)

revision: ##@Database Создать миграцию
	docker exec -it backend uv run alembic -c backend/db/alembic.ini revision --autogenerate

upgrade:  ##@Database Накатить миграции до выбранной
	docker exec -it backend uv run alembic -c backend/db/alembic.ini upgrade $(or $(REVISION_ARG),head)

downgrade:  ##@Database Откатить миграции до выбранной
	docker exec -it backend uv run alembic -c backend/db/alembic.ini downgrade $(or $(REVISION_ARG),base)

test:
	docker compose up backend-tests --build
