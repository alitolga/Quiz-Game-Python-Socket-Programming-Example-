from socket import *
import json
import threading

HOST = '127.0.0.1'
PORT = 12000

# Initialize connection (create socket, bind port and listen) 
serverSocket = socket(AF_INET, SOCK_STREAM) # TCP Socket
serverSocket.bind(('', PORT))
serverSocket.listen(45)
print('listening on', (HOST, PORT))

# Open connections
with open('questions.json') as f:
    questions = json.load(f)['questions']

valid_answers = ['a', 'b', 'c', 'd']


def startContest(s, addr):

    # Receive username
    username = s.recv(1024).decode()
    print(username, " connected")
    points = 0

    # Send # of questions
    s.send(str(len(questions)).encode())

    for question in questions:
        # print(question)

        question['msg'] = "Current Points: " + str(points)

        # Send questions
        msg = json.dumps(question).encode()
        s.send(msg)

        # Receive answer
        answer = s.recv(1024).decode()
        print(answer)
        # Send answer result
        if answer in valid_answers and answer is valid_answers[question['correct_answer']]:
            points += 10
            msg = "The answer is correct!"
            s.send(msg.encode())
        else:
            msg = "Wrong answer! The correct answer was " + valid_answers[question['correct_answer']]
            s.send(msg.encode())
        print("Total points: " + str(points))
    
    s.close()


while True:
    s, addr = serverSocket.accept()
    threading.Thread(target = startContest, args = (s, addr)).start()
