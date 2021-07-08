from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

user = 'bleyceua'
password = 'LcvCfITW4teZg9Eq7kE2dfJxMizJk6WF'
host = 'tuffi.db.elephantsql.com'
database = 'bleyceua'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "asdfga"

db = SQLAlchemy(app)


class Generos(db.Model):
    __tablename__ = "generos"

    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(255), nullable=False)

    def __init__(self, genero):
        self.genero = genero

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, novo_genero):  # adicionar sinopse
        self.genero = novo_genero
        self.save()

    @staticmethod
    def generos_nome(genero_nome):
        return Generos.query.filter(Generos.genero == genero_nome).first()


class Animes(db.Model):
    __tablename__ = "animes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)
    trailer = db.Column(db.String(255), nullable=True)
    sinopse = db.Column(db.String(1750), nullable=True)
    idgeneros = db.Column(db.Integer, db.ForeignKey(
        'generos.id'), nullable=False)
    generos = db.relationship('Generos', foreign_keys='Animes.idgeneros')

    def __init__(self, nome, imagem_url, trailer, sinopse, idgeneros):
        self.nome = nome
        self.imagem_url = imagem_url
        self.trailer = trailer
        self.sinopse = sinopse
        self.idgeneros = idgeneros

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, novo_nome, nova_imagem_url, novo_idgenero, novo_trailer, nova_sinopse):  # adicionar sinopse
        self.nome = novo_nome
        self.imagem_url = nova_imagem_url
        self.idgenero = novo_idgenero
        self.trailer = novo_trailer
        self.sinopse = nova_sinopse  # adicionar sinopse

        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def read_all():
        db.session.close_all()
        return Animes.query.order_by(Animes.nome.asc()).all()

    @staticmethod
    def read_single(id_registro):
        animes_generos = Animes.query.join(Generos).filter(
            Animes.id == id_registro).first()
        db.session.close_all()
        return animes_generos.query.get(id_registro)

    @staticmethod
    def conta():
        db.session.close_all()
        return Animes.query.count()


@app.route("/")
def index():
    total = Animes.query.count()
    db.session.close_all()
    return render_template("index.html", total=total)


@app.route("/read")
def read_all():
    registros = Animes.read_all()
    db.session.close_all()
    return render_template("read.html", registros=registros)

@app.route("/read/<id_registro>")
def read_id(id_registro):
    anime_genero = Generos.query.join(Animes, Generos.id == Animes.idgeneros).add_columns(Animes.id, Animes.nome, Animes.imagem_url,
                                                                                          Animes.trailer, Animes.sinopse, Animes.idgeneros, Generos.id, Generos.genero).filter(Animes.id == id_registro).first()
    anime_velho = Animes.read_single(id_registro)
    db.session.close_all()
    return render_template("read_single.html", anime_genero=anime_genero, anime_velho=anime_velho)


@app.route("/create", methods=('GET', 'POST'))
def create():
    novo_id = None

    anime_genero = Generos.query.join(Animes, Generos.id == Animes.idgeneros).add_columns(Animes.id, Animes.nome, Animes.imagem_url,Animes.trailer, Animes.sinopse, Animes.idgeneros, Generos.genero)

    if request.method == 'POST':
        form = request.form

        registro_genero = Generos.generos_nome(form['genero'])

        registro = Animes(form['nome'], form['imagem_url'],
                          form['trailer'], form['sinopse'], registro_genero.id)
        registro.save()

        novo_id = registro.id

    db.session.close_all()
    return render_template("create.html", anime_genero=anime_genero, novo_id=novo_id)


@app.route('/update/<id_registro>', methods=('GET', 'POST'))
def update(id_registro):
    sucesso = False

    anime_genero = Generos.query.join(Animes, Generos.id == Animes.idgeneros).add_columns(Animes.id, Animes.nome, Animes.imagem_url,Animes.trailer, Animes.sinopse, Animes.idgeneros, Generos.genero).filter(Animes.id == id_registro).first()

    anime_velho = Animes.read_single(id_registro)

    if request.method == 'POST':
        form = request.form

        registro_genero = Generos.generos_nome(form['genero'])

        anime_velho.update(form['nome'], form['imagem_url'], registro_genero.id,
                            form['trailer'], form['sinopse'])

        sucesso = True

    db.session.close_all()
    return render_template('update.html', anime_genero=anime_genero, anime_velho=anime_velho, sucesso=sucesso)


@app.route('/delete/<id_registro>')
def delete(id_registro):
    registro = Animes.read_single(id_registro)
    return render_template("delete.html", registro=registro)


@app.route('/delete/<id_registro>/confirmed')
def delete_confirmed(id_registro):
    sucesso = False

    registro = Animes.read_single(id_registro)

    if registro:
        registro.delete()
        sucesso = True
        
    db.session.close_all()
    return render_template("delete.html", registro=registro, sucesso=sucesso)


if (__name__ == "__main__"):
    app.run(debug=True)

