# Database:
# V Tabel met alle locaties (alleen pk en naam locatie)
# ~V Kindtabel met tegels per locatie
  # ... Kolommen: naam, vijand, tekst, afbeelding voor en achter, evt. later token (tekst kan beter op html-pagina?)
  # V Supermarkt: kassa, bakkerij, olie
  # V Drogist: kassa, magazijn
  # V Slagerij: balie, oven
  # V Warenhuis: kassa?, elektronica, restaurant
# - Tabel met een paar karakters
    # ...# kolommen: naam, foto, waarden voor kracht/slimheid etc., aantal levens, bio, ...?

# - ? Tabel voor bijhouden welke beurt voor tijdlijn ?niet nodig
# - Monsters/vijanden (later pas?)

import sqlite3

conn = sqlite3.connect("./db/testscenario.db")
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS Locatie;
""")
cur.execute("""
DROP TABLE IF EXISTS Tegel;
""")
cur.execute("""
DROP TABLE IF EXISTS Karakter;
""")

cur.execute("""
DROP TABLE IF EXISTS Vijand;
""")

cur.execute("""
CREATE TABLE Locatie (
  id INTEGER PRIMARY KEY,
  naam TEXT
  );
""")

locaties = [(1, "supermarkt"),(2, "warenhuis"),(3, "drogist"),(4, "slagerij")]

cur.executemany("""
INSERT INTO Locatie(id, naam)
VALUES (?,?);
""", locaties)

cur.execute("""
CREATE TABLE Tegel (
  id INTEGER PRIMARY KEY,
  naam TEXT,
  locatie_id INTEGER,
  vijand_id INTEGER,
  tekst TEXT,
  afbeelding_voor TEXT,
  afbeelding_achter TEXT,
  bezocht BOOLEAN,
  foreign key (locatie_id) references Locatie (id)
  on delete cascade
  );
""")

# Schrijf teksten van achterkant tegels uit voor ze in een array te stoppen
text_super_kassa = "Je vraagt de vrouw achter de kassa of zij iets verdachts heeft gezien. Ze zegt van niet, maar er was wel iemand die erg lang bij de olie stond te kijken."
text_super_bakker = "In de bakkerij doet een man broden in en uit een oven. Hij zegt dat de oven erg goed beveiligd is en vorige week nog getest op brandveiligheid."
text_super_olie = "Er staan veel flessen olie in het schap maar ze zitten allemaal goed dicht. Je kunt (met token??) de olie wegvoeren, maar daarmee verlies je [x] sociale vaardigheid."
text_drogist_kassa = "Je vraagt of er brandbare artikelen zijn. De mevrouw achter de kassa zegt dat ze antimuggenvloeistof met brandbaar oplosmiddel hebben. Je kunt dit weghalen, maar daarmee verlies je [x] sociale vaardigheid."
text_drogist_magazijn = "Je ziet een hoop zakken met poeder liggen boven een verwarmingsinstallatie. Je kunt deze wegvoeren (met token?) maar daarmee verlies je [x] sociale vaardigheid."
text_warenhuis_kassa = "De man achter de kassa zegt dat ze regelmatig controleren op brandveiligheid, maar dat er de grootste kans is op iets wat misgaat op de elektronica afdeling."
text_warenhuis_elektronica = "Er liggen veel apparaten met snoeren aangesloten ter demonstratie. Je kunt een aantal apparaten afsluiten maar daarmee verlies je [x] sociale vaardigheid."
text_warenhuis_restaurant = "Er zitten een paar mensen te eten maar het is verder rustig. Er worden warme broodjes geserveerd maar er lijkt niets mis met de oven (door naar nieuwe tegel met token?)"
text_slagerij_balie = "Je ziet niemand dus je kijkt achter de balie. Daar wordt je aangevallen door een boze slager met een mes."
text_slagerij_oven = "Er ligt vlees te bakken, het ruikt lekker. Verder is er niets opvallends."


tegels = [
    (1, "kassa", 1, text_super_kassa, "images/kassa.jpg", "images/kassa.jpg", False),
    (2, "bakkerij", 1, text_super_bakker, "images/bakkerij.jpg", 'images/bakker_achter.jpg', False),
    (3, "olie afdeling", 1, text_super_olie, "images/olie.jpg", "images/olie.jpg", False),
    (4, "kassa", 3, text_drogist_kassa, "images/drogist_kassa.jpg", "images/drogist_kassa_achter.jpg", False),
    (5, "magazijn", 3, text_drogist_magazijn,"images/drogist_magazijn.jpg","images/drogist_magazijn_achter.jpg", False),
    (6, "kassa", 2, text_warenhuis_kassa, "images/warenhuis_kassa_voor.jpg", "images/warenhuis_kassa_achter.jpg", False),
    (7, "elektronica-afdeling", 2, text_warenhuis_elektronica, "images/warenhuis_tvs.jpg", "images/warenhuis_tvs.jpg", False),
    (8, "restaurant", 2, text_warenhuis_restaurant, "images/warenhuis_restaurant.jpg", "images/warenhuis_restaurant.jpg", False),
    (9, "balie", 4, text_slagerij_balie, "images/slagerij_balie.jpg", "images/slagerij_balie_achter.jpg", False),
    (10, "oven", 4, text_slagerij_oven, "images/slagerij_oven.jpg", "images/slagerij_oven.jpg", False)
]

cur.executemany("""
  INSERT INTO Tegel(id, naam, locatie_id, tekst, afbeelding_voor, afbeelding_achter, bezocht)
  VALUES(?,?,?,?,?,?,?)
""", tegels)


cur.execute("""
CREATE TABLE Karakter (
  id INTEGER PRIMARY KEY,
  naam TEXT,
  bio TEXT,
  foto TEXT,
  levens INTEGER,
  kracht INTEGER,
  intelligentie INTEGER,
  sociaal INTEGER
   );
""")

bio_einstein = "Je kent hem wel, briljante man maar niet heel sterk of sociaal vaardig"
bio_hunk = "Een gespierde vent die het van zijn kracht moet hebben, niet van zijn hersenen"

karakters = [
    (1,"Einstein",bio_einstein,"images/Einstein.jpg",5,1,5,2),
    (2,"Hunk",bio_hunk,"images/hunk.jpg",5,5,1,3)
]

cur.executemany("""
INSERT INTO Karakter(id,naam,bio,foto,levens,kracht,intelligentie,sociaal)
  VALUES (?,?,?,?,?,?,?,?)
""", karakters)

cur.execute(""" 
DROP TABLE IF EXISTS Volgende_locatie;
 """)

cur.execute(""" 
CREATE TABLE Volgende_locatie (
id INTEGER PRIMARY KEY,
tegel TEXT
);
""")

cur.execute(""" 
INSERT INTO Volgende_locatie(tegel) VALUES (?)
""", "x")

# Altijd kracht en geen andere metric of strength bij een vijand?
cur.execute(""" 
CREATE TABLE Vijand (
  id INTEGER PRIMARY KEY,
  naam TEXT,
  tegel_id INTEGER,
  levens INTEGER,
  kracht INTEGER,
  foreign key (tegel_id) references Tegel (id)
  on delete cascade
  );
""")

vijanden = [
    (1, "boze slager", 9, 5, 4)
]

cur.executemany(""" 
INSERT INTO Vijand(id, naam, tegel_id, levens, kracht) VALUES (?,?,?,?,?)
""", vijanden)

# Nodig?
cur.execute(""" 
  DROP TABLE IF EXISTS Timeline
""")

# cur.execute("""
# ALTER TABLE Tegel (
#   foreign key (locatie_id) references Locatie (id)
#   );          
# """)

conn.commit()
conn.close()