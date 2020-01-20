from socket import *
import json
import datetime, threading
import time
import PySimpleGUI as sg

# Function to fetch localhost's Ipv4 address
def getIP():
    soc = socket(AF_INET, SOCK_DGRAM)
    soc.connect(("8.8.8.8", 80))
    return soc.getsockname()[0]

def timer():
   now = time.localtime(time.time())
   return now[5]

def showRemainingTime():
    while True:
        time.sleep(10)
        global answered
        global passed_time
        if answered:
            break
        else:
            passed_time += 10
            print(str(passed_time) + " seconds passed!")
        

HOST = getIP()
PORT = 12000
QUIZ = 'QUIZ COMPETITION'

layout = [
          [sg.Text('Please enter your Name')],
          [sg.Text('Name', size=(15, 1)), sg.InputText('name')],
          [sg.Submit()]
         ]

window = sg.Window(QUIZ).Layout(layout)
button, values = window.Read()

username = values[0]

# Initialize connection
s = socket(AF_INET, SOCK_STREAM) # TCP Socket
s.connect((HOST, PORT))

s.send(username.encode())

# Receive number of questions
questions = int(s.recv(1024).decode())
print("Total # of questions are: " + str(questions))

for i in range(0, questions):
    # Receive questions
    message = s.recv(1024).decode()
    question = json.loads(message)

    answers = []
    for index, answer in enumerate(question['answers']):
        answers.append( chr(ord('a') + index) + ") " + answer )

    timestamp = datetime.datetime.now()

    # Send contestant answer
    answered = False
    passed_time = 0
    t1 = threading.Thread(target = showRemainingTime)
    t1.start()

    layout = [
        [sg.Text('\nYou have 1 minute to give an answer.\n')],
        [sg.Text(question['question'])],
        [sg.Radio(answers[0], "ANSWER", default=True)],
        [sg.Radio(answers[1], "ANSWER")],
        [sg.Radio(answers[2], "ANSWER")],
        [sg.Radio(answers[3], "ANSWER")],
        [sg.Submit()]
    ]

    window = sg.Window(QUIZ).Layout(layout)
    button, values = window.Read()
    ans = 'a'
    for index, j in enumerate(values):
        if j is True:
           ans = chr(ord('a') + index)
    answered = True
    t1.join()
    if passed_time >= 60:
        print("Timeout! Your answer will not be valid for this question")
        ans = "Timeout"
        s.send(ans.encode())
    else:
        s.send(ans.encode())

    # Receive answer result
    message = s.recv(1024).decode()
    layout = [
        [sg.Text(message)],
        [sg.Submit()]
    ]
    window = sg.Window(QUIZ).Layout(layout)
    button, values = window.Read()

s.close()
