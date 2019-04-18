import cv2
import math
import req1, req2, req3, req4

def main():
	menu = {}
	menu['1']="- Requisito 1"
	menu['2']="- Requisito 2"
	menu['3']="- Requisito 3"
	menu['4']="- Requisito 4"
	menu['5']="- Sair"
	while True:
		print('-------MENU-------')
		options=menu.keys()
		options = sorted(menu)
		for entry in options:
			print (entry, menu[entry])
		selection=input("Selecione: ")
		print('------------------')
		if selection =='1':
			req1.main()
			print()
		elif selection =='2':
			req2.main()
			print()
		elif selection =='3':
			req3.main()
			print()
		elif selection =='4':
			req4.main()
			print()
		elif selection == '5':
			break
		else:
			print ("Opcao invalida.")


if __name__  == "__main__":
	main()