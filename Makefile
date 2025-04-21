dev:
	uv run Services/${service}/src/${service}/main.py

build:
	docker build -t ${service}:dev -f docker/${service}.dockerfile .

push: 
	kind load docker-image ${service}:dev --name rwml-34fa

deploy: build push 
	kubectl delete -f deployments/dev/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployments/dev/${service}/${service}.yaml	

lint:
	ruff check . --fix --no-cache --unsafe-fixes