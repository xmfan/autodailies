import csv
from typing import Optional

from model.instruction import Instruction

class Routine:
    instructions = []
    
    def __init__(self, path: str) -> None:
        # Open the CSV file in read mode
        with open(path, 'r') as file:
            # Create a CSV reader object
            reader = csv.reader(file)
        
            # Skip the first row
            next(reader)
        
            # Iterate over each remaining row in the CSV file
            for angle, dist in reader:
                self.instructions.append(Instruction(float(angle), float(dist)))

    def next(self) -> Optional[Instruction]:
        if not self.instructions:
            return None
            
        return self.instructions.pop(0)

        