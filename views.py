from flask import Flask
from flask import g
from flask import render_template
from flask import abort
from flask import request
from flask import url_for
from flask import redirect
from flask import session

#import chatbot_brain

app = Flask(__name__)

@app.route('/')
def show_chatbot(reply="1test"):
    """Displays base.html when user goes to main page."""
    return render_template('base.html', reply=reply)


@app.route('/submit', methods=['GET','POST'])
def submit():
    """Accepts user submission, creates reply, redirects to homepage."""
    submission = request.form['submission']
    reply = "test" #cbot.<"analyze the input">(submission)
    return show_chatbot(reply)


if __name__ == '__main__':
    #cbot = chatbot_brain.Chatbot()
    #app.run(debug=True)
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8000, app)
    srv.serve_forever()
