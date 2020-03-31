IMAGE_NAME = html-server-image
VERSION = v2
DIR = $(shell pwd)
HTML_FILE = "tempBrowseLocal.html"
ARGS=

requirements:
	pip install -r setup/requirements.txt

generate:
	python -m chinese_non_natively $(ARGS)

compile_gen:
	cd chinese_non_natively/ && easycython --debugmode add_pinyin.pyx && cd ..
	python -m chinese_non_natively $(ARGS)

build:
	docker build -t $(IMAGE_NAME):$(VERSION) -f docker/Dockerfile .

run:
	docker run -d \
	-p 8082:8080 \
	-v $(DIR)/$(HTML_FILE):/usr/share/nginx/html/index.html \
	$(IMAGE_NAME):$(VERSION)