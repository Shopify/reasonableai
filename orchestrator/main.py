from src.query_classifier.query_classifier import QueryClassifier
class Orchestrator():
    prompt = "> "

    def chat_loop(self):
        while True:
            query = input(self.prompt)
            print(query)
            if query == "exit":
                exit(0)
            else:
                response = QueryClassifier(query).classify()
                print(response)

if __name__ == '__main__':
    Orchestrator().chat_loop()
