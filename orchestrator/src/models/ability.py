class Ability:
    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url

    def __repr__(self):
        return f"Ability(name='{self.name}', description='{self.description}')"