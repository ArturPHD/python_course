from FakeMapReduceFramework import DataLoader, Job
import os
import string

def word_count_mapper(line):
    """Mapper for the Word Count task."""
    line = line.translate(str.maketrans('', '', string.punctuation))
    words = line.lower().split()
    for word in words:
        if word:
            yield (word, 1)

def word_count_reducer(accumulator, next_value):
    """Reducer for the Word Count task. It's a simple pairwise sum."""
    return accumulator + next_value

def run_word_count():
    """Sets up and runs the Word Count job."""
    input_file = os.path.join('data', 'word_count_input.txt')
    output_dir = os.path.join('output', 'word_count_results')
    
    loader = DataLoader(input_file)
    job = Job(loader, word_count_mapper, word_count_reducer, output_dir)
    
    print("Running Word Count example...")
    final_results = job.run()
    
    print(f"\nWord Count finished! Results are in '{output_dir}'.")
    print("Final counts (sorted):")
    for key, value in sorted(final_results):
        print(f"{key}: {value}")

if __name__ == '__main__':
    run_word_count()