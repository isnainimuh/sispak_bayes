from flask import Flask, request, flash, render_template, url_for
from form2 import NewGejalaForm, NewPenyakitForm
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
#koneksi ke database
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:''@localhost/bayes'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY']=SECRET_KEY

db = SQLAlchemy(app)

app.app_context().push()

class Penyakit(db.Model):
    kd_penyakit = db.Column(db.Integer, primary_key=True)
    nama_penyakit = db.Column(db.String(80), unique=True)

    def __init__(self, nama_penyakit):
        self.nama_penyakit=nama_penyakit

    def __repr__(self):
        return f"{self.kd_penyakit} {self.nama_penyakit}"

class Gejala(db.Model):
    kd_gejala = db.Column(db.Integer, primary_key=True)
    gejala = db.Column(db.String(80), unique=True)

    def __init__(self, gejala):
        self.gejala=gejala
    
    def __repr__(self):
        return f"{self.kd_gejala} {self.gejala}"

class Aturan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kd_penyakit = db.Column(db.Integer, db.ForeignKey(Penyakit.kd_penyakit))
    kd_gejala = db.Column(db.Integer, db.ForeignKey(Gejala.kd_gejala))
    probabilitas = db.Column(db.Float)

    def __repr__(self):
        return f"{self.kd_gejala} {self.kd_penyakit} {self.probabilitas}"


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/penyakit")
def penyakit():
    data = Penyakit.query.all()
    return render_template('penyakit.html', data=data)

@app.route("/insertPenyakit")
def insertPenyakit():
    form = NewPenyakitForm()
    return render_template('formPenyakit.html', form=form)

@app.route("/gejala")
def gejala():
    return render_template('gejala.html')

@app.route("/insertGejala", methods=['POST'])
def insertGejala():
    form = NewGejalaForm()
    return render_template('formGejala.html', form=form)

@app.route("/prediksi")
def prediksi():
    return render_template('prediksi.html')


@app.route("/submitPen", methods=['POST','GET'])
def submitPen():
    form = NewPenyakitForm(request.form)
    if form.validate():
        pen = Penyakit(request.form['nama_penyakit'])
        db.session.add(pen)
        try:
            db.session.commit()
            flash(f"Penyakit {pen.nama_penyakit} berhasil ditambahkan")
            return render_template ('formPenyakit.html', penyakit=pen.nama_penyakit)  
        except Exception as e:
            db.session.rollback()
            flash(f"Penyakit {pen.nama_penyakit} gagal ditambahkan. Error {e}")
            return render_template  ('formPenyakit.html', penyakit=pen.nama_penyakit)
    else:
        return "Invalidate form"

@app.route("/updatePenyakit/<int:id>", methods=['POST','GET'])
def updatePenyakit(id):
    form = NewPenyakitForm()
    data_update = Penyakit.query.get_or_404(id)
    #data_update = Penyakit.query.filter_by(kd_penyakit=id)
    if request.method == 'POST':
        data_update.nama_penyakit = request.form['nama_penyakit']
        try:
            db.session.commit()
            flash(f"Update penyakit berhasil!")
            return render_template('editPenyakit.html', form=form, data_update=data_update)
        except Exception as e:
            db.session.rollback()
            flash(f"Update gagal! Error {e}")
            return render_template ('editPenyakit.html', form=form, data_update=data_update)
    else:
        return render_template ('editPenyakit.html', form=form, data_update=data_update)




@app.route("/submitGejala", methods=['POST','GET'])
def submitGejala():
    form = NewGejalaForm(request.form)
    if form.validate():
        gej = Gejala(request.form['gejala'])
        db.session.add(gej)
        try:
            db.session.commit()
            flash(f"Gejala {gej.kd_gejala} berhasil ditambahkan")
            return render_template ('gejala.html', gejala=gej.kd_gejala)  
        except Exception as e:
            db.session.rollback()
            flash(f"Gejala {gej.kd_gejala} gagal ditambahkan. Error {e}")
            return render_template  ('gejala.html', gejala=gej.kd_gejala)
    else:
        return "Invalidate form"


if __name__ == '__main__':
    app.run(debug=True)