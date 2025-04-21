dev:
	uv run Services/${service}/src/${service}/main.py

build:
	docker build -t ${service}:dev -f docker/${service}.dockerfile .

push: 
	kind load docker-image trades:dev --name rwml-34fa

deploy: build push 
	kubectl delete -f deployments/dev/trades/trades.yaml	
	kubectl apply -f deployments/dev/trades/trades.yaml	

lint:
	ruff check . --fix --no-cache --unsafe-fixes