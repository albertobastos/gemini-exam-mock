import json
import re

def markdown_to_json(input_filepath, output_filepath):
    questions = []
    unique_topics = set()
    current_topic = ""
    current_question = None
    current_q_num = 0

    # Regular expressions to identify the different parts of the markdown
    topic_pattern = re.compile(r'^\*\*(Tema\s+.*?)\*\*$')
    # Captured group 1 is the question number, group 2 is the text
    question_pattern = re.compile(r'^\*\*Pregunta\s+(\d+)\.\*\*\s+(.*)$')
    answer_pattern = re.compile(r'^\*\s+\*\*([A-Z]\).*?)\*\*\s+(.*)$')

    def validate_question(q, q_num, topic):
        """Checks if a question has exactly one correct answer."""
        correct_count = sum(1 for ans in q["respostes"] if ans[1] is True)
        if correct_count != 1:
            print(f"⚠️ WARNING: In '{topic}', Pregunta {q_num} has {correct_count} correct answers (expected exactly 1).")

    with open(input_filepath, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue

            # 1. Check for a Topic header
            topic_match = topic_pattern.match(line)
            if topic_match:
                current_topic = topic_match.group(1).strip()
                unique_topics.add(current_topic)
                continue

            # 2. Check for a Question
            question_match = question_pattern.match(line)
            if question_match:
                # If we were already parsing a question, validate and save it
                if current_question:
                    validate_question(current_question, current_q_num, current_topic)
                    questions.append(current_question)
                
                current_q_num = question_match.group(1)
                enunciat = question_match.group(2).strip()
                current_question = {
                    "tema": current_topic,
                    "enunciat": enunciat,
                    "respostes": []
                }
                continue

            # 3. Check for an Answer
            answer_match = answer_pattern.match(line)
            if answer_match and current_question is not None:
                correct_indicator = answer_match.group(1)
                answer_text = answer_match.group(2).strip()
                
                is_correct = "(Correcta)" in correct_indicator
                
                # Format as a two-item list: [Answer String, Boolean]
                current_question["respostes"].append([answer_text, is_correct])
                continue

    # Don't forget to validate and append the very last question in the file
    if current_question:
        validate_question(current_question, current_q_num, current_topic)
        questions.append(current_question)

    # Write the structured data to a JSON file
    with open(output_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(questions, json_file, ensure_ascii=False, indent=2)
    
    # 4. Print Summary
    print("\n--- Parsing Summary ---")
    print(f"Topics detected: {len(unique_topics)}")
    print(f"Questions processed: {len(questions)}")
    print(f"Output successfully saved to: '{output_filepath}'\n")

if __name__ == "__main__":
    markdown_to_json("001.md", "questions.json")