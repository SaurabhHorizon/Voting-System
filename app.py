from flask import Flask, render_template, Response, jsonify, request

from FER_Camera import VideoCamera, Party, parties

app = Flask(__name__)

camera = None





@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("index2.html")


@app.route("/vote", methods=["GET", "POST"])
def vote():
    party = request.args.get('party') 
    global camera
    print("party:",party)
    camera.vote(party)

    return jsonify({"status":"OK"})


@app.route("/get_status", methods = ['GET','POST'])
def get_status():
    try:
        status = camera.get_status()
        return jsonify(status)
    except:
        return jsonify({"status":""})


def generate(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') 
        

@app.route("/video_feed")
def video_feed():
    global camera
    camera = VideoCamera()
    return Response(generate(camera),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/video")
def video():
    return render_template("video2.html", parties=parties)

if __name__=='__main__':
    app.run(debug=True) #,  host="0.0.0.0", port=80)