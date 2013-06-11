CHECK=\033[32m✔\033[39m
DONE="\n$(CHECK) Done.\n"

PROJECT=jd
SPIDER=directory
TARGET=jcnrd

deploy:
	@echo "\nDeploy $(PROJECT)..."
	scrapy deploy $(TARGET) -p $(PROJECT)
	@echo $(DONE)
