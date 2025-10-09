from FakeMapReduceFramework import DataLoader, Job
import os

def exam_mapper(line):
    """Mapper for the exam problem."""
    parts = line.strip().split()
    if not parts:
        return

    # Check for room availability data
    if parts[0] in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']:
        day = parts[0]
        for hour_str in parts[1:]:
            if hour_str.isdigit():
                yield ((day, int(hour_str)), (True, [])) # (is_available, [friends])

    # Assume it's friend preference data
    else:
        name = line[:12].strip()
        time_slots = line[12:].split()[1:]
        
        i = 0
        while i < len(time_slots):
            day, hour_str = time_slots[i], time_slots[i+1]
            if hour_str.isdigit():
                yield ((day, int(hour_str)), (False, [name])) # (is_available, [friends])
            i += 2

def exam_reducer(accumulator, next_value):
    """
    Pairwise reducer for the exam problem.
    Accumulator: (is_available_so_far, [friends_so_far])
    Next Value:  (is_available_in_this_record, [friend_from_this_record])
    """
    is_available = accumulator[0] or next_value[0]
    combined_friends = accumulator[1] + next_value[1]
    return (is_available, combined_friends)

def format_exam_results(results, output_dir):
    """Formats the final results according to the exam's specifications."""
    valid_slots = []
    for (day, hour), (is_available, friends) in results:
        if is_available and len(friends) > 3:
            valid_slots.append(((day, hour), (len(friends), sorted(friends))))
            
    sorted_results = sorted(valid_slots, key=lambda item: item[1][0], reverse=True)

    output_file_path = os.path.join(output_dir, 'final_results.txt')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for (day, hour), (count, names) in sorted_results:
            f.write(f"{day} {hour} {count}\n")
            for name in names:
                f.write(f"{name}\n")
    print(f"Formatted results written to {output_file_path}")

def run_exam_solver():
    """Sets up and runs the exam problem job."""
    input_file = os.path.join('data', 'exam_input.txt')
    output_dir = os.path.join('output', 'exam_results')
    
    loader = DataLoader(input_file)
    job = Job(loader, exam_mapper, exam_reducer, output_dir)
    
    print("\nRunning Exam Problem solver...")
    exam_raw_results = job.run()
    
    format_exam_results(exam_raw_results, output_dir)
    print(f"Exam Problem finished! Results are in '{output_dir}/final_results.txt'.")

if __name__ == '__main__':
    run_exam_solver()