class Desire:
    def __init__(self, name, description, priority):
        self.name = name
        self.description = description
        self.priority = priority

    def __repr__(self):
        return f"Desire(name='{self.name}', description='{self.description}', priority={self.priority})"
