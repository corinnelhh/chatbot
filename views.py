from flask import Flask
from flask import g
from flask import render_template
from flask import abort
from flask import request
from flask import url_for
from flask import redirect
from flask import session


@app.route('/')
def show_chatbot():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
