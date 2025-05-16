class EntityNotFoundException(Exception):
    def __init__(self, entity_class, entity_id):
        self.entity_name = entity_class.__qualname__
        self.entity_id = entity_id
        msg = f"{self.entity_name} with id {self.entity_id} not found"
        super().__init__(msg)
