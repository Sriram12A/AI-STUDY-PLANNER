from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    subjects = []
    marks = []
    totals = []

    # Collect 4 subjects
    for i in range(1, 5):
        subject = request.form.get(f"subject{i}")
        mark = request.form.get(f"mark{i}")
        total = request.form.get(f"total{i}")

        if subject and mark and total:
            subjects.append(subject)
            marks.append(int(mark))
            totals.append(int(total))

    results = []
    timetable = []

    for subject, mark, total in zip(subjects, marks, totals):
        percentage = (mark / total) * 100

        if percentage < 50:
            level = "Very Weak"
            hours = 3
        elif percentage < 70:
            level = "Moderate"
            hours = 2
        else:
            level = "Strong"
            hours = 1

        results.append(
            f"{subject}: {round(percentage,2)}% → {level}"
        )

        timetable.append(
            f"{subject} → Study {hours} hour(s) daily"
        )

    return render_template(
        "index.html",
        results=results,
        timetable=timetable
    )


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)


