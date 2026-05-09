import matplotlib.pyplot as plt


def generate_means_sequence(collated_answers_path):
    """
    Generates a sequence of mean answer values per question across all participants.


    Definition
    -----------
        This function reads a structured text file (collated answers) containing participants' answers,
        extracts selected answers per question, and computes the mean response for each question
        across all participants (ignoring unanswered questions marked as 0).


    Parameters
    -----------
        collated_answers_path (str): Path to the text file containing collated participant answers.


    Returns
    -----------
        list[float]: A list of mean values, one per question.
    """

    def extract_answers(participant):

        """
        Extracts selected answers for a single participant.


        Definition
        -----------
            Each question is assumed to have a block of 4 possible answers,
            with the selected answer marked by '[X]'. If no answer is selected,
            0 is recorded for that question.


        Parameters
        -----------
            participant (list[str]): Lines corresponding to a single participant.


        Returns
        -----------
            list[int]: List of selected answer indices (1-4), or 0 if unanswered.
        """

        answers = []
        # iterate through all elements of this list of lines of one participant
        for index, line in enumerate(participant):

            # define a question group for each question
            if "Question " in line:
                
                question_group = participant[index+1: index+5]
                checker_iteration = 0
                # iterate through answers of that question group
                for smaller_index, answer in enumerate(question_group):
                    # identify which answer is taken
                    if "[X]" in answer:
                        answer_number = smaller_index + 1
                        answers.append(answer_number)
                        break
                    else:
                        # if an answer doesn't contain [X] then increase check count by 1
                        checker_iteration += 1
                # if check count was made for all answers then no answer was given therefore 0
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
    """
    Visualizes participant answer data using matplotlib.


    Parameters
    -----------
        collated_answers_path (str): Path to the text file containing collated participant answers.
        n (int): Visualization mode selector (1 or 2).


    Returns
    -----------
        Supports two visualization modes:
        - n == 1: scatter plot of mean answers per question
        - n == 2: line plots of individual participant responses


    Raises
    -----------
        Exception: If n is not 1 or 2.
    """

    # One participant data from the collated answers file transformed into a list of lines
    def extract_answers(participant):
        """
        Extracts selected answers for a single participant.


        Definition
        -----------
            Each question is assumed to have a block of 4 possible answers,
            with the selected answer marked by '[X]'. If no answer is selected,
            0 is recorded for that question.


        Parameters
        -----------
            participant (list[str]): Lines corresponding to a single participant.


        Returns
        -----------
            list[int]: List of selected answer indices (1-4), or 0 if unanswered.
        """

        answers = []
        # iterate through all elements of this list of lines of one participant
        for index, line in enumerate(participant):

            # define a question group for each question
            if "Question " in line:
                
                question_group = participant[index+1: index+5]
                checker_iteration = 0
                # iterate through answers of that question group
                for smaller_index, answer in enumerate(question_group):
                    # identify which answer is taken
                    if "[X]" in answer:
                        answer_number = smaller_index + 1
                        answers.append(answer_number)
                        break
                    else:
                        # if an answer doesn't contain [X] then increase check count by 1
                        checker_iteration += 1
                # if check count was made for all answers then no answer was given therefore 0
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

    means = generate_means_sequence(collated_answers_path)
    # Plots using matplotlib.pyplot according to the input (n)

    plt.figure(figsize=(10, 5))
    plt.grid(True)

    # Scatter plot of means
    if n == 1:
        plt.scatter(range(1, 101), means)
        plt.xlabel("Question Number")
        plt.ylabel("Mean Answer Value")
        plt.title("Meane Answer Value per Question")
        plt.show()
    elif n == 2:
        # Line plots for every individual answers
        for answer in smaller_groups:
            plt.plot([i + 1 for i in range(len(answer))], answer, alpha=0.5)
        plt.xlabel("Question Number")
        plt.ylabel("Answers Value")
        plt.title("Individual Answer Sequences")
        plt.show()
    else:
        raise Exception("The second given input (n) should be either 1 or 2")


