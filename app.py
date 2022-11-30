from flask import Flask, url_for, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, login_required
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['SECRET_KEY']="uzumymw"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

#CLASS USERS

class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name


#CLASS PESSOA
class Inventario(db.Model):
    __tablename__ = 'inventario'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(84), nullable=False)
    modelo = db.Column(db.String(255), nullable=False)
    ano = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.String(255), nullable=False)
    data = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method=='POST':
        user = User()
        user.nome_completo = request.form['nome_completo']
        user.login = request.form["usuario"]
        user.password = generate_password_hash(request.form["password"])
        db.session.add(user)
        db.session.commit()            
        flash('Usuario criado com sucesso!')
        return redirect("/login")

    return render_template("register.html")
    
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['usuario']
        password = request.form['senha']
        user = User.query.filter_by(login=username).first()
        if not user:
            return redirect(url_for("login"))
        if not check_password_hash(user.password, password):
            return redirect(url_for("login"))

        return redirect(url_for("Inventory"))
    return render_template("login.html")

@app.route("/cadastro", methods=["GET","POST"])
def cadastro():
    if request.method=="POST":
        itens = Inventario()
        itens.item = request.form["item"]
        itens.modelo = request.form["modelo"]
        itens.ano = request.form['ano']
        itens.quantidade = request.form["quant"]
        itens.valor = request.form["valor"]
        itens.data = request.form["data"]
        db.session.add(itens)
        db.session.commit()
        if db.session.commit==True:
            flash("Item cadastrado com sucesso!")
            return redirect(url_for("cadastro"))
    return render_template("cadastro.html")

@login_required
@app.route("/inventory")
def Inventory():
    itens = Inventario.query.all()
    return render_template("list_cadastros.html", itens=itens)

@app.route("/inventory/<int:id>")
def delete(id):
    itens = Inventario.query.filter_by(id=id).first()
    db.session.delete(itens)
    db.session.commit()
    return redirect("/inventory")

@login_required
@app.route("/settings", methods=["GET", "POST"])
def settings():
    usuarios = User.query.all()
    return render_template("settings.html",usuarios=usuarios)


if __name__=="__main__":
    app.run(debug=True)