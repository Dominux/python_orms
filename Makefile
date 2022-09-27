test_tortoise_orm:
	cd tortoise_orm \
	&& docker-compose -f docker-compose.test.yml down \
	&& docker-compose -f docker-compose.test.yml build \
	&& docker-compose -f docker-compose.test.yml run app || true \
	&& cd -
