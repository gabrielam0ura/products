from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:senha@localhost:5432/teste'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    value = db.Column(db.Float, nullable=False)
    disponible = db.Column(db.String(3), nullable=False)

@app.route('/')
def index():
    produtos = Produto.query.order_by(Produto.value.asc()).all()
    return render_template('index.html', produtos=produtos)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        value = request.form['value']
        disponible = request.form['disponible']

        novo_produto = Produto(name=name, description=description, value=value, disponible=disponible)
        
        db.session.add(novo_produto)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
