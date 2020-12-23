import sqlite3
import json

def creation():
    conn = sqlite3.connect('measurements.db')
    c = conn.cursor()

    c.execute("""
    create table who (
    wkey varchar(255) not null primary key,
    comment varchar(255),
    date_meas date,
    gender varchar(1)
    )
    """)

    c.execute("""
    create table measurements (
    wkey varchar(255),
    mtype varchar(255),
    mval float );""")

    conn.commit()
    conn.close()

def drop():
    conn = sqlite3.connect('measurements.db')
    c = conn.cursor()

    print(c.execute(""" drop table measurements"""))
    print(c.execute(""" drop table who"""))


def load_data(pname):
    conn = sqlite3.connect('measurements.db')
    c = conn.cursor()

    with open("../measurements/" + pname + "_data.json", "r") as read_file:
        dic = json.load(read_file)

    if "G" in pname and "C" not in pname:
        comment = "Gilewska"
    elif "D" in pname:
        comment =  "Donnanno"
    elif "W" in pname:
        comment = "Wargnier"
    elif "C" in pname:
        comment = "Chiapetta"
    else:
        comment = ""

    if pname[0] == "G":
        pname.replace("G","B")
        gender = "B"
    elif pname[0] == "W":
        gender = "W"
    elif pname[0] == "M":
        gender = "M"
    elif pname[0] == "sophie":
        gender = "W"
        comment = "Sophie Métivier sur mesure"
    elif pname == "gregoire":
        gender = "B"
        comment = "Grégoire Métivier sur mesure"
    else:
        gender = ""

    c.execute("""insert into who (wkey, comment, gender) values (?,?,?)""", (pname,comment,gender))


    for key, val in dic.items():
        c. execute("insert into measurements values (?,?,?)", (pname,key,val))

    conn.commit()
    conn.close()

# drop()
# creation()
# measlist = ["sophie","G6C","G8C","G10C","G12C","G14C","G16C","gregoire","M36G","M38G","M38W","M40G","M40W","M42G","M42W","M44D","M44G","M44W","M46D","M46G","M46W","M48D","M48G","M48W","M50D","M50G","M52D","M52G","M54D","M54G","W34G","W36G","W38G","W40G","W42G","W44G","W46G","W48G"]
# for pname in measlist:
#     load_data(pname)
