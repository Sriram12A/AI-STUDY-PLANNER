# AI Study Planner

An intelligent Study Planner application built with Flask and scikit-learn. The app uses linear regression and priority-weighted logic to help students optimize their study hours based on target marks, previous performance, and available time.

## Features
- **Smart Time Allocation**: Uses Machine Learning to predict required total study hours.
- **Priority Logic**: Adjusts time automatically based on theory vs. practical subjects.
- **Detailed Distribution**: Generates a day-to-day study timetable.
- **Presentation Generator**: Includes a script to automatically generate PowerPoint slides of model performance and planning metrics.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd "ai pro"
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   ```

3. **Activate the environment:**
   - **Windows:** `.\.venv\Scripts\activate`
   - **Mac/Linux:** `source .venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask application:**
   ```bash
   python app.py
   ```
   *Note: If port 5000 is occupied, you might need to run it on a different port.*

6. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:5001/` (or the port displayed in your terminal).

7. **Generate Presentation:**
   ```bash
   python create_presentation.py
   ```
   This will generate a `Study_Plan_Analysis.pptx` file with analytics.
