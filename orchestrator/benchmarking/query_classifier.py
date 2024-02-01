from tqdm import tqdm
from src.utils.compentencies import Ability, SemanticNetwork
from src.utils.query_llm import QueryLLM

models = [
    # 'deepseek-llm:67b-chat',
    # 'dolphin2.2-mistral:latest',
    # 'mistral:latest',
    'mixtral:latest',
    # 'orca-mini:13b',
    # 'orca-mini:7b',
    # 'phi:latest',
    # 'samantha-mistral:latest',
]

temperatures = [0]

compentencies = [
    Ability("GitHub", "Read GitHub repos, create pull requests and issues", "http://github.com"),
    Ability("Researcher", "Search the web information, returns appropriate documents. Useful for finding facts", "http://google.com"),
    SemanticNetwork("Tigers", "Information about Tigers, their habits, ranges, diets, etc", "http://tigers.com"),
    SemanticNetwork("Lions", "Information about Lions, their habits, ranges, diets, etc", "http://lions.com"),
    SemanticNetwork("Cats", "Information about house cats, their habits, naps, diets, etc", "http://cats.com")
]

queries = [
    "Where do big wild cats live?",
    # "When was the last commit to the ReasonAbleAI repo?",
]

attempts = 2

prompt_env = Environment(loader=FileSystemLoader('../prompts'))
template = prompt_env.get_template('query_classifier.j2')

number_of_tests = len(queries) * len(models) * len(temperatures) * attempts

results = []

for query in queries:
    reasoning_prompt = template.render(prompt=query, compentencies=compentencies)

    for model in models:
        for temperature in temperatures:
            for i in range(attempts):
                response = QueryLLM(reasoning_prompt).response['message']['content']
                results.append(results)

print(results)