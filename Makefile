dev:
	uv run Services/trader/src/trader/main.py

build:
	docker build -t trades:dev -f docker/trades.dockerfile .
