from flask import Flask, render_template, request, Response, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senha@localhost/atividade_teste'

db = SQLAlchemy(app)

#cria tabela
class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nome = db.Column(db.String(45), unique = True)
    email = db.Column(db.String(45), unique = True)
    senha = db.Column(db.String(45))
    adm = db.Column(db.Boolean, default= False)

    def __init__(self, nome, email, senha, adm):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.adm = adm

@app.route("/adm", methods=["GET"])
def selecionar_todos_usuarios():

    usuarios_objetos = Usuario.query.all() 
    return render_template("lista_usuarios.html", usuario_final = usuarios_objetos)

@app.route("/adm/<id>", methods = ["GET"])
def selecionar_um_usuario(id):

    usuario_objeto = Usuario.query.get(id)
    return render_template("lista_usuarios.html", usuario = usuario_objeto)

@app.route("/adm/cadastrar", methods = ["GET" , "POST"])
def criar_usuario():

    if(request.method == 'POST'):
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']
        adm = 'adm_cadastrar' in request.form
        nome = nome.strip()
        email = email.strip()
        senha = senha.strip()

        if(senha == confirmar_senha):
            try:
                usuario_email = Usuario.query.filter_by(nome=nome).first()
                if usuario_email:
                    return redirect("/adm")
                usuario_nome = Usuario.query.filter_by(email=email).first()
                if usuario_nome:
                    return redirect("/adm")
                if(not nome):
                    print("cadastrar nome")
                    return redirect("/adm")
                if(not email):
                    print("cadastrar email")
                    return redirect("/adm")
                if(not senha):
                    print("cadastrar senha")
                    return redirect("/adm")
                
                usuario = Usuario(nome, email, senha, adm)
                db.session.add(usuario)
                db.session.commit()
                return redirect("/adm")
            except Exception as e:
                print("Erro" , e)
                return redirect("/adm")
        return redirect("/adm")
    
#Atualiza usuario
@app.route("/adm/<id>/atualizar", methods =["POST"])
def atualiza_usuario(id):
    usuario_objeto = Usuario.query.get(id)
    print(usuario_objeto.nome)

    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    nome = nome.strip()
    email = email.strip()
    senha = senha.strip()

    if(not nome):
        return redirect("/adm")
    if(not email):
        return redirect("/adm")
    if(not senha):
        return redirect("/adm")

    usuario_objeto.nome = nome
    usuario_objeto.email = email
    usuario_objeto.senha = senha
    
    
    if 'adm_alterar' in request.form:
        usuario_objeto.adm = True
    else:
        usuario_objeto.adm = False

    db.session.commit()
    return redirect('/adm')

@app.route("/adm/<id>/atualiza")
def atualizar_usuario(id):

    usuario_objeto = Usuario.query.get(id)
    return render_template("lista_usuarios.html", usuario_atualiza = usuario_objeto, atualizar = True)

@app.route("/adm/<id>/deletar")

def deleta_usuario(id):

    usuario_objeto = Usuario.query.get(id)
    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return redirect("/adm")
    except Exception as e:
        print("Erro", e)
        return redirect("/adm")
    
    

if __name__ == "__main__":
    app.run(debug=True)