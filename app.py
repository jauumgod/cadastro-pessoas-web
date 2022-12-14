from flask import Flask, url_for, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, login_required, LoginManager, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import csv
import xlsxwriter

app = Flask(__name__)
app.config['SECRET_KEY']="uzumymw"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

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

class user(object):
    def __init__(self, id, username, active=True):
        self.username = username
        self.id = id

        #self.active = active
    def is_authenticated(self):
        return True  

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return 5

@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)

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
            flash('Credenciais Inv??lidas')
            return redirect(url_for("login"))

        if not check_password_hash(user.password, password):
            flash('Credenciais Inv??lidas')
            return redirect(url_for("login"))

        #login_user(user)   
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
        return redirect(url_for("cadastro"))
        flash("Item cadastrado com sucesso!")
    return render_template("cadastro.html")


@app.route("/inventory")
#@login_required
def Inventory():
    itens = Inventario.query.all()
    return render_template("list_cadastros.html", itens=itens)


@app.route("/inventory/delete/<int:id>")
#@login_required
def delete_inventario(id):
    itens = Inventario.query.filter_by(id=id).first()
    db.session.delete(itens)
    db.session.commit()
    return redirect("/inventory")

@app.route("/settings/delete/<int:id>")
#@login_required
def delete_users(id):
    usuario = User.query.filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    return redirect("/settings")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    usuarios = User.query.all()
    return render_template("settings.html",usuarios=usuarios)


@app.route("/logout")
#@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/alterar_senha", methods=['GET', 'POST'])
def alterar_senha(id):
    if request.method=='POST':
        senha_antiga = request.form['senha_antiga']
        nova_senha = request.form['nova_senha']

        usuario = User.query.filter_by(id=id).first()
        db.session.add(usuario)
        db.session.commit()
        redirect("/settings")

@app.route("/inventory/gerar_csv", methods=["GET", "POST"])
def relatorio():
    from_db = []
    relatorio = Inventario.query.all()
    dados = 0
    for lista in relatorio:
        from_db.append(lista)
    print(from_db)


if __name__=="__main__":
    app.run(debug=True)