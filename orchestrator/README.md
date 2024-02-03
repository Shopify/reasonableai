# Orchestrator

The orchestrator is an app that interacts with humans, semantic networks, and abilities. When the orchestrator receives a human interaction, it will use generative AI to extract the semantic meaning from the interaction, determine if any of its semantic networks or abilities are related to the query, and then generate tasks to action the interaction.

The orchestrator will continuously improve its semantic networks by acquiring new information with the researcher abilities and updating/creating connections between concepts in semantic networks. The orchestrator can have ongoing tasks using abilities, like improving its own code base. However, interactions with humans will be a priority task.

Unlike queries directly against LLMs, the orchestrator will be inquisitive and proactive. It will be far more humble and willing to ask clarifying questions and admit ignorance. Using abilities, it may also proactively ask humans questions via Slack, for instance, asking whether a specific source it has found contains accurate information and then updating its semantic network with this new information. The orchestrator actions will be auditable as the LLM prompts it produces and responses will be logged. Hallucinations will be far less likely as the LLM prompts the orchestrator produces will be structured with appropriate context.

## Containerized Deployment

Create [`settings.yaml`](https://github.com/Shopify/reasonableai/blob/main/orchestrator/settings.yaml.example) with [semantic networks](https://github.com/Shopify/reasonableai/tree/main/semantic_network), abilities (incoming...), desires of your choosing, and [Ollama API url](https://ollama.ai/).

```
semantic_networks:
  - name: Tigers
    url: https://tigers.domain.tld
    description: Has details about tigers, their habbits, range, etc
abilities:
  - name: Researcher
    url: https://reseracher.domain.tld
    description: Can query the internet to reserach any topic
desires:
  - name: Tigers
    priority: 10
    description: Use the Researcher ability to learn about Tigers and store that information in the Tigers semantic network
ollama_url: https://ollama-api.domain.tld
```

Example `docker-compose.yaml`

```
version: '3'
services:
  orchestrator-web:
    build: .
    container_name: orchestrator-web
    hostname: orchestrator-web-host
    volumes:
      - .:/app
    ports:
      - "5000:5000"
    environment:
      - RABBITMQ_HOST=amqp://guest:guest@my-rabbit:5672/
      - OLLAMA_URL=${OLLAMA_URL}
    depends_on:
      - my-rabbit

  orchestrator-worker:
    build: .
    command: celery -A celery_app worker
    container_name: orchestrator-worker
    hostname: orchestrator-worker-host
    volumes:
      - .:/app
    environment:
      - RABBITMQ_HOST=amqp://guest:guest@my-rabbit:5672/
      - ORCHESTRATOR_WEB_URL=http://orchestrator-web:5000
      - OLLAMA_URL=${OLLAMA_URL}
    depends_on:
      - my-rabbit

  my-rabbit:
    image: rabbitmq:3-management-alpine
    container_name: my-rabbit
    hostname: my-rabbit-host
    ports:
      - "15672:15672"
      - "5672:5672"
    volumes:
      - rabbit_data:/var/lib/rabbitmq

volumes:
  rabbit_data:
```

```bash
$ podman-compose up
```
