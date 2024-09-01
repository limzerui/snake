import json
import math
from collections import defaultdict

def euclidean_distance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

def calculate_weightage(student, school):
    # Weightage for distance (50%)
    distance = euclidean_distance(student['homeLocation'], school['location'])
    distance_score = 50 / (1 + distance)  # Closer distance gives a higher score

    # Weightage for alumni (30%)
    alumni_score = 30 if 'alumni' in student and student['alumni'] == school['name'] else 0

    # Weightage for volunteer (20%)
    volunteer_score = 20 if 'volunteer' in student and student['volunteer'] == school['name'] else 0

    return distance_score + alumni_score + volunteer_score

def allocate_students(input_data):
    schools = input_data['schools']
    print(f"{schools}")
    students = input_data['students']
    print(f"{students}")

    school_scores = defaultdict(list)

    # Calculate weightage for each student for each school
    for student in students:
        for school in schools:
            score = calculate_weightage(student, school)
            school_scores[school['name']].append((score, student['id']))

    school_allocation = defaultdict(list)
    for school in schools:
        name = school['name']
        max_alloc = school['maxAllocation']
        sorted_students = sorted(school_scores[name], key=lambda x: (-x[0], x[1]))
        allocated_students = [student_id for _, student_id in sorted_students[:max_alloc]]
        school_allocation[name] = allocated_students

    return school_allocation

def main():
    # Read input data
    with open('input.json', 'r') as infile:
        input_data = json.load(infile)

    # Allocate students to schools
    allocation = allocate_students(input_data)

    # Format the output
    output = [{school: students} for school, students in allocation.items()]

    # Write output to JSON file
    with open('output.json', 'w') as outfile:
        json.dump(output, outfile, indent=4)

if __name__ == "__main__":
    main()
