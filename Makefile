# commands
.PHONY: build up down clean logs exec

# Builds the Docker environment
build:
	docker-compose build

# Brings up the Docker environment
up:
	docker-compose up -d

# Brings down the Docker environment
down:
	docker-compose down

# Cleans up Docker environment and removes volumes
clean:
	docker-compose down -v

# Views the output from containers for debugging
logs:
	docker-compose logs

# Execute a command inside the Docker app container
exec:
	docker-compose exec app bash
