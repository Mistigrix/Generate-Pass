"""Ce fichier contient l'interface graphique et toute les fonctions permettant de configurer le proramme"""
from functions import *
from constantes import *
import tkinter
import pickle
from functools import partial


def interfaceConfig():
    """Creer une nouvelle fenetre pour configurer le programme"""

    window_config = tkinter.Tk()
    window_config.geometry('400x400')
    window_config.maxsize(width=400, height=400)
    window_config.minsize(width=400, height=400)
    window_config.title('Configuration')
    window_config.iconbitmap('img/config.ico')

    label_config = tkinter.Label(window_config, text='Bienvenue aux paramètres')
    label_config.pack()

    # creation du champ de l'addresse url
    label_url = tkinter.Label(window_config, text='Addresse URL:')
    label_url.place(x=10, y=50)

    entry_url = tkinter.Entry(window_config, font=('Helvetica', 10), width=30)
    entry_url.place(x=100, y=50)

    # creation du champ pour entrer le nom de l'utilisateur
    label_user = tkinter.Label(window_config, text='Nom utilisateur:')
    label_user.place(x=10, y=100)

    entry_user = tkinter.Entry(window_config, font=('Helvetica', 10), width=30)
    entry_user.place(x=100, y=100)

    # creation du champ pour entrer le mot de passe de l'utilisateur
    label_pass = tkinter.Label(window_config, text='Mot de passe:')
    label_pass.place(x=10, y=150)

    entry_pass = tkinter.Entry(window_config, font=('Helvetica', 10), width=30)
    entry_pass.place(x=100, y=150)

    # choix de la difficulter

    diff = tkinter.StringVar()

    label_diff = tkinter.Label(window_config, text='Niveau de difficulter du mot de passe')
    label_diff.place(x=50, y=200)

    # difficulter facile
    radio_diff_easy = tkinter.Radiobutton(window_config, text='Facile', value=EASY, variable=diff)
    radio_diff_easy.place(x=75, y=225)

    # difficulter moyenne
    radio_diff_moyen = tkinter.Radiobutton(window_config, text='Moyenne', value=MOYEN, variable=diff)
    radio_diff_moyen.place(x=75, y=250)

    # difficulter difficile
    radio_diff_hard = tkinter.Radiobutton(window_config, text='Difficile', value=HARD, variable=diff)
    radio_diff_hard.place(x=75, y=275)


    # on remplir les champs des dernieres modification si elle existe
    config = recupConfig()
    if len(config) != 0:
        entry_url.insert(0, config['url'])
        entry_user.insert(0, config['user'])
        entry_pass.insert(0, config['password'])

    # creer un bouton pour annuler
    button_cancel = tkinter.Button(window_config, text='Annuler', font=('Helvetica', 10),
                                   command=window_config.destroy)
    button_cancel.place(x=200, y=300)

    button_vailde = tkinter.Button(window_config, text='Valider', font=('Helvetica', 10), command=partial(saveConfig, window_config, entry_url, entry_user, entry_pass, diff))
    button_vailde.place(x=300, y=300)

    window_config.mainloop()
    window_config.quit()


def saveConfig(window_config, entry_url, entry_user, entry_pass, difficulty=HARD):
    """Recupere et sauvegarde les configuration faites dans les paramètres"""

    url = entry_url.get()
    user = entry_user.get()
    password = entry_pass.get()
    diff = difficulty.get()

    print('text:'.diff)

    # creer une liste contenant les configuration
    config = {}
    config['url'] = url
    config['user'] = user
    config['password'] = password
    config['difficulty'] = diff

    # ouverture du fichier config en mode ecriture
    with open('config.config', 'wb') as file_config:
        mon_pickle = pickle.Pickler(file_config)
        mon_pickle.dump(config)

    # on ferme la fenetre de parametre
    window_config.destroy()

def recupConfig():
    """Recuperer les configuration dans le fichier config"""

    # ouverture du fichier en mode lecture binaire
    try:
        with open('config.config', 'rb') as file_config:
            mon_unpickle = pickle.Unpickler(file_config)
            try:
                config = mon_unpickle.load()
            except MemoryError:
                print("Une erreur est survenue")
            except EOFError:
                # le fichier est vide alors on renvoi un dictionnaire vide
                return {}
    except FileNotFoundError:
        return {}

    # retour du dictionnaire qu'il y est du contenue ou pas
    return config

def create_file(file):
    """Creer le fichier au nom entrer en parametre"""

    file_create = open(file, 'a')

    return file_create
