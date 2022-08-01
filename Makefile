NAME = posology
PWD = $(shell pwd)

.PHONY: train
train:
	docker build -t $(NAME)-train -f trainer.Dockerfile .
	docker run --rm\
		--name=$(NAME)-train\
		-v $(PWD)/src/train:/app/posology\
		$(NAME)-train


.PHONY: api
api:
	docker build -t $(NAME)-api -f api.Dockerfile .
	docker run --rm\
		--name=$(NAME)-api\
		-v $(PWD)/src/api:/app/posology\
		-v $(PWD)/src/train/models:/app/posology/resources\
		-p 4002:4002\
		-d\
		$(NAME)-api

.PHONY: clean
clean:
	docker rm --force $(NAME)-api
	docker rm --force $(NAME)-train
	docker image rm --force $(NAME)-api
	docker image rm --force $(NAME)-train
