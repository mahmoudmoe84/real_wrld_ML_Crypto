#####################################################
#Development
#####################################################
dev:
	uv run Services/${service}/src/${service}/main.py

build-for-dev:
	docker build -t ${service}:dev -f docker/${service}.dockerfile .

push-for: 
	kind load docker-image ${service}:dev --name rwml-34fa

deploy-for-dev: build push 
	kubectl delete -f deployments/dev/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployments/dev/${service}/${service}.yaml	

#####################################################
#Production
#####################################################
build-and-push-for-prod:
	docker buildx build --platform linux/arm64,linux/amd64 -t ghcr.io/mahmoudmoe84/${service}:0.1.3-beta.$(shell date +%s) -f docker/${service}.dockerfile . --push
#####################################################





lint:
	ruff check . --fix --no-cache --unsafe-fixes