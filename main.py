import json
import tkinter


def load(subject, topic):
    with open(f"{subject}.json", "r") as retrieve:
        data = json.load(retrieve)[topic]
    questions = []
    for i in data:
        pair = (i, data[i])
        questions.append(pair)
    return questions


questions = load("computing", "databases")


