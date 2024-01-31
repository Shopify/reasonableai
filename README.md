# ReasonAbleAI (WIP - Hack Days Project)

🚨Please note this is a Hack Days project and may not adhere to Shopify's code quality standards🚨

## Working with the repository

1. Ensure you have [pipenv](https://pipenv.pypa.io/en/latest/) installed
2. Run `pipenv install` to install the dependencies
3. Run `pipenv shell` to shell into your environment
4. To start the orchestrator `make run_orchestrator`
5. To start the semantic network `make run_semantic_network`

## Context

ChatGPT regurgitating facts is a party trick. The true value of Generative AI is its ability to organise information and then reason. This is a proposed open source self-improving auditable framework using Large Language Models (LLMs) like ChatGPT and [Mixtral](https://mistral.ai/news/mixtral-of-experts/).

Generative AI is predicting what should come next and is unaware of concepts. For instance, generative AI image models do not have a concept of a human hand. The models predict that a finger-like structure is normally next to another finger-like structure so they often create hands with too many fingers. Increasing the context window will help reduce these kinds of errors but it does not address the fundamental problem, the model is unaware of the concept of a hand. This project will use generative AI’s semantic extraction and reasoning abilities to build a concept aware auditable AI framework that can learn, think, and improve itself.


## Design

This is the intial design but expect this to evolve during prototyping. We will design the APIs or adopt an existing standard. The scope of this Hack Days will be limited to text however design decisions should assume we will be using multimodal models in the future.

![Image](https://github.com/gregology/gregology.github.io/assets/1595448/6b35dd47-bde1-4c10-a2c2-bd6aa9fac799)


### Human

A mostly hairless ape.


### Semantic network

A semantic network will be concepts stored within a graph-based data structure and accessible via an app with an API to interface. Each semantic network will be atomic for a specific subject, for example, a Python coding semantic network or a semantic network based on your email inbox. A Python coding semantic network may be read-only and publicly accessible while your email inbox semantic network would be read/write and private. The concepts and relationships will be added to the semantic network via an orchestrator.


### Ability

An ability is an app with an API interface that can do a specific task. For instance, run python code and return the results, extract emails from an inbox via IMAP, create a GitHub pull request on a repo, use the internet to answer a question, or ask a specific human a question via Slack. Ideally, we can create an ability that can generate pull requests to create new abilities, improve existing abilities, and improve the orchestrator (most importantly improving prompt and case statement efficiency).

We will create a researcher ability first. This ability will know where to search for specific information online, for instance, if you query a researcher ability for the current prime minister of Canada, it may search the internet, find an answer on Wikipedia, check the primary source, validate that the linked primary source is legitimate, and then return the answer along with the source. A researcher will also be able to return relevant documents for a specific concept, for example, if you query a researcher ability for documentation on Python coding, it will need a way to reason where accurate documentation exists, hopefully determining that sources like docs.python.org, docs.python-guide.org, the Wikipedia articles for Python_(programming_language), and the top 1000 packages on pypi.org are legitimate. Then, where licencing permits, scrape those sources and returning the documents (the orchestrator could then process these documents to grow a semantic network).


### Orchestrator

The orchestrator is an app that interacts with humans, semantic networks, and abilities. When the orchestrator receives a human interaction, it will use generative AI to extract the semantic meaning from the interaction, determine if any of its semantic networks or abilities are related to the query, and then generate tasks to action the interaction.

The orchestrator will continuously improve its semantic networks by acquiring new information with the researcher abilities and updating/creating connections between concepts in semantic networks. The orchestrator can have ongoing tasks using abilities, like improving its own code base. However, interactions with humans will be a priority task.

Unlike queries directly against LLMs, the orchestrator will be inquisitive and proactive. It will be far more humble and willing to ask clarifying questions and admit ignorance. Using abilities, it may also proactively ask humans questions via Slack, for instance, asking whether a specific source it has found contains accurate information and then updating its semantic network with this new information. The orchestrator actions will be auditable as the LLM prompts it produces and responses will be logged. Hallucinations will be far less likely as the LLM prompts the orchestrator produces will be structured with appropriate context.

#### Example orchestrator interaction

As a simple example consider the orchestrator receiving this query from a human "who is the current prime minister of Canada?". The orchestrator will programmatically generate a prompt for an LLM using knowledge of its available semantic networks and abilities to determine how best to proceed.

```prompt
"who is the current prime minister of Canada?".
Return a JSON blob that answers the following questions about this chat message with confidence scores from 0 to 1 using a precision of 0.01;
 - single_question (does this chat message contain a single question?)
 - multiple_questions (does this chat message contain multiple questions?)
 - clarifying_questions (does this chat message require clarification?)
  ...
 - python_semantic_network (does this chat message relate to Python coding?)
 - online_researcher_ability (does this chat message contain a question that can change over time?)
```

```response
{
  "single_question" : 1,
  "multiple_questions": 0,
  "clarifying_questions": 0,
  ...
  "python_semantic_network": 0,
  "online_researcher_ability": 0.99
}
```

Using the response and case statements the orchestrator will;

* create a task to respond to the human informing them that they are currently researching the question
* create a task to pass this message to its online research ability (with listener)
* create a listener that waits for the online research ability tasks to finish and then responds to the human

The reasoning logic occurring during these interactions is logged and the framework's decisions are auditable. 


## Technology

_Current choices for the tech stack are weakly held opinions, please make cases for alternative stacks._


### Models

This framework will be LLM agnostic, capable of running on local or cloud models and be easily portable to new LLM offerings. For most reasoning tasks the orchestrator should use efficient LLMs with high reasoning abilities. Currently for reasoning skills the best locally hosted offering is [Mistral's Mixtral](https://mistral.ai/news/mixtral-of-experts/) and the best cloud hosted offering is OpenAI's ChatGPT 4. We can use [Ollama](https://ollama.ai/) as an interface for local models and OpenAI API for cloud models.


### Implementation

We will use Python and Flask where possible as it is lightweight and simple which will make it easier for the framework to understand and self-improve.

We will use Podman for containerization. A deployment will consist of a single orchestrator app with multiple semantic networks and abilities.

A **semantic network** will consist of a simple API app and a graph-based database. Semantic network APIs will expose a documentation endpoint designed specifically for efficient ingestion by LLMs. The documentation endpoint will contain details about what is stored within the semantic network. Semantic network APIs will allow the orchestrator to retrieve documents and relationships. When the semantic network allows write access the semantic network API will also allow the orchestrator to insert documents and create relationships. We will use Flask for the API app and Neo4j as the graph-based database. The optimal graph-based database to use will depend on the size and relationships of the concepts being stored.

An **ability** will be an app with an API. Ability APIs will differ depending on their use case but all ability APIs will expose a documentation endpoint designed specifically for efficient ingestion by LLMs. The orchestrator will use the documentation endpoint to craft API calls to the ability. The code / framework choice will be dependent on the task. Specific abilities may consist of multiple docker containers, for instance, an online researching ability may have an associated [SearXNG](https://github.com/searxng/searxng) instance for querying the internet.

The **orchestrator** will be an app with either an API or chat interface that is capable of running queued tasks. This will likely be a simple Flask app using Celery and Flower with PostgresSQL & Redis. 


# Open questions

* Is Flask the best stack for the orchestrator app?
* What risks are associated with creating this and how can we mitigate dangers?
* What safety measures and canaries should we implement?
* How should we be testing our frameworks for biases?


# Further research links

Software
* [Ollama](https://ollama.ai/) - self host LLM models with API
* [SearXNG](https://github.com/searxng/searxng) - meta search engine with API

Models
 * [Mistral's Mixtral](https://mistral.ai/news/mixtral-of-experts/) - current best preforming locally hostable LLM
 * [Ollama's library of models](https://ollama.ai/library?sort=newest) - list of new LLMs available in Ollama

Concepts
* [Graph databases](https://en.wikipedia.org/wiki/Graph_database) and [Cypher](https://en.wikipedia.org/wiki/Cypher_(query_language))
* [Prompt engineering](https://en.wikipedia.org/wiki/Prompt_engineering)
* [Neuro-symbolic AI](https://en.wikipedia.org/wiki/Neuro-symbolic_AI)

Videos
 * [From artificial intelligence to hybrid intelligence - with Catholijn Jonker](https://youtu.be/vb_Os_AJXjY)


_Project based on this [blog post](https://gregology.net/2024/01/generative-ai-framework-to-grow-thinking-agents/)._
