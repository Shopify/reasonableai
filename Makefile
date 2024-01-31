run_orchestrator:
	python3 orchestrator/main.py

run_semantic_network:
	flask --app semantic_network.main run --debug