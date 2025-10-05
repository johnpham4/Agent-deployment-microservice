.PHONY:
.ONESHELL:

include .env
export

make env:
	poetry env use .venv/bin/python

ml-platform-up:
	docker compose -f compose.yml up -d mlflow_server

ml-platform-logs:
# For make command that follows logs, if not add prefix '-' then when interrupet the command, it will complain with Error 130
	- docker compose -f compose.yml logs -f

ngrok:
	docker compose -f compose.yml up -d ngrok

ngrok_mlflow:
	@echo "Getting ngrok URL..."
	@curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | cut -d'"' -f4 || echo "Ngrok not ready yet, try again in a few seconds"

ngrok_minio:
	@echo "Getting ngrok URL..."
	@url=$$(curl -s http://localhost:4042/api/tunnels | grep -o '"public_url":"[^"]*"' | cut -d'"' -f4); \
	if [ -n "$$url" ]; then \
		echo "NGROK_MINIO_URL=$$url" > .env.ngrok; \
		echo "Ngrok URL saved to .env.ngrok: $$url"; \
	else \
		echo "Ngrok not ready yet, try again in a few seconds"; \
	fi
make compose:
	- docker compose -f compose.yml up

lab:
	poetry run jupyter lab --port 8888 --host 0.0.0.0

down:
	docker compose -f compose.yml down

remove-data:
	rm -rf data/mlflow

clean: down remove-data
