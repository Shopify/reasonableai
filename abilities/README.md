# Abilites

An ability is an app with an API interface that can do a specific task. For instance, run python code and return the results, extract emails from an inbox via IMAP, create a GitHub pull request on a repo, use the internet to answer a question, or ask a specific human a question via Slack. Ideally, we can create an ability that can generate pull requests to create new abilities, improve existing abilities, and improve the orchestrator (most importantly improving prompt and case statement efficiency).

We will create a researcher ability first. This ability will know where to search for specific information online, for instance, if you query a researcher ability for the current prime minister of Canada, it may search the internet, find an answer on Wikipedia, check the primary source, validate that the linked primary source is legitimate, and then return the answer along with the source. A researcher will also be able to return relevant documents for a specific concept, for example, if you query a researcher ability for documentation on Python coding, it will need a way to reason where accurate documentation exists, hopefully determining that sources like docs.python.org, docs.python-guide.org, the Wikipedia articles for Python_(programming_language), and the top 1000 packages on pypi.org are legitimate. Then, where licencing permits, scrape those sources and returning the documents (the orchestrator could then process these documents to grow a semantic network).