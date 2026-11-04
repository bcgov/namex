.PHONY: help build tag push clean

REGION := northamerica-northeast1
IMAGE_PROJECT := c4hnrd-tools
IMAGE_REPO := vm-repo
IMAGE_NAME := namex-solr-healthcheck
ENVS := dev test sandbox prod

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build              Build base image"
	@echo "  tag                Tag image for all environments"
	@echo "  push               Push all tags to artifact registry"
	@echo "  clean              Remove local images"

build:
	docker build -t $(REGION)-docker.pkg.dev/$(IMAGE_PROJECT)/$(IMAGE_REPO)/$(IMAGE_NAME):latest .
	@echo "✓ Built image"

tag: build
	$(foreach env,$(ENVS),docker tag $(REGION)-docker.pkg.dev/$(IMAGE_PROJECT)/$(IMAGE_REPO)/$(IMAGE_NAME):latest $(REGION)-docker.pkg.dev/$(IMAGE_PROJECT)/$(IMAGE_REPO)/$(IMAGE_NAME):$(env);)
	@echo "✓ Tagged for: $(ENVS)"

push: tag
	$(foreach env,$(ENVS),docker push $(REGION)-docker.pkg.dev/$(IMAGE_PROJECT)/$(IMAGE_REPO)/$(IMAGE_NAME):$(env);)
	@echo "✓ Pushed all tags"

clean:
	$(foreach env,$(ENVS),docker rmi $(REGION)-docker.pkg.dev/$(IMAGE_PROJECT)/$(IMAGE_REPO)/$(IMAGE_NAME):$(env) || true;)
	docker rmi $(REGION)-docker.pkg.dev/$(IMAGE_PROJECT)/$(IMAGE_REPO)/$(IMAGE_NAME):latest || true
	@echo "✓ Cleaned"
