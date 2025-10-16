.PHONY:
.ONESHELL:

include .env
export

make env:
	poetry env use .venv/bin/python

mlflow:
	docker compose -f mlflow/compose.yml up -d

monitor:
	docker compose -f monitor/compose.yml up -d

app:
	docker compose -f compose.yml up -d

down:
	docker compose -f monitor/compose.yml down &&
	docker compose -f mlflow/compose.yml down &&
	docker compose -f compose.yml down

ngrok_mlflow:
	@echo "Getting ngrok URL..."
	@curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | cut -d'"' -f4 || echo "Ngrok not ready yet, try again in a few seconds"


cloudfare:
	cloudflared tunnel --url localhost:5002

lab:
	jupyter lab --port 8888 --host 0.0.0.0

remove-data:
	rm -rf data/mlflow

clean: down remove-data
