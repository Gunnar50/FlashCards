
def get_questions():
    questions = []

    with open('questions_files/final_exame.txt', 'r') as questionsImport:
        temp = []
        lines = questionsImport.read().splitlines()
        choices = []
        is_choice = True
        for i, line in enumerate(lines):
            if len(temp) > 0 and is_choice:
                if line == ".":
                    temp.append(choices)
                    choices = []
                    is_choice = False
                    continue
                choices.append(line)
                continue

            if line == "!":
                questions.append(temp)
                temp = []
                is_choice = True
            else:
                temp.append(line)

    return questions


# for q in get_questions():
#     print(q)



