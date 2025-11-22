ENV_FILE := $(if $(wildcard .env),.env)
ifneq ($(ENV_FILE),)
include $(ENV_FILE)
export $(shell sed 's/=.*//' $(ENV_FILE))
endif

# Commands
help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

env: ##@Environment Create .env file with variables
	cat example.env > .env

up: ##@Docker Start app
	docker compose up -d --build

down: ##@Docker Stop app
	docker compose down

psql: ##@Database Connect to PostgreSQL database via psql util
	docker exec -it $(POSTGRES_HOST) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)