from flask import Flask, url_for, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, login_required



app = Flask(__name__)
app.config['SECRET_KEY']="uzumymw"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

#CLASS USERS

class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name


#class pessoa
class Pessoa(db.Model):
    __tablename__ = 'pessoas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(84), nullable=False, unique=True, index=True)
    idade = db.Column(db.String(255), nullable=False)
    nome_da_mae = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name

@app.route("/register", methods=['GET','POST'])
def register():
    if request.form=='POST':
        user = User()
        user.name = request.form["username"]
        user.password = request.form["password"]
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/cadastro", methods=['GET','POST'])
def cadastro():
    if request.form=='POST':
        user = Pessoa()
        user.name = request.form["username"]
        user.idade = request.form["idade"]
        user.mae = request.form["nome_mae"]
        user.in_cpf = request.form["cpf"]

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("cadastro.html")
    
@app.route("/login", methods=['GET','POST'])
def login():
    """
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
    """
    return render_template("login.html")

@app.route("/pessoas")
def pessoas_cadastradas():
    pessoas = Pessoa.query.all()
    return render_template("list_cadastros.html", pessoas=pessoas)

if __name__=="__main__":
    app.run(debug=True)