IMAGE_NAME = html-server-image
VERSION = v1
DIR = $(shell pwd)
HTML_FILE = "tempBrowseLocal.html"

requirements:
	pip install -r setup/requirements.txt

generate:
	python -m chinese_non_natively

build:
	docker build -t $(IMAGE_NAME):$(VERSION) -f docker/Dockerfile .

run:
	docker run -d \
	-p 8081:8080 \
	-v $(DIR)/$(HTML_FILE):/usr/share/nginx/html/index.html \
	$(IMAGE_NAME):$(VERSION)