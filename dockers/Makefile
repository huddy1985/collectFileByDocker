# autogenerate Dockfile

docker_run := ./scripts/run.sh
docker_file := ./scripts/docker/Dockerfile
repos := ./repos/repo.list
sh := bash

start:
	$(sh) $(docker_run) $(repos) $(docker_file)
