#--------------------------------------------#
#-------------->Generate pass <--------------#
# Programme permettant de generer un mot de passe aleatoire avec un nombre de carractère précis#

from functions import *
import tkinter # importation du module permettant de creer la fenetre

window = tkinter.Tk() # création de la fenetre

# definition de quelques proprité de notre fenetre
window.geometry("820x580")
# empêche le redimentionnement de l'ecran
window.maxsize(width=820, height=580)
window.minsize(width=820, height=580)

window.title("Generateur de mot de Passe Version 1-1-1")
window.config(bg='#4065A4')
window.iconbitmap('img/generate-pass.ico')

# apel à l'acceuil
home(window)

window.mainloop()

window.quit()
