.PHONY:
.ONESHELL:

include .env
export

make env:
	poetry env use .venv/bin/python

ngrok:
	docker compose -f compose.yml up -d ngrok

ngrok_mlflow:
	@echo "Getting ngrok URL..."
	@curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | cut -d'"' -f4 || echo "Ngrok not ready yet, try again in a few seconds"

compose:
	- docker compose -f compose.yml up -d

cloudfare:
	cloudflared tunnel --url localhost:5002

lab:
	jupyter lab --port 8888 --host 0.0.0.0

down:
	docker compose -f compose.yml down

remove-data:
	rm -rf data/mlflow

clean: down remove-data
