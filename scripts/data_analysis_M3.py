def generate_means_sequence(collated_answers_path):

    # reading the file
    with open(collated_answers_path, "r") as coll:
        lines = coll.readlines()

    smaller_groups = []
    
    # creating respondents groups
    for index in range(0, len(lines), 101):
        individual_group = []
        for line in lines[index: index+100]:
            if line.rstrip() != 0:
                individual_group.append(int(line.rstrip()))
            else:
                pass
        smaller_groups.append(individual_group)

    # iterating through each question and using its index on each
    # respondent group from the generated above to access the answer of it from each one
    means = []
    for question in range(0, 100):
        question_answers = []
        for individual in smaller_groups:
            answer = individual[question]
            if answer == 0:
                pass
            else:
                question_answers.append(answer)
        # compute means and then append
        means.append(sum(question_answers)/len(question_answers))

    return means
# Test
print(generate_means_sequence("mock/M_output/collated.txt"))