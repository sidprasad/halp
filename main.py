from flask import Flask, render_template, request, jsonify
from dialogic import DialogicPrompter
from assistant import Assistant
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/answer', methods=['POST'])
def assistantanswer():
    ast = Assistant()

    data = request.get_json()
    policy_url = data.get('policy_url')
    question = data.get('question')

    ans = ast.gen_answer(question=question, privacy_policy = policy_url)
    return ans




if __name__ == '__main__':
    app.run(debug=True)