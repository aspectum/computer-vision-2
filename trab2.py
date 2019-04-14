import cv2
import numpy as np
import math
import req2, req3

def main():
	menu = {}
	menu['1']="- Requisito 1" 
	menu['2']="- Requisito 2"
	menu['3']="- Requisito 3"
	menu['4']="- Requisito 4"
	menu['5']="- Sair"

	while True: 
		options=menu.keys()
		options = sorted(menu)
		for entry in options:
			print (entry, menu[entry])
		selection=input("Selecione: ") 
		if selection =='1': 
			import req1			
		elif selection =='2':
			req2.main()
			print()
		elif selection =='3': 
			req3.main()
			print()
		elif selection =='4': 
			pass
		elif selection == '5': 
			break
		else: 
			print ("Opcao invalida.")

if __name__  == "__main__":
	main()