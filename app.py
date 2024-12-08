# app.py
from flask import Flask, request, render_template
from query import search, documents, vocab_idf_values, inverted_index,links

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_route():
    query = request.form['query']
    results = search(query, documents, vocab_idf_values, inverted_index,links)
    return render_template('results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)