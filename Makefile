dev:
	uv run Services/${service}/src/${service}/main.py

build-and-push-images:
	./scripts/build_and_push_images.sh ${image_name} ${env}

deploy-images:
	./scripts/deploy.sh ${image_name} ${env}

lint:
	ruff check . --fix --no-cache