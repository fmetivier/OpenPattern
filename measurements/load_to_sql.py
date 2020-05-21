#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 15:07:04 2020

@author: metivier
"""
from OpenPattern.Pattern import Pattern
import sqlite3
import json


with open("../measurements/" + pname + "_data.json", "r") as read_file:
    dic = json.load(read_file)



	#syntax sqlite
	#~ conn = sqlite3.connect('test.db')
	#~ c=conn.cursor()

	#~ c.execute("""create table runparams (idrun int, Npoints int, N_steps int, p_tot int, w_tot int)""")
	#~ c.execute("""create table hits (idrun int, point_number int, t int, neighbour int)""")
	#~ c.execute("select max(rowid) from runparams")
	#~ max_number = c.fetchone()
	#~ print(max_number)
	#~ if  max_number[0] == None:
		#~ max_number = [0]


     #~ cursor.execute("insert into runparams values (?,?,?,?,?)", (RN, N_points, N_steps, sum(neighbour_list), sum(wall_list)))
	#~ conn.commit()
