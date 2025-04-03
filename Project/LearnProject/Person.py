import random

class Person:
    _used_id = set()  # Class-level attribute for tracking used IDs
    
    def __init__(self, name):
        self._name = name  
        self.id = self.generate_unique_id()

    @property
    def name(self):
        return self._name
    
    @name.setter 
    def name(self, value):  # Fixed method name
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @classmethod
    def generate_unique_id(cls):
        while True:
            new_id = random.randint(1_0000, 99_999)
            if new_id not in cls._used_id: 
                cls._used_id.add(new_id)
                return new_id
    
    

