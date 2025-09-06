up:
	docker compose -f infra/docker-compose.yml up -d


down:
	docker compose -f infra/docker-compose.yml down


seed:
	python -m apps.server.src.app.seed_demo