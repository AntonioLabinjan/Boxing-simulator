from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'SECRET'  # Zamijenite 'your_secret_key' sa stvarnim tajnim ključem
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:AN1246A301JA@localhost/bokseri'  # Zamijenite sa stvarnim podacima
db = SQLAlchemy(app)

# Definicija modela za baze podataka
class Boksač(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(255), nullable=False)
    prezime = db.Column(db.String(255), nullable=False)
    kategorija = db.Column(db.String(255))
    drzava = db.Column(db.String(255))
    broj_pobjeda = db.Column(db.Integer, default=0)
    broj_poraza = db.Column(db.Integer, default=0)
    broj_nerjesenih = db.Column(db.Integer, default=0)
    stil = db.Column(db.String(255))

class Borba(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.Date)
    runde = db.Column(db.Integer)
    zavrseno_na_bodove = db.Column(db.Boolean)
    nokaut = db.Column(db.Boolean)
    prekid = db.Column(db.Boolean)
    pobjednik_id = db.Column(db.Integer, db.ForeignKey('boksač.id'))
    gubitnik_id = db.Column(db.Integer, db.ForeignKey('boksač.id'))
    pobjednik = db.relationship('Boksač', foreign_keys=[pobjednik_id])
    gubitnik = db.relationship('Boksač', foreign_keys=[gubitnik_id])

@app.route('/')
def pocetna_stranica():
    return render_template('pocetna.html')

# Popis boksača
@app.route('/bokseri')
def popis_boksera():
    bokseri = Boksač.query.all()
    return render_template('popis_boksera.html', bokseri=bokseri)

# Dodavanje novog boksača
@app.route('/dodaj_boksera', methods=['GET', 'POST'])
def dodaj_boksera():
    if request.method == 'POST':
        ime = request.form['ime']
        prezime = request.form['prezime']
        kategorija = request.form['kategorija']
        drzava = request.form['drzava']
        stil = request.form['stil']

        novi_boksač = Boksač(ime=ime, prezime=prezime, kategorija=kategorija, drzava=drzava, stil=stil)
        db.session.add(novi_boksač)
        db.session.commit()
        return redirect(url_for('popis_boksera'))

    return render_template('dodaj_boksera.html')

# Uređivanje postojećeg boksača
@app.route('/uredi_boksera/<int:id>', methods=['GET', 'POST'])
def uredi_boksera(id):
    boksač = Boksač.query.get(id)

    if request.method == 'POST':
        boksač.ime = request.form['ime']
        boksač.prezime = request.form['prezime']
        boksač.kategorija = request.form['kategorija']
        boksač.drzava = request.form['drzava']
        boksač.stil = request.form['stil']

        db.session.commit()
        return redirect(url_for('popis_boksera'))

    return render_template('uredi_boksera.html', boksač=boksač)

# Brisanje boksača
@app.route('/izbrisi_boksera/<int:id>')
def izbrisi_boksera(id):
    boksač = Boksač.query.get(id)
    db.session.delete(boksač)
    db.session.commit()
    return redirect(url_for('popis_boksera'))

# Popis borbi
@app.route('/borbe')
def popis_borbi():
    borbe = Borba.query.all()
    return render_template('popis_borbi.html', borbe=borbe)



@app.route('/dodaj_borbu', methods=['GET', 'POST'])
def dodaj_borbu():
    if request.method == 'POST':
        # Dohvati podatke o borbi iz obrasca
        datum = request.form['datum']
        runde = request.form['runde']
        zavrseno_na_bodove = 'zavrseno_na_bodove' in request.form
        nokaut = 'nokaut' in request.form
        prekid = 'prekid' in request.form
        pobjednik_id = request.form['pobjednik_id']
        gubitnik_id = request.form['gubitnik_id']

        # Provjeri da li se boksači bore sami protiv sebe
        if pobjednik_id == gubitnik_id:
            error_message = "Boksač ne može boriti sam protiv sebe. Odaberite različite boksače."
            flash(error_message, 'error')  # Postavite poruku o grešci sa 'error' kategorijom
            bokseri = Boksač.query.all()
            return render_template('dodaj_borbu.html', bokseri=bokseri)

        # Stvori novu instancu borbe
        nova_borba = Borba(datum=datum, runde=runde, zavrseno_na_bodove=zavrseno_na_bodove,
                           nokaut=nokaut, prekid=prekid, pobjednik_id=pobjednik_id, gubitnik_id=gubitnik_id)

        # Dodaj borbu u bazu podataka
        db.session.add(nova_borba)
        db.session.commit()

        return redirect(url_for('popis_borbi'))

    # Prikaži obrazac za dodavanje borbe
    bokseri = Boksač.query.all()  # Dohvati sve boksače za popunjavanje padajućih izbornika
    return render_template('dodaj_borbu.html', bokseri=bokseri)    # Prikaži obrazac za dodavanje borbe
    


# Brisanje borbe
@app.route('/izbrisi_borbu/<int:id>')
def izbrisi_borbu(id):
    borba = Borba.query.get(id)
    db.session.delete(borba)
    db.session.commit()
    return redirect(url_for('popis_borbi'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
