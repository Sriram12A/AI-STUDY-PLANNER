from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.secret_key = "secret123"

# -----------------------------
# DATABASE CONFIG
# -----------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    prev_marks = db.Column(db.Float)
    target_marks = db.Column(db.Float)
    days_left = db.Column(db.Integer)
    theory_pct = db.Column(db.Float)
    practical_pct = db.Column(db.Float)
    total_study_hours = db.Column(db.Float)
    daily_theory = db.Column(db.Float)
    daily_practical = db.Column(db.Float)

with app.app_context():
    db.create_all()

# -----------------------------
# ML MODEL: Predicts Total Study Hours
# Features: [Improvement, Days Left]
# -----------------------------
# Synthetic training data
train_data = {
    "improvement": [5, 10, 15, 20, 25, 30, 5, 20, 40, 10],
    "days_left":   [30, 25, 20, 15, 10, 5, 60, 45, 10, 50],
    "total_hours": [15, 25, 40, 55, 75, 100, 10, 35, 120, 20]
}
df_train = pd.DataFrame(train_data)
X = df_train[["improvement", "days_left"]]
y = df_train["total_hours"]

model = LinearRegression().fit(X, y)

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        num_subjects = int(request.form.get("num_subjects", 0))
        results = []

        for i in range(num_subjects):
            subj_name = request.form.get(f"subject_{i}", "Subject")
            prev = float(request.form.get(f"prev_marks_{i}", 0))
            target = float(request.form.get(f"target_marks_{i}", 0))
            days = int(request.form.get(f"days_left_{i}", 1))
            theory_p = float(request.form.get(f"theory_pct_{i}", 50))
            pract_p = float(request.form.get(f"pract_pct_{i}", 50))

            # Step 1: Improvement Required
            improvement = max(target - prev, 0.1)

            # Step 2: Predict Total Study Hours (ML)
            prediction_input = np.array([[improvement, days]])
            total_hours = float(model.predict(prediction_input)[0])
            total_hours = max(total_hours, 1.0) # Ensure at least 1 hr

            # Step 3: Validate/Normalize Percentages
            total_pct = theory_p + pract_p
            if total_pct != 100:
                theory_p = (theory_p / total_pct) * 100
                pract_p = (pract_p / total_pct) * 100

            # Step 4: Intelligent Rules
            if pract_p > 60 or "Lab" in subj_name:
                pract_p += 10 # Boost practical priority
                theory_p -= 10
            
            if theory_p > 60 or "Theory" in subj_name:
                theory_p += 5 # Buffer for revision

            # Normalize again after rules
            final_total = theory_p + pract_p
            theory_p = (theory_p / final_total) * 100
            pract_p = (pract_p / final_total) * 100

            # Step 5: Allocate Study Time
            theory_time = (theory_p / 100) * total_hours
            practical_time = (pract_p / 100) * total_hours

            # Step 6: Distribute Across Days
            daily_theory = theory_time / days
            daily_practical = practical_time / days

            # Save to Database
            entry = StudyPlan(
                subject=subj_name, prev_marks=prev, target_marks=target,
                days_left=days, theory_pct=theory_p, practical_pct=pract_p,
                total_study_hours=round(total_hours, 2),
                daily_theory=round(daily_theory, 2),
                daily_practical=round(daily_practical, 2)
            )
            db.session.add(entry)

            results.append({
                "subject": subj_name,
                "prev": prev,
                "target": target,
                "days": days,
                "total_h": round(total_hours, 2),
                "theory_h": round(theory_time, 2),
                "pract_h": round(practical_time, 2),
                "daily_t": daily_theory,
                "daily_p": daily_practical
            })

        db.session.commit()
        
        total_daily_all = sum((r["daily_t"] + r["daily_p"]) for r in results)

        session["results"] = results
        session["total_daily_all"] = round(total_daily_all, 2)
        return redirect(url_for("results_page"))

    return render_template("index.html")

@app.route("/results")
def results_page():
    results = session.pop("results", None)
    total_daily_all = session.pop("total_daily_all", 0)
    if not results:
        return redirect(url_for("home"))
    return render_template("results.html", results=results, total_daily_all=total_daily_all)

if __name__ == "__main__":
    app.run(debug=True, port=5001)