from flask import Flask, render_template, Response
from camera import Video

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/reports')
def report():
    suprise_list=[]
    angry_list=[]
    happy_list=[]
    neutal_list=[]
    fear_list=[]
    sad_list=[]
    with open("ak.txt") as f:
        emotion_dictionary = {}
        for i in f.readlines():
            k = i.split()
            temp1 = k[0]
            temp2 = k[1]
            emotion_dictionary[temp2] = temp1



    for i in emotion_dictionary.keys():
        if (emotion_dictionary[i] == 'neutral'):
             neutal_list.append(i)
        else:
             neutal_list.append(0)
            
        if (emotion_dictionary[i] == 'surprise'):
             suprise_list.append(i)
        else:
             suprise_list.append(0)
        if (emotion_dictionary[i] == 'happy'):
             happy_list.append(i)
        else:
            happy_list.append(0)
        if (emotion_dictionary[i] == 'sad'):
             angry_list.append(i)
        else:
             angry_list.append(0)

        
    print(len(suprise_list))
        
        

    return render_template('report.html',suprises=suprise_list,angrys=angry_list,happys=happy_list,neutrals=neutal_list)
def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')

def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(debug=True)