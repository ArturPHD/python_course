python
import os
import json
import functools
from collections import defaultdict

class DataLoader:
    """A simple data loader that reads a file line by line."""
    def __init__(self, input_file):
        self.input_file = input_file

    def get_records(self):
        """A generator that yields records from the input file."""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()

class Job:
    """The main driver class for a FakeMapReduce job."""
    def __init__(self, data_loader, mapper, reducer, output_dir):
        self.data_loader = data_loader
        self.mapper = mapper
        self.reducer = reducer
        self.output_dir = output_dir
        self.intermediate_dir = os.path.join(self.output_dir, 'intermediate')
        
    def run(self):
        """Executes the full MapReduce job."""
        os.makedirs(self.intermediate_dir, exist_ok=True)
        
        print("--- 1. MAP PHASE ---")
        mapped_data = self._map_phase()
        self._save_intermediate_data(mapped_data, 'mapped_data.json')
        print(f"Mapped {len(mapped_data)} pairs.")
        
        print("\n--- 2. SHUFFLE & SORT PHASE ---")
        shuffled_data = self._shuffle_phase(mapped_data)
        self._save_intermediate_data(shuffled_data, 'shuffled_data.json')
        print(f"Shuffled into {len(shuffled_data)} unique keys.")

        print("\n--- 3. REDUCE PHASE ---")
        reduced_data = self._reduce_phase(shuffled_data)
        
        self._save_final_results(reduced_data)
        print(f"Reduced to {len(reduced_data)} final results.")
        
        return [(item['key'], item['value']) for item in reduced_data]

    def _map_phase(self):
        mapped_data = []
        for record in self.data_loader.get_records():
            for key, value in self.mapper(record):
                mapped_data.append({'key': key, 'value': value})
        return mapped_data

    def _shuffle_phase(self, mapped_data):
        shuffled = defaultdict(list)
        for item in mapped_data:
            key_tuple = tuple(item['key'])
            shuffled[key_tuple].append(item['value'])
        return dict(shuffled)

    def _reduce_phase(self, shuffled_data):
        reduced_data = []
        for key, values in shuffled_data.items():
            if not values:
                continue
            # Use functools.reduce to apply the pairwise reducer iteratively
            final_value = functools.reduce(self.reducer, values)
            reduced_data.append({'key': key, 'value': final_value})
        return reduced_data

    def _save_intermediate_data(self, data, filename):
        path = os.path.join(self.intermediate_dir, filename)
        data_to_save = {str(k): v for k, v in data.items()} if isinstance(data, dict) else data
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2)

    def _save_final_results(self, data):
        path = os.path.join(self.output_dir, 'results.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)