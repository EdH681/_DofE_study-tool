import json
import tkinter
import tkinter.ttk as ttk
import os
import random
from math import *


def load(subject, topic):
    with open(f"{subject}.json", "r") as retrieve:
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


def add(subject, title, filename):
    with open(f"{subject}.json", "r") as retrieve:
        temp = json.load(retrieve)

    new = {}
    with open(f"{filename}", "r") as take:
        for line in take:
            line = line.strip()
            line = line.split(",")
            new[line[0]] = line[1]

    temp[title] = new

    with open(f"{subject}.json", "w") as update:
        json.dump(temp, update)


def clear(container):
    for item in container.winfo_children():
        item.destroy()


def menu(frame):
    clear(frame)
    baseY = 200
    titleText = "Select an Option"
    title = tkinter.Label(frame, text=titleText, font=("Helvetica", 20, "bold"))
    title.place(relx=0, y=20, width=500, height=50)

    # Test Button
    startText = "Test Yourself"
    testYourself = tkinter.Button(frame, text=startText, font=("Helvetica", 20), command=lambda: selection(root))
    testYourself.place(x=50, y=baseY, width=400, height=50)

    # Add Button
    addText = "Add More Question Sets"
    addButton = tkinter.Button(frame, text=addText, font=("Helvetica", 20))
    addButton.place(x=50, y=baseY + 55, width=400, height=50)

    # View Button
    viewText = "View All Question Sets"
    viewButton = tkinter.Button(frame, text=viewText, font=("Helvetica", 20))
    viewButton.place(x=50, y=baseY + 110, width=400, height=50)

    # Remove Button
    removeText = "Remove a Question Set"
    removeButton = tkinter.Button(frame, text=removeText, font=("Helvetica", 20))
    removeButton.place(x=50, y=baseY + 165, width=400, height=50)


def selection(frame):
    clear(frame)

    # Getting Subjects
    options = ["Select an option"]
    for subject in os.listdir():
        if subject.split(".")[1] == "json":
            options.append(subject.split(".")[0].title())

    # Title
    title = tkinter.Label(frame, text="Select a Subject and a Topic", font=("Helvetica", 20, "bold"))
    title.pack(pady=10)

    # Topic Box
    tkinter.Label(frame, text="Select a Topic", font=("Helvetica", 12, "bold")).place(x=105, y=215)
    topicSelect = ttk.Combobox(frame, values=["Select an Option"], state="disabled", width=42)
    topicSelect.current(0)
    topicSelect.place(x=105, y=250)

    # Subject Box
    tkinter.Label(frame, text="Select a Subject", font=("Helvetica", 12, "bold")).place(x=105, y=115)
    subjectSelect = ttk.Combobox(frame, values=options, width=20, font=("Helvetica", 10), state="readonly")
    subjectSelect.current(0)
    subjectSelect.place(x=105, y=150)

    # Subject Button
    subjectButton = tkinter.Button(frame, text="Select",
                                   command=lambda: subject_check(subjectSelect.get(), topicSelect))
    subjectButton.place(x=275, y=150, width=100, height=22)

    # Start Button
    startButton = tkinter.Button(frame, text="Start", font=("Helvetica", 20), command=lambda: \
        questionGrab(frame, subjectSelect.get(), topicSelect.get()))
    startButton.place(x=105, y=350, width=280, height=50)

    # Return to Menu
    returnButton = tkinter.Button(frame, text="Menu", command=lambda: menu(frame))
    returnButton.place(x=10, y=470, width=50, height=25)


def subject_check(value, box):
    if value != "Select an option":
        box["state"] = "readonly"
        topics = ["Select an option"]
        with open(f"{value}.json", "r") as topicList:
            data = json.load(topicList)
            for topic in data:
                topics.append(topic)
        box["values"] = topics
    else:
        box['state'] = "disabled"
        box["values"] = ["Select an Option"]
        box.current(0)


def questionGrab(frame, subject, topic):
    try:
        questions = load(subject.lower(), topic.lower())
    except KeyError:
        tkinter.Label(frame, text="Select a valid topic", fg="red").place(x=105, y=400, width=280)
    except FileNotFoundError as e:
        print(e)
        tkinter.Label(frame, text="Select a valid subject", fg="red").place(x=105, y=400, width=280)
    else:
        quiz(frame, questions)


def quiz(frame, questions, questionNumber=1, correct=0, incorrect=0):
    clear(frame)
    random.shuffle(questions)
    title = tkinter.Label(frame, text=f"Question {questionNumber}", font=("Helvetica", 20, "bold"))
    title.place(x=0, y=10, width=500, height=50)

    if questions:
        questionAnswer = questions.pop(0)

        question = tkinter.Label(frame, text=questionAnswer[0], font=("Helvetica", 18), wraplength=455)
        question.place(x=0, y=100, width=500, height=150)

        answerBox = tkinter.Entry(frame, font=("Helvetica", 18), justify="center")
        answerBox.place(x=50, y=300, height=50, width=400)

        submitButton = tkinter.Button(frame, text="Submit", font=("Helvetica", 15),
                                      command=lambda: quiz_check(frame, answerBox.get(), questionAnswer, questions,
                                                                 questionNumber, correct, incorrect))
        submitButton.place(x=150, y=360, height=40, width=200)

        returnButton = tkinter.Button(frame, text="Return", command=lambda: selection(frame))
        returnButton.place(x=10, y=470, width=50, height=25)
    else:
        quizComplete(frame, correct, incorrect)


def quiz_check(frame, entered, questionAnswer, questions, questionNumber, correct, incorrect):
    right = check(entered.lower(), questionAnswer[1])
    questionNumber += 1
    if right:
        tkinter.Label(frame, text="Correct", fg="green", font=("Helvetica", 12)).place(x=0, y=270, width=500, height=30)
        correct += 1
    else:
        tkinter.Label(frame, text=f"Incorrect, it was {questionAnswer[1]}", fg="red", font=("Helvetica", 12)).place(x=0,
                                                                                                                    y=270,
                                                                                                                    width=500,
                                                                                                                    height=30)
        incorrect += 1

    tkinter.Button(frame, text="Continue", font=("Helvetica", 10),
                   command=lambda: quiz(frame, questions, questionNumber, correct, incorrect)).place(x=200, y=405,
                                                                                                     width=100,
                                                                                                     height=30)


def quizComplete(frame, correct, incorrect):
    clear(frame)
    tkinter.Label(frame, text="Quiz Complete", font=("Helvetica", 25, "bold")).pack()
    tkinter.Label(frame, text=f"{correct} correctly answered", font=("Helvetica", 20), fg="green").place(x=0, y=200,
                                                                                                         width=500,
                                                                                                         height=50)
    tkinter.Label(frame, text=f"{incorrect} incorrectly answered", font=("Helvetica", 20), fg="red").place(x=0, y=250,
                                                                                                           width=500,
                                                                                                           height=50)
    tkinter.Button(frame, text="Return to menu", font=("Helvetica", 18), command=lambda: menu(frame)).place(x=150,
                                                                                                            y=350,
                                                                                                            width=200,
                                                                                                            height=50)


# setting up the tkinter window
root = tkinter.Tk()
root.geometry("500x500")
root.resizable(False, False)
menu(root)

root.mainloop()
