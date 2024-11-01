#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# if python setup.py install goes well these two lines are not needed
#
# import sys
# sys.path.append("../")
#
# just uncomment the lines you whish to test.

import matplotlib.pyplot as plt

import OpenPattern as OP
import numpy as np


####################################################
#
# Check the database
#
#####################################################
#
# dbPATH = "/home/metivier/Nextcloud/Personnel/couture/OpenPattern/OpenPattern/data/measurements.db"

p = OP.Pattern(pname="Esther")
print(p.dbPATH)
print("ALLER")
for key, val in p.m.items():
    if 'tour' in key:
        print(key, val)
#
#
# p.m["longueur_epaule"] = 14
# p.save_measurements_sql(p.pname)
#
# print("MISE A ZERO")
# p.m = {}
# for key, val in p.m.items():
#     print(key, val)
#
# print("RETOUR")
# p.m = p.get_measurements_sql(p.pname)
# for key, val in p.m.items():
#     print(key, val)
#

####################################################
#
# Load measurements
#
#####################################################

# p = OP.Pattern()
# p.load_measurements("../measurements/measurement_sheet_Esther.csv")

####################################################
#
# Draw a bow tie
#
#####################################################
#
# p = OP.Bowtie(pname="M42W", width=5, pointe=1, figPATH="../samplePatterns/")
# p.draw(save=True, fname="diamond_42")
# plt.show()

####################################################
#
# Skirt
#
#####################################################


# p = OP.Basic_Skirt(
#     pname="W6C",
#     style="Chiappetta",
#     figPATH="../samplePatterns/",
#     frmt="svg",
# )
# p.draw()

####################################################
#
# Culotte
#
#####################################################

# p = OP.Culotte(
#     pname="W40D",
#     style="Donnanno",
#     ease=1,
#     figPATH="../samplePatterns/",
#     frmt="svg",
# )
# p.draw(save=True, fname="culotte")

# create a waist band
# w = OP.Waistband(pname="W4OD", ease=2)
# w.draw(save=True, paper="A4", fname="culotte_waist")


####################################################
#
# Bodices
# Women
#
#####################################################


# p = OP.Basic_Bodice(pname="Esther", gender="w", style="Donnanno")
# p.draw_bodice()
# p.draw_sleeves()
#
# p = OP.Basic_Bodice(pname="Esther", gender="w", style="Chiappetta")
# p.draw_bodice()
# p.draw_sleeves()
#
# p = OP.Basic_Bodice(pname="W36G", gender="w", style="Gilewska")
# p.add_bust_dart()
# p.add_waist_dart()
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

####################################################
#
# Men Bodice
#
#####################################################

# p = OP.Basic_Bodice(pname="Me", gender="m", style="Chiappetta")
# p.draw_bodice()
#
# p = OP.Basic_Bodice(pname="M44G", gender="m", style="Gilewska")
# p.draw_bodice()
#
# p = OP.Basic_Bodice(pname="Me", gender="m", style="Donnanno", ease=10)
# p.draw_bodice()

# p.chiappetta_armhole_sleeve_m()
# p.draw()
# p.draw_sleeves()


# p = OP.Shirt(pname="Me", gender="m", style="Chiappetta", ease=0, side_ease=3)
# p.basic_shirt_bodice(style="Chiappetta")
# p.chiappetta_basic_sleeve_m()

# p.draw_sleeves()
# p.draw()

# p.chiappetta_armhole_sleeve_m(ease=5, folds=1, fold_width=1, fente=11, wrist=5)
# p.draw_sleeves(save=True, paper="A4")
# p.draw(save=True, paper="A4")
# #
# # p.draw_subpatterns(overlay=True)
#
# cu = OP.Cuffs(pname="Me", gender="M", cuff_style="French", width=7, overlap=2)
# cu.draw_cuffs()
# #
# co = OP.Collars(
#     pname="Me",
#     gender="m",
#     collar_style="TwoPieces",
#     overlap=2,
#     longueur_col_dos=9.75,
#     longueur_col_devant=14,
#     up_collar_height=5,
# )
# co.draw_collar(save=True, paper="A4")
# # #
# pl = OP.Placket(pname="Me", gender="m", placket_style="SimpleOneSide", slit_length=11)
# pl.draw_placket(save=True)


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


####################################################
#
# Trousers
#
####################################################


# pans = OP.Basic_Trousers(
#     pname="M44D",
#     gender="m",
#     style="Donnanno",
#     darts=True,
#     figPATH="../docs/samplePatterns/",
#     frmt="svg",
# )
# pans.Donnanno_add_darts()
#
# pans.draw_basic_trousers(dic={"Pattern": "Basic trousers with dart"}, save=False)

# Grégoire's bermudas
# b = OP.Bermudas(pname="gregoire", gender="m")
# b.draw()

# pans = OP.Flared_pants(pname="sophie", gender="w")

# bp = OP.Pants_block(pname="M46D",gender="m", overlay=False, save=True, paper='A4')

####################################################
#
# In test
# Bespoke adjustments
#
####################################################

# waist_fit_dic={'sides': 1.5, 'center_front': 0.5, 'front_left': 0, 'front_right': 0, 'center_back': 0, 'back':0}

# pans = OP.Basic_Trousers( pname="sophie", gender='w', style='Donnanno', darts=False, wfd = waist_fit_dic)
# pans.draw_basic_trousers(dic = {"Pattern":"Basic Trousers"}, save = False, fname = 'Trousers')
# #
# b = OP.Bermudas(pname="sophie", gender='w' ,wfd = waist_fit_dic)
# b.draw()


####################################################
#
# Waist coat (incomplete)
#
####################################################


# wc = OP.Waist_Coat(overlap=False)
# wc.draw()
plt.show()
