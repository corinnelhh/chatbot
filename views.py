from flask import Flask
from flask import g
from flask import render_template
from flask import abort
from flask import request
from flask import url_for
from flask import redirect
from flask import session

import chatbot_brain

app = Flask(__name__)


@app.route('/')
def show_chatbot(reply="Say something to me!", sausage="I haven't said anything yet..."):
    """Displays base.html when user goes to main page."""
    return render_template('base.html', reply=reply, sausage=sausage)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """Accepts user submission, creates reply, redirects to homepage."""
    submission = request.form['submission']
    input_ = request.form['input_filter']
    output_ = request.form['output_filter']
    reply = cbot.compose_response(
        submission,
        input_filter=input_,
        output_filter=output_
        )
    sausage = """
    Input filter(s): {} \n Output filter(s): {} \n
    """.format(input_, output_)
    return show_chatbot(reply, sausage)


if __name__ == '__main__':
    cbot = chatbot_brain.Chatbot()
    cbot.fill_lexicon()
    # app.run(debug=True)
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8000, app)
    srv.serve_forever()
