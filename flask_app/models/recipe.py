class Recipe:
    def __init__(self,data):
        self.name = data["name"]
        self.under_thirty = data["under_thirty"]
        self.instructions = data["instructions"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]