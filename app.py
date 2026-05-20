from flask import Flask, render_template, redirect, request, url_for, session
from datetime import timedelta
import sqlite3
import random as rn

app = Flask(__name__)
app.secret_key = "zeer_stabiel_geheim_dat_nooit_verandert_1234567"

# Database initialisatie NODIG?
def init_timeline():
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS Timeline;    
    """)

    cur.execute("""
        CREATE TABLE Timeline (time INTEGER);
    """
    )
    cur.execute("""
        INSERT INTO Timeline (time) VALUES (-1);
    """)

    conn.commit()
    conn.close()

# App routes ...
@app.route("/")
def home_page():
    success = request.args.get("success")
    return render_template("intro.html", success=success)

@app.route("/overzicht", methods=["GET", "POST"])
# variabele timeline moet 1 toenemen telkens als /overzicht bezocht wordt na 1e keer
    # kan met database of session-variabele
def overzicht():

    # if Timeline #exists#:
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
    UPDATE Timeline SET time = time + 1;
    """)

    # else:
        # init_timeline()

    opgelost = 0    # Ook in database? Of bijhouden niet nodig, want gewoon link vanaf 'oplossing'?
    brand = 0       # Ook in database?
    
    conn.commit()
    cur.execute(""" SELECT * FROM Timeline; """)
    timeline = cur.fetchall() #Hiermee krijg je array met (n,) en met fetchone alleen (n,) waar n=getal


    if timeline[0][0] >= 10:
        brand = 1
    if not brand:
        if request.method == "POST":
            # Alleen voor tegel per locatie # karakter = request.form["karakter"]
            locatie = request.form["locatie"]
            # GOED? open template van de locatie die is ingevuld in form
            # Kan dit beter doen met button voor elke locatie

        return render_template("overzicht.html", timeline=timeline)
    else:
        return render_template("telaat.html")
    
    conn.close()


@app.route("/karakters")
def karakters():

    # Schrijf 1 functie voor deze (>)3 regels
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute(""" 
        SELECT naam, bio, foto, levens, kracht, intelligentie, sociaal
        FROM Karakter;
    """)

    karakters = cur.fetchall()
    conn.commit()
    conn.close()

    return render_template("karakters.html", karakters=karakters)

@app.route("/supermarkt", methods=["GET", "POST"])
def supermarkt():

    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, afbeelding_voor, bezocht FROM Tegel
        WHERE locatie_id = 1;
    """)
    tegels = cur.fetchall() #Check of je nog [n] moet selecteren

    # Haal waarde van locatie op uit form en sla op in database-tabel volgende locatie
    # if request.method == 'POST':
    #     tegel = str(request.form["tegel"]) 
    #     cur.execute(""" 
    #         UPDATE Volgende_locatie
    #         SET tegel = ?
    #         WHERE id = 1;
    #     """, (tegel,))
    # # Updaten van tegel in de database werkt niet, check!

    # conn.commit()
    # conn.close()

    # conn = sqlite3.connect("./db/testscenario.db")
    # cur = conn.cursor()
    # conn.row_factory = sqlite3.Row

    # cur.execute("""
    #     SELECT tegel FROM Volgende_locatie;
    # """)
    # locatie = cur.fetchone()   

    conn.commit()
    conn.close()

    
    #Dit werkt niet, locatie wordt nu niet aangepast adhv ingevuld formulier
        #Ophalen iets als 'volgende locatie' uit database en database aanpassen als formulier wordt ingevuld?
    return render_template("supermarkt.html", tegels=tegels)

@app.route("/warenhuis")
def warenhuis():
    
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, afbeelding_voor, bezocht FROM Tegel
        WHERE locatie_id = 2;
    """)
    tegels = cur.fetchall()

    conn.commit()
    conn.close()

    return render_template("warenhuis.html", tegels=tegels)

@app.route("/drogist")
def drogist():

    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row


    cur.execute("""
        SELECT naam, afbeelding_voor, bezocht FROM Tegel
        WHERE locatie_id = 3;
    """)
    tegels = cur.fetchall() #Check of je nog [n] moet selecteren

    conn.commit()
    conn.close()

    return render_template("drogist.html", tegels=tegels)    

@app.route("/slagerij")
def slagerij():

    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, afbeelding_voor, bezocht FROM Tegel
        WHERE locatie_id = 4;
    """)
    tegels = cur.fetchall() #Check of je nog [n] moet selecteren

    conn.commit()
    conn.close()

    return render_template("slagerij.html", tegels=tegels)

# App-routes voor tegels per locatie
@app.route("/supermarkt/kassa")
def supermarkt_kassa():
    
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, tekst, afbeelding_achter FROM Tegel
        WHERE id = 1;
    """)
    tegel = cur.fetchone() #Nu is tegel[0] de tekst als string en tegel[1] de url voor afbeelding als string

    cur.execute("""
        SELECT bezocht FROM Tegel
        WHERE id = 1;
    """)
    bezocht = cur.fetchone()
    if not bezocht[0]:
        cur.execute(""" 
            UPDATE TEGEL SET bezocht = True
            WHERE id = 1;
        """)

    conn.commit()
    conn.close()

    return render_template("supermarkt_tegel.html", tegel=tegel)

@app.route("/supermarkt/bakkerij")
def supermarkt_bakkerij():

    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, tekst, afbeelding_achter FROM Tegel
        WHERE id = 2;
    """)
    tegel = cur.fetchone() #Nu is tegel[0] de tekst als string en tegel[1] de url voor afbeelding als string

    cur.execute("""
        SELECT bezocht FROM Tegel
        WHERE id = 2;
    """)
    bezocht = cur.fetchone()
    if not bezocht[0]:
        cur.execute(""" 
            UPDATE TEGEL SET bezocht = True
            WHERE id = 2;
        """)

    conn.commit()
    conn.close()
    return render_template("supermarkt_tegel.html", tegel=tegel)

@app.route("/supermarkt/olie")
def supermarkt_olie():

    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, tekst, afbeelding_achter FROM Tegel
        WHERE id = 3;
    """)
    tegel = cur.fetchone() #Nu is tegel[0] de tekst als string en tegel[1] de url voor afbeelding als string

    cur.execute("""
        SELECT bezocht FROM Tegel
        WHERE id = 3;
    """)
    bezocht = cur.fetchone()
    if not bezocht[0]:
        cur.execute(""" 
            UPDATE TEGEL SET bezocht = True
            WHERE id = 3;
        """)

    conn.commit()
    conn.close()

    return render_template("supermarkt_tegel.html", tegel=tegel)

@app.route("/drogist/kassa")
def drogist_kassa():

    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, tekst, afbeelding_achter FROM Tegel
        WHERE id = 4;
    """)
    tegel = cur.fetchone() #Nu is tegel[0] de tekst als string en tegel[1] de url voor afbeelding als string

    cur.execute("""
        SELECT bezocht FROM Tegel
        WHERE id = 4;
    """)
    bezocht = cur.fetchone()
    if not bezocht[0]:
        cur.execute(""" 
            UPDATE TEGEL SET bezocht = True
            WHERE id = 4;
        """)

    conn.commit()
    conn.close()

    return render_template("drogist_tegel.html", tegel=tegel)

@app.route("/drogist/magazijn")
def drogist_magazijn():
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, tekst, afbeelding_achter FROM Tegel
        WHERE id = 5;
    """)
    tegel = cur.fetchone() #Nu is tegel[0] de tekst als string en tegel[1] de url voor afbeelding als string

    cur.execute("""
        SELECT bezocht FROM Tegel
        WHERE id = 5;
    """)
    bezocht = cur.fetchone()
    if not bezocht[0]:
        cur.execute(""" 
            UPDATE TEGEL SET bezocht = True
            WHERE id = 5;
        """)

    conn.commit()
    conn.close()

    return render_template("drogist_tegel.html", tegel=tegel)

@app.route("/warenhuis/kassa")
def warenhuis_kassa():
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, tekst, afbeelding_achter FROM Tegel
        WHERE id = 6;
    """)
    tegel = cur.fetchone()

    cur.execute("""
        SELECT bezocht FROM Tegel
        WHERE id = 6;
    """)
    bezocht = cur.fetchone()
    if not bezocht[0]:
        cur.execute(""" 
            UPDATE TEGEL SET bezocht = True
            WHERE id = 6;
        """)

    conn.commit()
    conn.close()
    return render_template("warenhuis_tegel.html", tegel=tegel)

@app.route("/warenhuis/elektronica")
def warenhuis_elektronica():
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, tekst, afbeelding_achter FROM Tegel
        WHERE id = 7;
    """)
    tegel = cur.fetchone()

    cur.execute("""
        SELECT bezocht FROM Tegel
        WHERE id = 7;
    """)
    bezocht = cur.fetchone()
    if not bezocht[0]:
        cur.execute(""" 
            UPDATE TEGEL SET bezocht = True
            WHERE id = 7;
        """)

    conn.commit()
    conn.close()
    return render_template("warenhuis_tegel.html", tegel=tegel)

@app.route("/warenhuis/restaurant")
def warenhuis_restaurant():
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT naam, tekst, afbeelding_achter FROM Tegel
        WHERE id = 8;
    """)
    tegel = cur.fetchone()

    cur.execute("""
        SELECT bezocht FROM Tegel
        WHERE id = 8;
    """)
    bezocht = cur.fetchone()
    if not bezocht[0]:
        cur.execute(""" 
            UPDATE TEGEL SET bezocht = True
            WHERE id = 8;
        """)

    conn.commit()
    conn.close()
    return render_template("warenhuis_tegel.html", tegel=tegel) 

@app.route("/slagerij/balie")
def slagerij_balie():
    # Gevecht met paranoïde slager met mes
    # Krachtscore is 4, 'worp' is een random nummer van 0 t/m (krachtscore + 1)
        # Dus voor slager is dit 0 t/m 5
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT tekst, afbeelding_achter FROM Tegel
        WHERE id = 9;
    """)
    tegel = cur.fetchone()

    # Geef onderstaande de variabele naam van het karakter mee!
    naam = "Hunk"   # Dit later weg, haal karakter uit database
    cur.execute("""
        SELECT kracht FROM Karakter
        WHERE naam = (?)
     """, (naam,))
    self_kracht = cur.fetchone()[0]

    cur.execute("""
        SELECT kracht FROM Vijand
        WHERE tegel_id = 9;
     """)
    other_kracht = cur.fetchone()[0]

    cur.execute(""" 
        SELECT levens FROM Karakter
        WHERE naam = (?)
    """, (naam,))
    self_levens = cur.fetchone()[0] #Nodig om deze variabele te maken als je database waarde update?

    cur.execute("""
        SELECT levens FROM Vijand
        WHERE tegel_id = 9;
     """)
    other_levens = cur.fetchone()[0]

    # WAAROM DIT?
    cur.execute(""" SELECT * FROM Timeline; """)
    timeline = cur.fetchall() #Hiermee krijg je array met (n,) en met fetchone alleen (n,) waar n=getal

    # Dit kan ook met recursief programmeren, vooral als vijand 'defensiever' wordt als weinig levens
    # Zorg voor manier om dit interactief te maken zodat je gevecht ook kan zien
    while self_levens > 0 and other_levens > 0:
        # Laat bij elke JavaScript-interactie met button een worp plaatsvinden
            # Denk dat deze worpen in JavaScript moeten plaatsvinden
        self_worp = rn.choice(range(self_kracht + 2))
        other_worp = rn.choice(range(other_kracht + 2))
        if other_worp > self_worp:
            self_levens -= 1
            cur.execute("""
            UPDATE Karakter SET levens = levens - 1
            WHERE naam = (?);
            """, (naam,))
        # elif other_worp == self_worp:
        #   continue
        else:
            other_levens -=1
            cur.execute(""" 
            UPDATE Vijand SET levens = levens -1
            WHERE tegel_id = 9;
            """)

    # Staat tegel als bezocht merken nu op juiste plek?
    cur.execute("""
        SELECT bezocht FROM Tegel
        WHERE id = 9;
    """)
    bezocht = cur.fetchone()
    if not bezocht[0]:
        cur.execute(""" 
            UPDATE TEGEL SET bezocht = True
            WHERE id = 9;
        """)

    conn.commit()
    conn.close()
    return render_template("slagerij_balie.html", tegel=tegel)

@app.route("/slagerij/oven")
def slagerij_oven():
    
    conn = sqlite3.connect("./db/testscenario.db")
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row

    cur.execute("""
        SELECT tekst, afbeelding_achter FROM Tegel
        WHERE id = 10;
    """)
    tegel = cur.fetchone() #Nu is tegel[0] de tekst als string en tegel[1] de url voor afbeelding als string

    cur.execute("""
        SELECT bezocht FROM Tegel
        WHERE id = 10;
    """)
    bezocht = cur.fetchone()
    if not bezocht[0]:
        cur.execute(""" 
            UPDATE TEGEL SET bezocht = True
            WHERE id = 10;
        """)

    conn.commit()
    conn.close()

    return render_template("slagerij_oven.html", tegel=tegel)

# App-route voor oplossing #

@app.route("/oplossing", methods=["GET", "POST"])
def oplossing():
    if request.method == "POST":
        oplossing = str(request.form.get("oplossing"))
        if 'poeder' in oplossing and 'drogist' in oplossing and 'magazijn' in oplossing:
            return render_template("oplossing.html", success=True)

        else:
            return render_template("oplossing.html", success=False)
    
    return render_template("oplossing.html", success=False)


# -----------------------------
# APP STARTEN
# -----------------------------
if __name__ == "__main__":
    init_timeline()
    app.run(debug=True)