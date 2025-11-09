#!/usr/bin/env python3
import json
import re
import os

# Read the JSON file
with open('datasets/zbrojak_full.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Get all image files
image_files = os.listdir('data/img')

# Create a mapping of question numbers to image files
question_to_image = {}

for img_file in image_files:
    if not img_file.endswith('.png'):
        continue
    
    # Extract question numbers from filename
    # Examples: 608.png, 656-657.png, 649-651.png
    base_name = img_file.replace('.png', '')
    
    if '-' in base_name:
        # Range of questions (e.g., 656-657)
        parts = base_name.split('-')
        start = int(parts[0])
        end = int(parts[1])
        for q_num in range(start, end + 1):
            question_to_image[q_num] = f"data/img/{img_file}"
    else:
        # Single question (e.g., 608)
        q_num = int(base_name)
        question_to_image[q_num] = f"data/img/{img_file}"

# Add image field to questions
for question in questions:
    name = question.get('name', '')
    
    # Extract question number from name (e.g., "608. Some text..." -> 608)
    match = re.match(r'^(\d+)\.', name)
    if match:
        q_num = int(match.group(1))
        if q_num in question_to_image:
            question['image'] = question_to_image[q_num]
            print(f"Added image to question {q_num}: {question_to_image[q_num]}")

# Write back to file
with open('datasets/zbrojak_full.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"\nDone! Processed {len(questions)} questions.")
print(f"Found {len(question_to_image)} question-to-image mappings.")
