#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('./..')

import matplotlib.pyplot as plt
#~ from OpenPattern.Points import Point

import OpenPattern as OP
import numpy as np




# Skirts
# # p = OP.Basic_Skirt(pname='W16C')
# p.draw()
# ease=8

##################

# p = OP.Basic_Skirt(pname='W38G',style='Gilewska',curves=True)
# p.draw()
# w = OP.Waistband(pname='W40D')
# w.draw()



# Women
# p = OP.Basic_Bodice(pname = "W36G", gender = 'w', style = 'Gilewska')
# p.add_bust_dart()
# p.add_waist_dart()
# p.draw_bodice({"Pattern":"Bodice with darts"},save=True,paper='A4')
# p.draw_sleeves()

# Men
# p = OP.Basic_Bodice(pname="M40mC", style='Chiappetta')
# p.chiappetta_armhole_sleeve_m()
# p.draw()
# p.draw_sleeves()


p = OP.Shirt(pname="gregoire", gender='m', age=16)
p.basic_shirt_bodice(style="G")
p.chiappetta_armhole_sleeve_m(ease=3,folds=1,fold_width=1,fente=11, wrist=5)
p.draw_sleeves()
p.draw()
# p.draw_subpatterns(overlay=True)

cu = OP.Cuffs(pname="gregoire",gender='m',cuff_style='French',width=5,ease=3,overlap=2)
cu.draw_cuffs()

co = OP.Collars(pname='gregoire',gender='m',collar_style='TwoPieces',overlap=2)
co.draw_collar()




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

# pans = OP.Basic_Trousers( pname="sophie", gender='w', style='Donnanno', darts=False)
# pans.Donnanno_add_darts()
# pans.draw_basic_trousers(dic = {"Pattern":"Basic Trousers"}, save = False, fname = 'Trousers')

# Gregoire's pyjama
# pans= OP.Basic_Trousers(pname="gregoire",gender="m",style="Donnanno")
# pans.Donnanno_add_darts()
# pans.draw_basic_trousers(dic = {"Pattern":"Basic Trousers"}, save = False, fname = 'Trousers')

# bp = OP.Pants_block(pname="sophie",gender="w", overlay=False)
#
# bp = OP.Pants_block(pname="M46D",gender="m", overlay=False, save=True, paper='A4')

#pans = OP.Flared_pants( pname="sophie", gender='w')

plt.show()
