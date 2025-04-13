dev:
	uv run Services/trader/src/trader/main.py

build:
	docker build -t trades:dev -f docker/trades.dockerfile .

push: 
	kind load docker-image trades:dev --name rwml-34fa

deploy: build push 
	kubectl apply -f deployments/dev/trades/trades.yaml	
