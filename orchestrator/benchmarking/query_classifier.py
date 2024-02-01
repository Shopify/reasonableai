import json
from tqdm import tqdm
import numpy as np
from prettytable import PrettyTable
from jinja2 import Environment, FileSystemLoader
from src.models.ability import Ability
from src.models.semantic_network import SemanticNetwork
from src.utils.query_llm import QueryLLM

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def calculate_consistency(results):
    for result in results:
        ratios = [run['ratios'] for run in result['runs']]
        consistencies = []
        for i in range(len(ratios[0])):
            relevance_scores = [ratio[i]['relevance'] for ratio in ratios]
            confidence_scores = [ratio[i]['confidence'] for ratio in ratios]
            consistencies.append({
                'topic name': ratios[0][i]['topic name'],
                'relevance consistency': np.std(relevance_scores),
                'relevance max': max(relevance_scores),
                'relevance min': min(relevance_scores),
                'relevance avg': np.mean(relevance_scores),
                'relevance median': np.median(relevance_scores),
                'confidence consistency': np.std(confidence_scores),
                'confidence max': max(confidence_scores),
                'confidence min': min(confidence_scores),
                'confidence avg': np.mean(confidence_scores),
                'confidence median': np.median(confidence_scores)
            })
        result['consistency'] = consistencies
        print(f"Consistency for query '{result['query']}' with model '{result['model']}' and temperature {result['temperature']}: {consistencies}")

def calculate_timings(results):
    for result in results:
        for timing in ['prompt_eval_duration_seconds']:
            timings = [run[timing] for run in result['runs']]
            result[timing + '_max'] = max(timings)
            result[timing + '_avg'] = sum(timings) / len(timings)

def pretty_print_results(results):
    table = PrettyTable()
    table.field_names = ["Query", "Model", "Temperature", "Topic", "Relevance Consistency", "Relevance Max", "Relevance Min", "Relevance Avg", "Relevance Median", "Confidence Consistency", "Confidence Max", "Confidence Min", "Confidence Avg", "Confidence Median", "Max Prompt Eval Duration", "Avg Prompt Eval Duration"]
    for result in results:
        for consistency in result['consistency']:
            table.add_row([result['query'], result['model'], result['temperature'], consistency['topic name'], consistency['relevance consistency'], consistency['relevance max'], consistency['relevance min'], consistency['relevance avg'], consistency['relevance median'], consistency['confidence consistency'], consistency['confidence max'], consistency['confidence min'], consistency['confidence avg'], consistency['confidence median'], result['prompt_eval_duration_seconds_max'], result['prompt_eval_duration_seconds_avg']])
    print(table)

def benchmark():

    models = [
        'deepseek-llm:67b-chat',
        # 'dolphin2.2-mistral:latest',
        'mistral:latest',
        'mixtral:latest',
        # 'orca-mini:13b',
        # 'orca-mini:7b',
        # 'phi:latest',
        # 'samantha-mistral:latest',
    ]

    temperatures = [0.0, 0.2, 0.5]

    compentencies = [
        Ability("GitHub", "Read GitHub repos, create pull requests and issues", "http://github.com"),
        Ability("Researcher", "Search the web information, returns appropriate documents. Useful for finding facts", "http://google.com"),
        SemanticNetwork("Tigers", "Information about Tigers, their habits, ranges, diets, etc", "http://tigers.com"),
        SemanticNetwork("Lions", "Information about Lions, their habits, ranges, diets, etc", "http://lions.com"),
        SemanticNetwork("Cats", "Information about house cats, their habits, naps, diets, etc", "http://cats.com")
    ]

    queries = [
        "Where do big wild cats live?",
        "When was the last commit to the ReasonAbleAI repo?",
    ]

    runs = 5

    prompt_env = Environment(loader=FileSystemLoader('prompts'))
    template = prompt_env.get_template('query_classifier.j2')

    number_of_tests = len(queries) * len(models) * len(temperatures) * runs
    print(f"Running {number_of_tests} tests")

    results = []

    pbar = tqdm(total=number_of_tests)

    for query in queries:
        prompt = template.render(prompt=query, compentencies=compentencies)
        for model in models:
            for temperature in temperatures:
                details = {
                    "query": query,
                    "model": model,
                    "temperature": temperature,
                    "runs": []
                }
                for i in range(runs):
                    tqdm.write(f"Benchmarking: '{query}', model: '{model}', temperature: {temperature}, run: {i+1} of {runs}")

                    response = QueryLLM(
                        prompt=prompt,
                        model=model,
                        temperature=temperature,
                        json_response=True,

                    ).response

                    details['runs'].append({
                        "ratios": response['message']['content']['ratios'],
                        "prompt_eval_duration_seconds": response['prompt_eval_duration'] / 1000000.0,
                        "eval_count": response['eval_count'],
                    })

                    pbar.update()

                results.append(details)

    pbar.close()

    calculate_consistency(results)
    calculate_timings(results)

    pretty_print_results(results)

    save_to_json(results, 'benchmarking/query_classifier.json')

if __name__ == '__main__':
    benchmark()
