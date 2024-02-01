import json
import tkinter
import random


def load(subject, topic):
    with open(f"{subject}.json", "r") as retrieve:
        data = json.load(retrieve)[topic]
    questions = []
    for i in data:
        pair = (i, data[i])
        questions.append(pair)
    return questions


def check(attempt, answer, threshold=2):
    correct = 0
    for i in attempt:
        if i in answer:
            print(i)
            correct += 1
            answer = answer.replace(i, "")
            print(answer)
    threshold = len(answer) - threshold

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

