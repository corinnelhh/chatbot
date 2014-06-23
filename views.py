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


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]


if __name__ == '__main__':
    #cbot = chatbot_brain.Chatbot()
    #app.run(debug=True)
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8000, app)
    srv.serve_forever()
