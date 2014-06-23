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
def show_chatbot():
    """Displays base.html when user goes to main page."""
    return render_template('base.html', reply=reply)


@app.route('/submit', methods=['POST'])
def submit():
    """Accepts user submission, creates reply, redirects to homepage."""
    try:
        submission = request.form['submission']
        reply = cbot.<"analyze the input">(submission)
    return redirect(url_for('show_chatbot'))


if __name__ == '__main__':
    cbot = chatbot_brain.Chatbot()
    app.run(debug=True)
