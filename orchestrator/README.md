# Orchestrator

The orchestrator is an app that interacts with humans, semantic networks, and abilities. When the orchestrator receives a human interaction, it will use generative AI to extract the semantic meaning from the interaction, determine if any of its semantic networks or abilities are related to the query, and then generate tasks to action the interaction.

The orchestrator will continuously improve its semantic networks by acquiring new information with the researcher abilities and updating/creating connections between concepts in semantic networks. The orchestrator can have ongoing tasks using abilities, like improving its own code base. However, interactions with humans will be a priority task.

Unlike queries directly against LLMs, the orchestrator will be inquisitive and proactive. It will be far more humble and willing to ask clarifying questions and admit ignorance. Using abilities, it may also proactively ask humans questions via Slack, for instance, asking whether a specific source it has found contains accurate information and then updating its semantic network with this new information. The orchestrator actions will be auditable as the LLM prompts it produces and responses will be logged. Hallucinations will be far less likely as the LLM prompts the orchestrator produces will be structured with appropriate context.

## Setup
