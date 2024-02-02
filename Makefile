run_orchestrator:
	python3 orchestrator/main.py

run_orchestrator_worker:
	cd orchestrator && podman-compose up -d # this may not always work its a bit finnickey
	cd orchestrator/src/event_framework && celery -A event_framework worker --loglevel=INFO

run_semantic_network:
	flask --app semantic_network.main run --debug