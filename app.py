from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

top_score = 0


class FormModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    question1 = db.Column(db.String(100), nullable=False)
    question2 = db.Column(db.String(100), nullable=False)
    question3 = db.Column(db.String(100), nullable=False)

    # def __str__(self):
    #     return self.username

    def __repr__(self):
        return f"<FormResponse {self.username}>"


@app.route('/', methods=['GET', 'POST'])
def home():
    global top_score

    if request.method == 'POST':
        user_answers = {}

        username = request.form.get('username')
        question1 = request.form.get('question1')
        question2 = request.form.get('question2')
        question3 = request.form.get('question3')
        question4 = request.form.get('question4')

        user_answers["question1"] = question1
        user_answers["question2"] = question2
        user_answers["question3"] = question3
        user_answers["question4"] = question4

        response_data = FormModel(username=username, question1=question1, question2=question2, question3=question3)
        db.session.add(response_data)
        db.session.commit()

        correct_answers = {
            "question1": "24",
            "question2": "Pasifik",
            "question3": "300.000",
            "question4": "Ankara",
        }

        score = sum(1 for k, v in correct_answers.items() if user_answers[k] == v) * 25

        if "user_high_score" not in session or score > session["user_high_score"]:
            session["user_high_score"] = score

        if score > top_score:
            top_score = score

        return render_template('base.html', top_score=top_score, current_top_score=session.get("current_top_score", 0))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)
