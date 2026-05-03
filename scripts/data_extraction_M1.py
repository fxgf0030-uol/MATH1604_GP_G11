"""
data_extraction_M1.py

This file reads a quiz answer text file and saves the answers as numbers.
"""

from pathlib import Path


def extract_answers_sequence(file_path):
    """
    Read one answer file and return a list of 100 numbers.

    1, 2, 3, and 4 mean the selected answer.
    0 means the question was not answered.
    """

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"The input file does not exist: {file_path}")

    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    answers = []
    current_options = []

    for line in lines:
        line = line.strip()

        if line.startswith("Question "):
            if current_options:
                selected_answer = _parse_single_question(current_options)
                answers.append(selected_answer)
                current_options = []

        elif line.startswith("["):
            current_options.append(line)

    if current_options:
        selected_answer = _parse_single_question(current_options)
        answers.append(selected_answer)

    if len(answers) != 100:
        raise ValueError(
            f"Expected 100 answers, but extracted {len(answers)} answers."
        )

    return answers


def _parse_single_question(option_lines):
    """
    Check one question and return the selected answer number.

    Return 0 if no answer was selected.
    """

    if len(option_lines) != 4:
        raise ValueError(
            f"Each question should have 4 options, but found {len(option_lines)}."
        )

    selected_options = []

    for option_number, option_line in enumerate(option_lines, start=1):
        if option_line.lower().startswith("[x]"):
            selected_options.append(option_number)

    if len(selected_options) > 1:
        raise ValueError(
            f"More than one selected answer was found: {selected_options}"
        )

    if len(selected_options) == 0:
        return 0

    return selected_options[0]


def write_answers_sequence(answers, n, destination_path):
    """
    Write the answer list to a text file.

    The file name is answers_list_respondent_n.txt.
    """

    if not isinstance(answers, list):
        raise TypeError("answers must be provided as a list.")

    if len(answers) != 100:
        raise ValueError(
            f"answers must contain exactly 100 values, but got {len(answers)}."
        )

    valid_answers = {0, 1, 2, 3, 4}

    for answer in answers:
        if answer not in valid_answers:
            raise ValueError(
                "answers may only contain the values 0, 1, 2, 3, and 4."
            )

    if not isinstance(n, int):
        raise TypeError("n must be an integer.")

    if n <= 0:
        raise ValueError("n must be a positive integer.")

    output_folder = Path(destination_path)
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / f"answers_list_respondent_{n}.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        for answer in answers:
            file.write(f"{answer}\n")
