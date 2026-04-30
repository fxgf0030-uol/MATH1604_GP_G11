def generate_means_sequence(collated_answers_path):


    # One participant data from the collated answers file transformed into a list of lines
    def extract_answers(participant):

        answers = []
        for index, line in enumerate(participant):

            if "Question " in line:

                question_group = participant[index+1: index+5]
                checker_iteration = 0

                for smaller_index, answer in enumerate(question_group):
                    
                    if "[X]" in answer:
                        answer_number = smaller_index + 1
                        answers.append(answer_number)
                        break
                    else:
                        checker_iteration += 1
                    
                if checker_iteration >= 4:
                    answers.append(0)
            else:
                continue
            

        # a list of numbers of answers for each individual
        return answers

        
    # Reads the data with each line as an element in the list
    with open(collated_answers_path, "r") as coll:
        lines = coll.readlines()

    # Initialize a list that will contain smaller lists of answer values to every question
    # for every participant as a single (smaller) list
    smaller_groups = []
    
    # Initalize a list that is updated every 100 (or less) answers of every participant
    # That is then appended into the smaller groups
    individual_list = []

    # Looping the lines list until a star is found
    for index, line in enumerate(lines):

        # Checks if star was the first element in the file then stop
        # or else continue the implementation
        if line.strip() == "*":
            # Updates both the question group list and the participant list
            smaller_groups.append(extract_answers(individual_list))
            individual_list = []
        else:
            # Updates elements in the smaller participant list with every anwer until the (*)
            individual_list.append(line)

    # Last check if a star was not present for the last participant
    if individual_list:
        smaller_groups.append(extract_answers(individual_list))
        
    means = []
    for question in range(0, 100):

        question_answers = []
        
        # Extracting the question answer through its index from the previous loop
        for individual in smaller_groups:

            # Using that index to find eevry participant's answer to it
            answer = individual[question]
            # ignoring the no-answer questions in the calculation
            if answer != 0:
                question_answers.append(answer)

        # After looping through every answer, calculate the mean for i'th question
        # and repeat the loop for every given question.
        means.append(sum(question_answers)/len(question_answers))        

    return means



def visualize_data(collated_answers_path, n):
    
    means = generate_means_sequence(collated_answers_path)

    # Reads the data with each line as an element in the list
    with open(collated_answers_path, "r") as coll:
        lines = coll.readlines()

    # Initialize a list that will contain smaller lists of answer values to every question
    # for every participant as a single (smaller) list
    smaller_groups = []
    
    # Initalize a list that is updated every 100 answers of every participant
    # That is then appended into the smaller groups
    individual_list = []

    # Looping the lines list until a star is found
    for index, line in enumerate(lines):

        # Checks if star was the first element in the file then stop
        # or else continue the implementation
        if "*" in line:
            if index != 0:
                # Updates both the question group list and the participant list
                smaller_groups.append(individual_list)
                individual_list = []
            else:
                continue
        else:
            # Updates elements in the smaller participant list with every anwer until the (*)
            individual_list.append(int(line.strip()))

    # Last check if a star was not present for the last participant
    if individual_list:
        smaller_groups.append(individual_list)

    # Plots using matplotlib.pyplot according to the input (n)
    # Scatter plot of means
    if n == 1:
        plt.scatter(range(1, 101), means)
        plt.xlabel("Question Number")
        plt.ylabel("Answers Mean")
        plt.show()
    elif n == 2:
        # Line plots for every individual answers
        for answer in smaller_groups:
            plt.plot(range(1, 101), answer, alpha=0.5)
        plt.xlabel("Question Number")
        plt.ylabel("Answers Value")
        plt.show()
    else:
        raise Exception("The second given input (n) should be either 1 or 2")

        