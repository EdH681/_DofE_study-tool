Program 2 for DofE skill

New modules used:
- Tkinter
- JSON files
- (subprocess)

What I improved:
- Improving maintenance: using variables instead of repeated hard-coding
- commenting more often

The aim of this project was to make a study tool which functions similar to Quizlet flashcards


It is composed of:

THE STORAGE:
- Questions and answers are stored in JSON files
- Every SUBJECT stored has a corresponding JSON file
- Within the JSON files are objects which represent a topic
- these have the question as the header and the answer as the stored value


THE QUIZ:
- JSON files are stored with the questions and answers within them
- These items are retrieved and added to a list
- The quiz functions shuffle the question list and iterate through until no questions are remaining

THE ADDER:
- An interface to allow users to add their own question sets
- The user types their questions and answers separated by a separator which they can select in a text file
- They then enter the location to the text file and the name of the subject they want to add the questions to
- The program takes the questions and answers from the text file and adds them to the corresponding JSON file under a new object

THE VIEWER:
- An interface which allows the user to view all existing study sets they have created
- The user selects the subject and the topic from the dropdown menus
- The questions and answers withing that topic are then displayed in the tkinter text widget below

THE DELETER:
- An interface which allows users to remove study sets
- The user selects the subject and topic to remove
- Another option is available to delete the entire subject
- Both options have a final confirmation window to reduce the chance of accidentally removing a subject/topic
- There is also an option to open the file location of all the json files incase the user wants to only edit a set not remove
