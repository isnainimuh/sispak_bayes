from wtforms import Form, StringField, validators, SubmitField

class NewPenyakitForm(Form):
    nama_penyakit = StringField('Nama Penyakit', [validators.DataRequired()])
    submit = SubmitField("Submit")

class NewGejalaForm(Form):
    gejala = StringField('Gejala',[validators.DataRequired()])
    #submit = SubmitField("Submit")