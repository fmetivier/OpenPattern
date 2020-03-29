import sys
sys.path.append('./..')

import matplotlib.pyplot as plt
#~ from OpenPattern.Points import Point
import OpenPattern as OP



# Women
#~ p = OP.Basic_Bodice(pname = "W44G", gender = 'w', style = 'Gilewska')
#~ p.add_bust_dart()
#~ p.add_waist_dart()
#~ p.draw_bodice({"Pattern":"Bodice without dart"},save=True,paper='Ledger')
#~ p.draw_sleeves()

# Men
#~ p = OP.Basic_Bodice(pname = "M44G", gender = 'm', style = 'Gilewska')
#~ p.draw_bodice({"Pattern":"Basic Shirt"}, save=True, fname='BasicShirt', paper='A4')
#~ p.save_measurements()
#~ p.draw_sleeves()

#~ c = OP.Cuffs(pname = 'M44G', gender = 'm', style = 'Gilewska', cuff_style = 'Simple')
#~ c.draw_cuffs(save=True)

col = OP.Collars(pname = "M44G", gender = 'm', style = 'Gilewska',  collar_style = 'OnePiece', overlap=2, collar_height=2)
col.draw_collar(save=True)

#~ pans = OP.Basic_Trousers()

# Grégoire's pyjama
#~ pans= OP.Pants_block(pname="gregoire")
#~ pans.draw_basic_trousers(dic = {"Pattern":"Basic Trousers"}, save = False, fname = 'Trousers', paper='A4')


plt.show()
