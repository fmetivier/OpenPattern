#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('./..')

import matplotlib.pyplot as plt
#~ from OpenPattern.Points import Point
import OpenPattern as OP
import numpy as np




#
p = OP.Basic_Skirt(pname='W14C')
p.draw_skirt()

# Women
# p = OP.Basic_Bodice(pname = "W36G", gender = 'w', style = 'Gilewska')
# p.add_bust_dart()
# p.add_waist_dart()
# p.draw_bodice({"Pattern":"Bodice with darts"},save=True,paper='A4')
# p.draw_sleeves()

# Men
# p = OP.Basic_Bodice(hip=False)
# p.draw_bodice()

# p = OP.Waist_Coat()



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
