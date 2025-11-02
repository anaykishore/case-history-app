from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('case_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_number TEXT,
            case_type TEXT,
            year TEXT,
            first_party TEXT,
            second_party TEXT,
            court_complex TEXT,
            filing_date TEXT,
            cnr_number TEXT,
            first_hearing TEXT,
            next_hearing TEXT,
            court_judge TEXT,
            case_stage TEXT,
            fir_number TEXT,
            remarks TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_case():
    case_id = request.args.get('case_id')
    case = None

    if request.method == 'GET' and case_id:
        # Fetch existing case data to pre-fill the form
        conn = sqlite3.connect('case_data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM cases WHERE id = ?', (case_id,))
        case = c.fetchone()
        conn.close()
        return render_template('add_case.html', case=case)

    if request.method == 'POST':
        case_id = request.form.get('case_id')
        data = (
            request.form['case_number'],
            request.form['case_type'],
            request.form['year'],
            request.form['first_party'],
            request.form['second_party'],
            request.form['court_complex'],
            request.form['filing_date'],
            request.form['cnr_number'],
            request.form['first_hearing'],
            request.form['next_hearing'],
            request.form['court_judge'],
            request.form['case_stage'],
            request.form['fir_number'],
            request.form['remarks']
        )

        conn = sqlite3.connect('case_data.db')
        c = conn.cursor()

        if case_id:
            # Update existing case
            c.execute('''
                UPDATE cases SET
                    case_number = ?, case_type = ?, year = ?, first_party = ?, second_party = ?,
                    court_complex = ?, filing_date = ?, cnr_number = ?, first_hearing = ?,
                    next_hearing = ?, court_judge = ?, case_stage = ?, fir_number = ?, remarks = ?
                WHERE id = ?
            ''', data + (case_id,))
        else:
            # Insert new case
            c.execute('''
                INSERT INTO cases (
                    case_number, case_type, year, first_party, second_party,
                    court_complex, filing_date, cnr_number, first_hearing,
                    next_hearing, court_judge, case_stage, fir_number, remarks
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)

        conn.commit()
        conn.close()
        return redirect('/add')

    return render_template('add_case.html', case=None)

@app.route('/search', methods=['GET', 'POST'])
def search_case():
    result = []
    searched = False  # Flag to track if a search was performed
    if request.method == 'POST':
        searched = True
        filters = {
            'case_number': request.form.get('case_number'),
            'case_type': request.form.get('case_type'),
            'year': request.form.get('year'),
            'first_party': request.form.get('first_party'),
            'second_party': request.form.get('second_party'),
            'court_complex': request.form.get('court_complex'),
            'cnr_number': request.form.get('cnr_number'),
            'next_hearing': request.form.get('next_hearing'),
            'fir_number': request.form.get('fir_number')
        }

        conn = sqlite3.connect('case_data.db')
        c = conn.cursor()

        for field, value in filters.items():
            if value:
                query = f"SELECT * FROM cases WHERE {field} = ?"
                c.execute(query, (value,))
                result = c.fetchall()
                break  # Only search by the first filled field

        conn.close()

    return render_template('search_case.html', results=result, searched=searched)

@app.route('/hearing_list', methods=['GET', 'POST'])
def hearing_list():
    cases = []
    selected_date = None

    if request.method == 'POST':
        selected_date = request.form.get('hearing_date')
        conn = sqlite3.connect('case_data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM cases WHERE next_hearing = ?', (selected_date,))
        cases = c.fetchall()
        conn.close()

    return render_template('hearing_list.html', cases=cases, hearing_date=selected_date)

@app.route('/update', methods=['GET', 'POST'])
def update_search():
    result = []
    searched = False
    if request.method == 'POST':
        searched = True
        filters = {
            'case_number': request.form.get('case_number'),
            'case_type': request.form.get('case_type'),
            'year': request.form.get('year'),
            'first_party': request.form.get('first_party'),
            'second_party': request.form.get('second_party'),
            'court_complex': request.form.get('court_complex'),
            'cnr_number': request.form.get('cnr_number'),
            'next_hearing': request.form.get('next_hearing'),
            'fir_number': request.form.get('fir_number')
        }

        conn = sqlite3.connect('case_data.db')
        c = conn.cursor()

        for field, value in filters.items():
            if value:
                query = f"SELECT * FROM cases WHERE {field} = ?"
                c.execute(query, (value,))
                result = c.fetchall()
                break  # Only search by the first filled field

        conn.close()

    return render_template('update_case_search.html', results=result, searched=searched)

if __name__ == '__main__':
    app.run(debug=True)