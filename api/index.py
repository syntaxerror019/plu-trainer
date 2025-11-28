from flask import Flask, render_template, redirect, request
import csv
import random    

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/practice')
def practice():
    return redirect('/')

@app.route('/practice/plu/code', methods=['GET', 'POST'])
def practice_plu_code():
    iscorrect = None
    previous_options = None
    previous_correct_code = None
    previous_name = None
    
    if request.method == 'POST':
        correct_plu = request.form.get('correct_plu')
        plu_code = request.form.get('plu_code')
        iscorrect = True if plu_code == correct_plu else False
        previous_options = request.form.get('options').split(',')
        previous_correct_code = correct_plu
        previous_name = request.form.get('name')
        
    name, correct_plu, options = generate_quiz_options()
    
    return render_template('quiz.html', iscorrect=iscorrect, correct=correct_plu, options=options, name=name, previous_options=previous_options, previous_correct_code=previous_correct_code, previous_name=previous_name)

@app.route('/practice/plu/image')
def practice_plu_image():
    return render_template('quiz_image.html')

@app.route('/practice/match')
def practice_match():
    return render_template('match.html')

@app.route('/docs')
def docs():
    items = load_commodities()
    return render_template('render.html', items=items)

def load_commodities():
    commodities = []
    with open('./commodities.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            commodities.append(row)
    return commodities

def generate_quiz_options():
    items = load_commodities()
    items = [i for i in items if "Retailer" not in i['Variety']]
    
    correct_item = random.choice(items)
    name = f"{correct_item['Commodity'].title()} {correct_item['Variety'].title()}".strip()
    correct_plu = correct_item['Plu']
    wrong_items = random.sample([i for i in items if i['Plu'] != correct_plu], 3)

    options = [correct_plu] + [i['Plu'] for i in wrong_items]
    random.shuffle(options)

    return name, correct_plu, options


if __name__ == '__main__':
    app.run(debug=True)