#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# if python setup.py install goes well these two lines are not needed
#
# import sys
# sys.path.append("../")
import matplotlib.pyplot as plt

import OpenPattern as OP
import numpy as np


####################################################
#
# check the database
#
#####################################################

# p = OP.Pattern(pname="gregoire")
# for key, val in p.m.items():
#     print(key, val)

####################################################
#
# load measurements
#
#####################################################

# p = OP.Pattern(dbPATH="../measurements/")
# p.load_measurements("../measurements/measurement_sheet_Esther.csv")

####################################################
#
# Bow tie
#
#####################################################

# p = OP.Bowtie(width=5, pointe=1)
# plt.show()

####################################################
#
# Skirt
#
#####################################################


p = OP.Basic_Skirt(
    pname="W6C",
    style="Chiappetta",
    figPATH="../samplePatterns/",
    frmt="svg",
)
p.draw()

####################################################
#
# Culotte
#
#####################################################

# p = OP.Culotte(
#     pname="sophie",
#     style="Donnanno",
#     ease=1,
#     dbPATH="../measurements/",
#     figPATH="../samplePatterns/",
#     frmt="svg",
# )
# p.draw(save=True, fname="culotte")


# w = OP.Waistband(pname="sophie", ease=2)
# w.draw(save=True, paper="A4", fname="culotte_waist")


####################################################
#
# Bodice
#
#####################################################

# Women
# p = OP.Basic_Bodice(
#     pname="Esther", gender="w", style="Gilewska", dbPATH="../measurements/"
# )
# p.draw_bodice()
# p.draw_sleeves()
#
# p = OP.Basic_Bodice(
#     pname="Esther", gender="w", style="Donnanno", dbPATH="../measurements/"
# )
# p.draw_bodice()
# p.draw_sleeves()

# p = OP.Basic_Bodice(
#     pname="W36G", gender="w", style="Gilewska", dbPATH="../measurements/"
# )
# p.add_bust_dart()
# p.add_waist_dart()
#
# p.draw_bodice()
# p.draw_sleeves()


##############################
#
# Esther shirt dress:
#
##############################

# p = OP.Shirt(
#     pname="Esther",
#     gender="w",
#     style="Chiappetta",
#     age=16,
#     dbPATH="../measurements/",
#     figPATH="../samplePatterns/",
#     overlay=True,
#     hip=True,
#     lower_length=60 - 12,  # waist-knee depth
# )
#
# p.basic_shirt_bodice()
# p.chiappetta_armhole_sleeve_m()
# #
# p.draw({"Pattern": "Robe-chemise"}, paper="A4", save=True)
# p.draw_sleeves(paper="A4", fname="manche_esther", save=True)
# p.draw_bodice()
# p.draw_sleeves()

# p.add_bust_dart()
# p.add_waist_dart()
# p.draw({"Pattern":"Bodice with darts"},save=True)
# p.draw_sleeves()

####################################################
#
# Men Bodice
#
#####################################################

# p = OP.Basic_Bodice(
#     pname="Me", gender="m", style="Chiappetta", dbPATH="../measurements/"
# )
# p.draw_bodice()
# p = OP.Basic_Bodice(pname="M40G", gender="m", style="Gilewska")
# p.draw_bodice()
# p = OP.Basic_Bodice(pname="M44D", gender="m", style="Donnanno", ease=10)
# p.draw_bodice()
# p.chiappetta_armhole_sleeve_m()
# p.draw()
# p.draw_sleeves()


# p = OP.Shirt(pname="Me", gender='m', style = "Gilewska")
# p.basic_shirt_bodice(style="Gilewska")
# p.chiappetta_basic_sleeve_m()
# p.draw_sleeves()
# p.chiappetta_armhole_sleeve_m(ease=3,folds=1,fold_width=1,fente=11, wrist=5)
# p.draw_sleeves()
# p.draw(save=True,paper='A4')
#
# p.draw_subpatterns(overlay=True)

# cu = OP.Cuffs(pname="Me",gender='M',cuff_style='Simple',width=7,overlap=2)
# cu.draw_cuffs()
#
# co = OP.Collars(pname='Me',gender='m',collar_style='TwoPieces',overlap=2)
# co.draw_collar()
#


####################################################
#
# Hospital Gown
#
#####################################################

# p = OP.Hospital_Gown()
# p.draw_gown()
# p.draw_sleeves()

# p = OP.Basic_Bodice(pname = "M44D", gender = 'm', style = 'Donnanno', ease=24)
# p.draw_bodice({"Pattern":"Basic Shirt"}, save=True, fname='BasicShirt', paper='A4')

# p.save_measurements()
# p.draw_sleeves()

####################################################
#
# Cuffs, collars and plackets
#
#####################################################

# c = OP.Cuffs(pname = 'M44G', gender = 'm', style = 'Gilewska', cuff_style = 'Simple')
# c.draw_cuffs(save=True)

# col = OP.Collars(pname = "M44G", gender = 'm', style = 'Gilewska',  collar_style = 'TwoPieces', overlap=2, collar_height=3)
# col.draw_collar(save=True)

# p = OP.Placket(pname = "M44G", gender = 'm', placket_style = 'SimpleOneSide', slit_length = 10)
# p.draw_placket()


####################################################
#
# Pans
#
#####################################################


# Grégoire's pans
# pans = OP.Basic_Trousers(
#     pname="M44D",
#     gender="m",
#     style="Donnanno",
#     darts=True,
#     dbPATH="../measurements/",
#     figPATH="../docs/samplePatterns/",
#     frmt="svg",
# )
# pans.Donnanno_add_darts()

# pans.draw_basic_trousers(dic={"Pattern": "Basic trousers with dart"}, save=True)

# Grégoire's bermudas BUGGED
# b = OP.Bermudas(pname="gregoire", gender="m", dbPATH="../measurements/")
# b.draw()


# waist_fit_dic={'sides': 1.5, 'center_front': 0.5, 'front_left': 0, 'front_right': 0, 'center_back': 0, 'back':0}
# pans = OP.Basic_Trousers( pname="sophie", gender='w', style='Donnanno', darts=False, wfd = waist_fit_dic)
# pans.draw_basic_trousers(dic = {"Pattern":"Basic Trousers"}, save = False, fname = 'Trousers')
# #
# b = OP.Bermudas(pname="sophie", gender='w' ,wfd = waist_fit_dic)
# b.draw()

# bp = OP.Pants_block(pname="sophie",gender="w", overlay=False)
#
# bp = OP.Pants_block(pname="M46D",gender="m", overlay=False, save=True, paper='A4')

# pans = OP.Flared_pants( pname="sophie", gender='w')


plt.show()
