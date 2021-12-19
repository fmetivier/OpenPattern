#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('./..')

import matplotlib.pyplot as plt
#~ from OpenPattern.Points import Point

import OpenPattern as OP
import numpy as np




# Skirts
# p = OP.Basic_Skirt(pname='sophie',style='Donnanno')
# p.draw()

# p = OP.Culotte(pname='sophie',style='Donnanno',ease=1)
# p.draw(save=True,paper='A4',fname='culotte')


##################

# w = OP.Waistband(pname='sophie',ease=2)
# w.draw(save=True,paper='A4',fname='culotte_waist')



# Women
# p = OP.Basic_Bodice(pname = "W36G", gender = 'w', style = 'Gilewska')
# p.add_bust_dart()
# p.add_waist_dart()
# p.draw({"Pattern":"Bodice with darts"},save=True)
# p.draw_sleeves()

# Men
p = OP.Basic_Bodice(pname="Me", style='Chiappetta')
# p.chiappetta_armhole_sleeve_m()
# p.draw()
# p.draw_sleeves()


# p = OP.Shirt(pname="Me", gender='m')
# p.basic_shirt_bodice(style="G")
# p.chiappetta_basic_sleeve_m()
# p.draw_sleeves()
# p.chiappetta_armhole_sleeve_m(ease=3,folds=1,fold_width=1,fente=11, wrist=5)
# p.draw_sleeves(save=True,paper='A4')
# p.draw(save=True,paper='A4')
#
# p.draw_subpatterns(overlay=True)

cu = OP.Cuffs(pname="Me",gender='M',cuff_style='Simple',width=5,ease=3,overlap=2)
cu.draw_cuffs(save=True)
#
# co = OP.Collars(pname='Me',gender='m',collar_style='TwoPieces',overlap=2)
# co.draw_collar(save=True)




# p = OP.Hospital_Gown()
# p.draw_gown()
# p.draw_sleeves()

# p = OP.Basic_Bodice(pname = "M44D", gender = 'm', style = 'Donnanno', ease=24)
# p.draw_bodice({"Pattern":"Basic Shirt"}, save=True, fname='BasicShirt', paper='A4')

# p.save_measurements()
# p.draw_sleeves()

# c = OP.Cuffs(pname = 'M44G', gender = 'm', style = 'Gilewska', cuff_style = 'Simple')
# c.draw_cuffs(save=True)

# col = OP.Collars(pname = "M44G", gender = 'm', style = 'Gilewska',  collar_style = 'TwoPieces', overlap=2, collar_height=3)
# col.draw_collar(save=True)

# p = OP.Placket(pname = "M44G", gender = 'm', placket_style = 'SimpleOneSide', slit_length = 10)
# p.draw_placket()

# waist_fit_dic={'sides': 1.5, 'center_front': 0.5, 'front_left': 0, 'front_right': 0, 'center_back': 0, 'back':0}
# pans = OP.Basic_Trousers( pname="sophie", gender='w', style='Donnanno', darts=False, wfd = waist_fit_dic)
# pans.draw_basic_trousers(dic = {"Pattern":"Basic Trousers"}, save = False, fname = 'Trousers')
# #
# b = OP.Bermudas(pname="sophie", gender='w' ,wfd = waist_fit_dic)
# b.draw()

# Gregoire's pyjama
# pans= OP.Basic_Trousers(pname="gregoire",gender="m",style="Donnanno")
# pans.Donnanno_add_darts()
# pans.draw_basic_trousers(dic = {"Pattern":"Basic Trousers"}, save = False, fname = 'Trousers')

# bp = OP.Pants_block(pname="sophie",gender="w", overlay=False)
#
# bp = OP.Pants_block(pname="M46D",gender="m", overlay=False, save=True, paper='A4')

#pans = OP.Flared_pants( pname="sophie", gender='w')

plt.show()
