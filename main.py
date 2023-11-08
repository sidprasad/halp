from flask import Flask, render_template, request, jsonify
from dialogic import DialogicPrompter
from assistant import Assistant
from utilities import get_policy_from_web_html

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():

    if request.method == 'POST':
        policy_url = request.form.get('policy_url')
        policy_html = get_policy_from_web_html(policy_url)
        return render_template('explorer.html', policy_html = policy_html, policy_url = policy_url)

    return render_template('index.html')
        

@app.route('/explorer')
def exploremode():
    policy_html = get_policy_from_web_html("https://www.gradescope.com/privacy")
    return render_template('explorer.html', policy_html = policy_html, policy_url = "https://www.gradescope.com/privacy")



@app.route('/answer', methods=['POST'])
def assistantanswer():
    ast = Assistant()

    data = request.get_json()
    policy_url = data.get('policy_url')
    question = data.get('question')

    ans = ast.gen_answer(question=question, privacy_policy = policy_url)
    return ans

@app.route('/dialogic/gen', methods=['POST'])
def questiongen():
    dq = DialogicPrompter()

    data = request.get_json()
    policy_url = data.get('policy_url')
    q = dq.gen_question(policy_url = policy_url)    
    return q


@app.route('/dialogic/check', methods=['POST'])
def answercheck():
    dq = DialogicPrompter()
    data = request.get_json()
    policy_url = data.get('policy_url')
    question = data.get('question')
    answer = data.get('answer')
    v = dq.check_answer(policy_url = policy_url, question = question, answer = answer)    
    return v

if __name__ == '__main__':
    app.run(debug=True)