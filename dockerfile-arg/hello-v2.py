from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Hello world! Version 1\n'

@app.route('/test/<username>')
def test(username):
    if username == "":
        return 'Testing hidden functionality ;)\n'
    else:
        return 'Greetings Master ' + username

if __name__ == '__main__':
    try:
        image_name = os.environ['PYTHON_IMAGE_NAME']
    except:
        image_name = 'unspecified'
    try:
        image_tag = os.environ['PYTHON_IMAGE_TAG']
    except:
        image_tag = 'unspecified'
    try:
        flask_ver = os.environ['FLASK_VER']
    except:
        flask_ver = 'unspecified'
    print("Base Image is " + image_name + ":" + image_tag)
    print("Flask version installed is "+flask_ver)
    app.run(host='0.0.0.0')
