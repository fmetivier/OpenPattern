from OpenPattern.Bodices import *

class shirt(Basic_Bodice):
	

	def __init__(self, collar_ease = 1, sleeve_lowering = 4, side_ease=4):
		pass
		
	def shirt_bodice(self):
		pass
		
	def shirt_sleeve_m(self,ease=3,Slit_length=12, fold_number=3, fold_length=1):
		pass

		#~ if fold_number > 0:
			#~ S = np.array([self.m["tour_poignet"]/2 + ease/2 + 0.5, 0])
			#~ V = np.array([-(self.m["tour_poignet"]/2 + ease/2 + fold_number*fold_length - 0.5), 0])

		# slit 
		# Stb Slit bottom
		#~ Stb = self.middle(np.array([0,0]),V)
		#~ #Stt Slit top
		#~ Stt = Stb + [0,Slit_length]


		#~ if fold_number >= 1:
			#~ f1 = np.array([0,0])+[0.5,0]
			#~ self.Sleeve_points_dic['f1']=f1
		#~ if fold_number >= 2:
			#~ f2 = self.middle(np.array([0,0]),Stb)
			#~ self.Sleeve_points_dic['f2']=f2
		#~ if fold_number >= 3:
			#~ f3 = self.middle(V,Stb)
			#~ self.Sleeve_points_dic['f3']=f3

		#~ self.Sleeve_segments = [[Stt,Stb],[f1,f1-[1,0]],[f2,f2-[1,0]],[f3,f3+[1,0]]]
			
		# draw method
		#~ for seg in self.Sleeve_segments:
		#~ self.segment(seg[0],seg[1],ax,{'color':'0.1','linestyle':'solid'})
