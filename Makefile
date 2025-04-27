#####################################################
#Development
#####################################################
dev:
	uv run Services/${service}/src/${service}/main.py

build-for-dev:
	docker build -t ${service}:dev -f docker/${service}.dockerfile .

push-for-dev: 
	kind load docker-image ${service}:dev --name rwml-34fa

deploy-for-dev: build-for-dev push-for-dev 
	kubectl delete -f deployments/dev/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployments/dev/${service}/${service}.yaml	

#####################################################
#Production
#####################################################
build-and-push-for-prod:
	docker buildx build --platform linux/arm64,linux/amd64 -t ghcr.io/mahmoudmoe84/${service}:0.1.4-beta.$(shell date +%s) -f docker/${service}.dockerfile . --push

deploy-for-prod:
	kubectl delete -f deployments/prod/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployments/prod/${service}/${service}.yaml
	
#####################################################
lint:
	ruff check . --fix --no-cache --unsafe-fixes