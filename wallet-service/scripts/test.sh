#!/bin/sh

# Exit in case of error
set -e

docker-compose -f docker-compose.yml build --build-arg SSH_PRV_KEY="$(cat ~/.ssh/id_git)" --build-arg GITHUB_TOKEN="$(cat .github_token)" backend
# Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-compose.yml down -v --remove-orphans
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml exec -T backend bash /app/tests-start.sh
#docker-compose -f docker-compose.yml down -v --remove-orphans
