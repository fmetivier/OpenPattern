import sqlite3
import json
import numpy as np

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


def chiapetta_load():

    conn = sqlite3.connect('measurements.db')
    c = conn.cursor()

    f = open("/home/metivier/Nextcloud/Personnel/couture/OpenPattern/measurements/Gregoire16.csv")

    entete = f.readline()
    entete = entete.strip("\n").split(";")
    for i in np.arange(len(entete)-1)+1:
        if entete[i] != '':
            key = 'Gregoire16'
            c.execute("""insert into who (wkey, comment, gender) values (?,?,?)""", (key,"Gregoire mai 2021","M"))


    meas =  f.readlines()
    for m in meas:
        m  = m.strip("\n").split(";")
        for i in np.arange(len(m)-1)+1:
            if m[i] != '':
                key = 'Gregoire16'
                print('taille', entete[i],m[0],m[i])
                c. execute("insert into measurements values (?,?,?)", (key,m[0],m[i]))


    conn.commit()
    conn.close()

def donnanno_w_load():

    conn = sqlite3.connect('measurements.db')
    c = conn.cursor()

    f = open("/home/metivier/Nextcloud/Personnel/couture/OpenPattern/measurements/DonnannoW.csv")

    entete = f.readline()
    entete = entete.strip("\n").split(";")
    for i in np.arange(len(entete)-1)+1:
    #for i in [10]:
        if entete[i] != '':
            key = 'W' + str(entete[i]) + 'D'
            c.execute("""insert into who (wkey, comment, gender) values (?,?,?)""", (key,"Donnanno","W"))


    meas =  f.readlines()
    for m in meas:
        m  = m.strip("\n").split(";")
        for i in np.arange(len(m)-1)+1:
        # for i in [10]:
            if m[i] != '':
                key = 'W' + str(entete[i]) + 'D'
                print('age', entete[i],m[0],m[i])
                c. execute("insert into measurements values (?,?,?)", (key,m[0],m[i]))


    conn.commit()
    conn.close()

def table_meas():

    sql="""select mtype, sum(wkey = 'W36G') as WG, sum(wkey='M36G') as MG,
    sum(wkey='W40D') as WD, sum(wkey='M44D') as MD, sum(wkey='M38W') as MW, sum(wkey='W10C') as WC,
    sum(wkey='G10C') as GC, sum(wkey='M38mC') as MC from measurements group by mtype;"""

    conn = sqlite3.connect('measurements.db')
    c = conn.cursor()

    f=open("tableau_croise.tex",'w')
    f.write("""\\begin{tabular}{lllllllll}\n
    Mesure& FG & MG & WD & MD & MW & WC & GC & MC\\\\ \n""")
    for row in c.execute(sql):
        st = row[0].replace('_','\_')
        for i in range(8):
            if row[i+1]==1:
                st += "&X"
            else:
                st += "&"
        st+="\\\\ \\hline \n"
        f.write(st)

    f.close()

# drop()
# creation()
# measlist = ["sophie","G6C","G8C","G10C","G12C","G14C","G16C","gregoire","M36G","M38G","M38W","M40G","M40W","M42G","M42W","M44D","M44G","M44W","M46D","M46G","M46W","M48D","M48G","M48W","M50D","M50G","M52D","M52G","M54D","M54G","W34G","W36G","W38G","W40G","W42G","W44G","W46G","W48G"]
# for pname in measlist:
#     load_data(pname)
chiapetta_load()

#donnanno_w_load()
#table_meas()
