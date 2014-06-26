from flask import Flask
from flask import g
from flask import render_template
from flask import abort
from flask import request
from flask import url_for
from flask import redirect
from flask import session

import chatbot_brain
from input_filters import input_funcs
from output_filters import funct_dict

app = Flask(__name__)


@app.route('/')
def show_chatbot(reply="Say something to me!",
                 sausage="I haven't said anything yet..."):

    """Displays base.html when user goes to main page."""
    # input_filters = []
    # for key in input_funcs:
    #     input_filters.append(key)
    # print input_filters
    return render_template('base.html', reply=reply, sausage=sausage,
                           input_filters=input_funcs,
                           output_filters=funct_dict)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """Accepts user submission, creates reply, redirects to homepage."""
    submission = request.form['submission']
    input_ = request.form['input_filter']
    print input_
    output_ = []
    output_.append(request.form['output_filter'])
    output_.append(request.form['output_filter2'])
    output_.append(request.form['output_filter3'])
    reply = cbot.compose_response(
        submission,
        input_key=input_,
        output_filter=output_
        )
    sausage = """
    Input filter(s): {} \n Output filter(s): {}
    """.format(input_, output_)
    return show_chatbot(reply, sausage)


if __name__ == '__main__':
    cbot = chatbot_brain.Chatbot()
    cbot.fill_lexicon()
    # app.run(debug=True)
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8000, app)
    srv.serve_forever()
