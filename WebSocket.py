import time
import socket
from flask import Flask, render_template, request


direction = 'Clockwise'
pwm = 50
HEADER = 64
PORT = 21567
FORMAT = 'utf-8'
SERVER = "192.168.1.4"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        submit = request.form['submit']       
        if submit == 'Accelerate':
            print("Acceleratation")
            send("ACC")
            global pwm
            if pwm < 100:
                pwm = pwm + 5
        elif submit == 'Deaccelerate':
            print("Deacceleration")
            send("DEACC")
            if pwm > 0:
                pwm = pwm - 5
        elif submit == 'CW':
            print("Clockwise")
            send("CW")
            global direction
            direction = 'Clockwise'
        else:
            print("Counter clockwise")
            send("CCW")
            direction = 'Counter clockwise'
            
    templateData = {
        'PWM' : str(pwm),
        'Direction' : direction
        }
        
    return render_template('webserver.html', **templateData)

if __name__=="__main__":
    app.run()
