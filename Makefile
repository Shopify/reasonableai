run_orchestrator:
	python3 orchestrator/main.py

run_orchestrator_worker:
	cd orchestrator && podman-compose up -d # this may not always work its a bit finnickey
	cd orchestrator && celery -A tasks.celery_app worker --loglevel=info

run_semantic_network:
	flask --app semantic_network.main run --debug