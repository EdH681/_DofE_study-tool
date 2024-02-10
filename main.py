import json
import tkinter
import tkinter.ttk as ttk
import tkinter.messagebox
import os
import random
import subprocess

# FONTS
font = "Helvetica"
size20b = (font, 20, "bold")
size12b = (font, 12, "bold")
size09b = (font, 9, "bold")

size20 = (font, 20)
size18 = (font, 18)
size15 = (font, 15)
size12 = (font, 12)
size10 = (font, 10)
size09 = (font, 9)


def menu_button(frame):
    button = tkinter.Button(frame, text="Menu", command=lambda: menu(frame))
    button.place(x=14, y=45, height=30)


def load(subject, topic):
    with open(f"subjects/{subject}.json", "r") as retrieve:
        data = json.load(retrieve)[topic]
    questions = []
    for i in data:
        pair = (i, data[i])
        questions.append(pair)
    return questions


def check(attempt, answer, threshold=2):
    answer = answer.replace(" ", "")
    attempt = attempt.replace(" ", "")
    threshold = len(answer) - threshold
    answer = [*answer]
    correct = 0
    for i in attempt:
        if i in answer:
            correct += 1
            answer.remove(i)
        else:
            print(i)

    return correct > threshold


def clear(frame):
    for item in frame.winfo_children():
        item.destroy()


def get_subjects():
    options = ["Select an option"]
    for subject in os.listdir("subjects"):
        if subject.split(".")[1] == "json":
            options.append(subject.split(".")[0].title())
    return options


def menu(frame):
    clear(frame)
    baseY = 200
    titleText = "Select an Option"
    title = tkinter.Label(frame, text=titleText, font=size20b)
    title.place(relx=0, y=20, width=500, height=50)

    # Test Button
    startText = "Test Yourself"
    testYourself = tkinter.Button(frame, text=startText, font=size20, command=lambda: selection(frame))
    testYourself.place(x=50, y=baseY, width=400, height=50)

    # Add Button
    addText = "Add More Question Sets"
    addButton = tkinter.Button(frame, text=addText, font=size20, command=lambda: add_menu(frame))
    addButton.place(x=50, y=baseY + 55, width=400, height=50)

    # View Button
    viewText = "View All Question Sets"
    viewButton = tkinter.Button(frame, text=viewText, font=size20, command=lambda: viewer_menu(frame))
    viewButton.place(x=50, y=baseY + 110, width=400, height=50)

    # Remove Button
    removeText = "Remove a Question Set"
    removeButton = tkinter.Button(frame, text=removeText, font=size20, command=lambda: remove_menu(frame))
    removeButton.place(x=50, y=baseY + 165, width=400, height=50)


# QUIZ =================================================================================================================
def selection(frame):
    clear(frame)

    # Getting Subjects
    options = get_subjects()

    # Title
    title = tkinter.Label(frame, text="Select a Subject and a Topic", font=size20b)
    title.pack(pady=10)

    # Topic Box
    tkinter.Label(frame, text="Select a Topic", font=size12b).place(x=105, y=215)
    topicSelect = ttk.Combobox(frame, values=["Select an Option"], state="disabled", width=42)
    topicSelect.current(0)
    topicSelect.place(x=105, y=250)

    # Subject Box
    tkinter.Label(frame, text="Select a Subject", font=size12b).place(x=105, y=115)
    subjectSelect = ttk.Combobox(frame, values=options, width=20, font=size10, state="readonly")
    subjectSelect.current(0)
    subjectSelect.place(x=105, y=150)

    # Subject Button
    subjectButton = tkinter.Button(frame, text="Select",
                                   command=lambda: subject_check(subjectSelect.get(), topicSelect))
    subjectButton.place(x=275, y=150, width=100, height=22)

    # Start Button
    startButton = tkinter.Button(frame, text="Start", font=size20,
                                 command=lambda: question_grab(frame, subjectSelect.get(), topicSelect.get()))
    startButton.place(x=105, y=350, width=280, height=50)

    # Return to Menu
    menu_button(frame)


def subject_check(value, box):
    if value != "Select an option":
        box["state"] = "readonly"
        topics = ["Select an option"]
        with open(f"subjects/{value}.json", "r") as topicList:
            data = json.load(topicList)
            for topic in data:
                topics.append(topic)
        box["values"] = topics
    else:
        box['state'] = "disabled"
        box["values"] = ["Select an Option"]
        box.current(0)


def question_grab(frame, subject, topic):
    try:
        questions = load(subject.lower(), topic.lower())
    except KeyError as e:
        tkinter.Label(frame, text="Select a valid topic", fg="red", font=size09).place(x=105, y=400, width=280)
        print(e)
    except FileNotFoundError as e:
        tkinter.Label(frame, text="Select a valid subject", fg="red", font=size09).place(x=105, y=400, width=280)
    else:
        quiz(frame, questions)


def quiz(frame, questions, questionNumber=1, correct=0, incorrect=0):
    clear(frame)
    random.shuffle(questions)
    title = tkinter.Label(frame, text=f"Question {questionNumber}", font=size20b)
    title.place(x=0, y=10, width=500, height=50)

    if questions:
        questionAnswer = questions.pop(0)

        question = tkinter.Label(frame, text=questionAnswer[0], font=size18, wraplength=455)
        question.place(x=0, y=100, width=500, height=150)

        answerBox = tkinter.Entry(frame, font=size18, justify="center")
        answerBox.place(x=50, y=300, height=50, width=400)

        submitButton = tkinter.Button(frame, text="Submit", font=size15,
                                      command=lambda: quiz_check(frame, answerBox.get(), questionAnswer, questions,
                                                                 questionNumber, correct, incorrect))
        submitButton.place(x=150, y=360, height=40, width=200)

        returnButton = tkinter.Button(frame, text="Return", command=lambda: selection(frame))
        returnButton.place(x=10, y=470, width=50, height=25)
    else:
        quiz_complete(frame, correct, incorrect)


def quiz_check(frame, entered, questionAnswer, questions, questionNumber, correct, incorrect):
    right = check(entered.lower(), questionAnswer[1])
    questionNumber += 1
    if right:
        correctLabel = (tkinter.Label(frame, text="Correct", fg="green", font=size12))
        correctLabel.place(x=0, y=270, width=500, height=30)
        correct += 1
    else:
        incorrectText = f"Incorrect, it was {questionAnswer[1]}"
        incorrectLabel = tkinter.Label(frame, text=incorrectText, fg="red", font=size12)
        incorrectLabel.place(x=0, y=270, width=500, height=30)
        incorrect += 1

    continueButton = tkinter.Button(frame, text="Continue", font=size10,
                                    command=lambda: quiz(frame, questions, questionNumber, correct, incorrect))
    continueButton.place(x=200, y=405, width=100, height=30)


def quiz_complete(frame, correct, incorrect):
    clear(frame)
    tkinter.Label(frame, text="Quiz Complete", font=size20b).pack()
    correctAnswered = tkinter.Label(frame, text=f"{correct} correctly answered", font=size20, fg="green")
    correctAnswered.place(x=0, y=200, width=500, height=50)
    incorrectAnswered = tkinter.Label(frame, text=f"{incorrect} incorrectly answered", font=size20, fg="red")
    incorrectAnswered.place(x=0, y=250, width=500, height=50)
    menuReturn = tkinter.Button(frame, text="Return to menu", font=size15, command=lambda: menu(frame))
    menuReturn.place(x=150, y=350, width=200, height=50)


# ADDING ===============================================================================================================
def add_menu(frame):
    clear(frame)
    title = tkinter.Label(frame, text="Add a New Study Set", font=size20b)
    title.pack(pady=10)

    howToText = """
    1. create a text file anywhere on your computer\n
    2. name the file <topic name>.txt\n
    3. type the question then the answer with a separator between them\n
    4. copy/paste the text file location into the box\n
    TIP: keep any text files in a folder so you can redo\nthem if something goes wrong
    """

    info = tkinter.Label(frame, text=howToText, font=size12)
    info.place(x=0, y=50, width=500, height=180)

    subjectTitle = tkinter.Label(frame, text="Enter the name of the subject", font=size10)
    subjectTitle.place(x=50, y=250)
    subject = tkinter.Entry(frame, justify="center", font=size12)
    subject.place(x=50, y=270, width=225, height=30)

    separatorTitle = tkinter.Label(frame, text="Select the separator", font=size10)
    separatorTitle.place(x=300, y=250)
    separators = ["Select an Option", "/", ",", ".", "-", "_"]
    separator = ttk.Combobox(frame, values=separators, state="readonly")
    separator.current(0)
    separator.place(x=300, y=275)

    fileTitle = tkinter.Label(frame, text="Enter the file location", font=size10)
    fileTitle.place(x=50, y=320)
    location = tkinter.Entry(frame, justify="center", font=size15)
    location.place(x=50, y=340, width=400, height=40)

    addSubmit = tkinter.Button(frame, text="Submit", font=size12,
                               command=lambda: add_checks(frame, subject.get(), separator.get(), location.get(),
                                                          subjectTitle, separatorTitle, fileTitle))
    addSubmit.place(x=150, y=410, width=200, height=30)

    menu_button(frame)


def add_checks(frame, subject, separator, filename, sub, sep, file):
    tiptop = True
    filename = filename.strip('"')

    # is a separator selected
    if separator == "Select an Option":
        sep["fg"] = "red"
        tiptop = False
    else:
        sep["fg"] = "black"

    # has a file been entered
    if not filename:
        tiptop = False
        file["fg"] = "red"
    else:
        file["fg"] = "black"

    # has a subject been entered
    if not subject:
        tiptop = False
        sub["fg"] = "red"
    else:
        sub["fg"] = "black"

    # does the text file exist
    fName = filename.split(".")[0]
    try:
        test = open(f"{fName}.txt", "r")
        test.close()
    except FileNotFoundError:
        file["fg"] = "red"
        tiptop = False
    else:
        file["fg"] = "black"

    # does the json file exist
    rawName = fName.split("\\")[-1].split(".")[0].lower()
    if os.path.exists(f"subjects/{subject}.json"):
        if subject:
            with (open(f"subjects/{subject}.json", "r") as find):
                search = json.load(find)
                exists = False
                for i in search:
                    if i == rawName:
                        existsError = tkinter.Label(frame, text=f"A topic with that name already exists under {subject}", fg="red", font=size09)
                        existsError.place(x=0, y=380, width=500)
                        tiptop = False
                        exists = True
                if not exists:
                    tkinter.Label(frame, text="", fg="red").place(x=0, y=380, width=500)
        else:
            tiptop = False

    if tiptop:
        add(frame, subject, rawName, filename, separator)


def add(frame, subject, topic, path, separator):
    try:
        with open(path, "r") as pull:
            full = pull.readlines()
            questions = [i.split(separator)[0].strip() for i in full]
            answers = [i.split(separator)[1].strip() for i in full]
    except IndexError:
        tkinter.Label(frame, text="You have a question without an answer", fg="red", font=size09).place(x=0, y=390, width=500)
    info = {}
    for q, a in zip(questions, answers):
        info[q] = a
    print(info)
    if not os.path.exists(f"subjects/{subject}.json"):
        with open(f"subjects/{subject}.json", "w") as create:
            json.dump({}, create)
    with open(f"subjects/{subject}.json", "r") as get:
        current = json.load(get)
    current[topic] = info
    try:
        with open(f"subjects/{subject}.json", "w") as send:
            json.dump(current, send)
    except json.JSONEncoder:
        tkinter.Label(frame, text="Error adding set", fg="red", font=size09).place(x=0, y=450, width=500)
    else:
        tkinter.Label(frame, text="Set added successfully", fg="green", font=size09).place(x=0, y=450, width=500)


# REMOVE ===============================================================================================================
def remove_menu(frame):
    clear(frame)

    tkinter.Label(frame, text="Remove a Set", font=size20b).pack()

    options = ["Select an option"]
    for subject in os.listdir("subjects"):
        if subject.split(".")[1] == "json":
            options.append(subject.split(".")[0].title())

    topicLabel = tkinter.Label(frame, text="Select the topic you want to delete", font=size12b)
    topicLabel.place(x=0, y=250, width=500)
    topicSelect = ttk.Combobox(frame, values=["Select an Option"], state="disabled", width=51)
    topicSelect.current(0)
    topicSelect.place(x=85, y=280)

    subjectLabel = tkinter.Label(frame, text="Select the subject to delete from", font=size12b)
    subjectLabel.place(x=0, y=120, width=500)
    subjectSelect = ttk.Combobox(frame, values=options, width=30, state="readonly")
    subjectSelect.current(0)
    subjectSelect.place(x=85, y=150)

    subButton = tkinter.Button(frame, text="Select", command=lambda: remove_check(subjectSelect.get(), topicSelect))
    subButton.place(x=315, y=150, height=22, width=100)

    submitButton = tkinter.Button(frame, text="Delete", font=size15, command=lambda: delete(frame, subjectSelect.get().lower(), topicSelect.get()))
    submitButton.place(x=150, y=320, width=200, height=40)

    tkinter.Label(frame, text="Alternatively, open the folder and edit the JSON file").place(x=0, y=400, width=500)
    fileButton = tkinter.Button(frame, text="Open Folder", font=size15, command=lambda: subprocess.Popen('explorer "subjects"'))
    fileButton.place(x=175, y=430, width=150, height=40)

    menu_button(frame)


def remove_check(value, box):
    if value != "Select an option":
        box["state"] = "readonly"
        topics = ["Select an option", "All of it"]
        with open(f"subjects/{value}.json", "r") as topicList:
            data = json.load(topicList)
            for topic in data:
                topics.append(topic)
        box["values"] = topics
    else:
        box['state'] = "disabled"
        box["values"] = ["Select an Option"]
        box.current(0)


def delete(frame, subject, topic):
    print()

    if topic == "All of it":
        if tkinter.messagebox.askyesno("Warning", f"Do you want to delete {subject}?"):
            try:
                os.remove(f"subjects/{subject}.json")
            except FileNotFoundError:
                tkinter.Label(frame, text="This subject doesn't exist", fg="red", font=size09).place(x=0, y=370, width=500)
            else:
                tkinter.Label(frame, text="Subject deleted successfully", fg="green").place(x=0, y=370, width=500)
    else:
        if tkinter.messagebox.askyesno("Warning", f"Do you want to delete {topic}?"):
            try:
                with open(f"subjects/{subject}.json", "r") as retrieve:
                    data = json.load(retrieve)
                del data[topic]
                with open(f"subjects/{subject}.json", "w") as update:
                    json.dump(data, update)
            except KeyError:
                tkinter.Label(frame, text="This topic doesn't exist", fg="red", font=size09).place(x=0, y=370, width=500)
            except FileNotFoundError:
                tkinter.Label(frame, text="Invalid selection", fg="red", font=size09).place(x=0, y=370, width=500)
            else:
                tkinter.Label(frame, text="Topic deleted successfully", fg="green", font=size09).place(x=0, y=370, width=500)


# VIEWING ==============================================================================================================
def viewer_menu(frame):
    clear(frame)

    viewerTitle = tkinter.Label(frame, text="Set Viewer", font=size20b)
    viewerTitle.pack()

    menu_button(frame)

    viewingArea = tkinter.Frame(frame, borderwidth=2, relief="ridge")
    viewingArea.place(x=50, y=200, width=400, height=250)

    topics = ["Select an option"]
    tkinter.Label(frame, text="Select the topic", font=size09b).place(x=250, y=80)
    topicSelect = ttk.Combobox(frame, values=topics, state="disabled")
    topicSelect.current(0)
    topicSelect.place(x=250, y=100)

    options = get_subjects()
    tkinter.Label(frame, text="Select the subject", font=size09b).place(x=100, y=80)
    subjectSelect = ttk.Combobox(frame, values=options, state="readonly")
    subjectSelect.current(0)
    subjectSelect.place(x=100, y=100)
    subjectSubmit = tkinter.Button(frame, text="Submit",
                                   command=lambda: subject_check(subjectSelect.get(), topicSelect))
    subjectSubmit.place(x=101, y=130, width=140, height=25)

    scroll = tkinter.Scrollbar(frame, relief="sunken", bd=2)
    scroll.place(x=450, y=200, height=250)

    contents = tkinter.Text(viewingArea, yscrollcommand=scroll.set, wrap="word")
    contents.pack()

    topicSubmit = tkinter.Button(frame, text="Submit", command=lambda: view_update(contents, subjectSelect.get().lower(), topicSelect.get(), frame))
    topicSubmit.place(x=250, y=130, width=140, height=25)


def view_update(display, subject, topic, frame):
    display.delete("1.0", "end")
    try:
        with open(f"subjects/{subject}.json", "r") as retrieve:
            topics = json.load(retrieve)[topic]
        questions = [(i, topics[i]) for i in topics]
        text = ""
        for question in questions:
            text = f"{text}\n{question[0]}\n>{question[1]}\n{'-' * 49}"

        display.insert(tkinter.END, text)
    except FileNotFoundError:
        tkinter.Label(frame, text="Invalid subject", fg="red", font=size09).place(x=0, y=165, width=500)
    except KeyError:
        tkinter.Label(frame, text="Invalid topic", fg="red", font=size09).place(x=0, y=165, width=500)
    else:
        tkinter.Label(frame, text="", fg="red", font=size09).place(x=0, y=165, width=500)


# MAIN =================================================================================================================
splashRoot = tkinter.Tk()
splashRoot.geometry(f"500x500")
splashRoot.title("")
nerd = tkinter.PhotoImage(file="assets/nerd.png")
tkinter.Label(splashRoot, image=nerd).place(relx=0.5, rely=0.5, anchor="center")

splashRoot.after(500, lambda: main(splashRoot))


def main(splash):
    splash.destroy()
    root = tkinter.Tk()
    root.iconbitmap("assets/nerd.ico")
    root.title("Academic Weaponiser")
    root.geometry("500x500")
    root.resizable(False, False)
    menu(root)


tkinter.mainloop()
