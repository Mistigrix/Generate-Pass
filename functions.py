from config import *
from constantes import *
import tkinter
from tkinter import messagebox
import random
import string
import time
from selenium import webdriver, common
from re import sub
from functools import partial


def bar(window):
    """Creer une bar de naviguation"""

    bar_menu = tkinter.Menu(window) # bar de naviguation

    # creation du premier menu qui est le champ de génération
    # celui ci sera déclancher immediatement sans passer par un sous menu
    bar_menu.add_cascade(label='Générateur', command=partial(home, window))


    # creation du second menu qui le menu du dictionnaire
    menu_dict = tkinter.Menu(bar_menu, tearoff=0)
    menu_dict.add_command(label='Listes', command=partial(afficheListes, window))
    menu_dict.add_command(label="Ajouter un mot", command=partial(interfaceAddWord, window))
    menu_dict.add_command(label='Supprimer un mot', command=partial(interfaceDelWord, window))
    bar_menu.add_cascade(label='Dictionnaire', menu=menu_dict)

    # un lien vers les paramètres
    bar_menu.add_cascade(label='Configurations', command=partial(interfaceConfig))

    # pour quitter le programme. Celui ci fonctionne comme le générateur
    bar_menu.add_cascade(label='Quitter', command=window.destroy)

    window.config(menu=bar_menu)


def home(window):

    # on clean d'abord l'ecran
    interfaceClean(window)

    # appel à la bar de naviguation
    bar(window)

    # Affichage du dernier mot de passe generer
    label_last_pass = tkinter.Label(window, text="Dernier mot de passe: " + selectLastPass(), bg='#4065A4',
                                    font=('Helvetica', 20), fg='white')
    label_last_pass.place(x=10, y=100)

    # creation de la frame
    frame = tkinter.Frame(bg='#4065A4')

    # creation des champs pour generer le mot de passe
    frame_password = tkinter.Frame(bg='#4065A4')

    # on creer le titre et on la place sur la frame creer
    label_title = tkinter.Label(window, text='Generateur de mot de passe', font=('Helvetica', 20), bg='#4065A4',
                                fg='white')
    label_title.pack(fill='x')

    label_space = tkinter.Label(frame, bg='#4065A4')
    label_space.pack()

    # on creer une entrée pour pourvoir afficher le mot de passe de tel sorte que l'utilasateur puissent la copier
    label_entry = tkinter.Entry(frame, bg='#4065A4', font=('Helvetica', 20), fg='black')
    label_entry.pack(fill='x')

    # creation du bouton de generation du mot de passe
    label_button = tkinter.Button(frame, text='Générer', bg='#4065A4', font=('Helvetica', 20), fg='white',
                                  command=partial(choicePass, label_entry))
    label_button.pack(fill='x')

    # creation du bouton de validation du mot de passe
    valid_button = tkinter.Button(frame, text='Valider', bg='#FF0000', font=('Helvetica', 20), fg='white',
                                  command=partial(valiPass, label_entry))
    valid_button.pack(fill='x')

    frame_password.pack()
    frame.pack(expand=True)  # on affiche la frame

# definition d'une methode pour nettoyé l'écran de la fenetre
def interfaceClean(window):
    """permet de supprimer tous ce qui a été creer à l'ecran"""
    for c in window.winfo_children():
        c.destroy()

def generateChars(min, max):
    """Fonction permetant de generer un mot de passe et renvoi le mot de passe"""
    password_min = min
    password_max = max

    diff = recupConfig()
    if diff['difficulty'] == EASY:
        print("La difficulter est: FACILE")
        # generation des carractères par boucle
        chars = "".join(random.choice(string.digits) for x in range(random.randint(password_min, password_max)))
    elif diff['difficulty'] == MOYEN:
        print("La difficulter est: MOYEN")
        # generation des carractères par boucle
        chars = "".join(random.choice(string.digits + string.punctuation) for x in range(random.randint(password_min, password_max)))
    elif diff['difficulty'] == HARD:
        print("La difficulter est: DIFFICILE")
        # generation des carractères par boucle
        password_min = 5
        password_max = 8
        chars = "".join(random.choice(string.digits + string.punctuation) for x in range(random.randint(password_min, password_max)))
    else:
        chars = ''
        print("Le niveau de difficulter est indeterminer")


    
    print(chars)
    print(password_min)
    print(password_max)
    return chars

def controlChrome(mypass):

    # insertion du path de l'exe pour controller chrome
    driver = webdriver.Chrome(executable_path='chromedriver.exe')

    # recuperation des listes de configuration
    config = recupConfig()

    # un dictionnaire contenan les configuration
    url = config['url']
    user = config['user']
    pass_config = config['password']

    try:
        # on entre le site à controler
        driver.get(url)
    except common.exceptions.InvalidArgumentException:
        # fermeture du naviguateur
        driver.close()
        displayMess("Votre addresse url n'est pas valide.\nVeillez la vérifier", 'Erreur Connexion')
        return 0

    except common.exceptions.WebDriverException:
        # fermeture du navigateur
        driver.close()
        displayMess("Vous n'êtes pas connecté au reseau", 'Erreur Connexion')
        return 0


    try:
        user_name = driver.find_element_by_id('username')
        password = driver.find_element_by_id('password')

    except common.exceptions.NoSuchElementException:
        driver.close()
        displayMess("Une erreur est survenue")
        return 0

    user_name.clear()
    user_name.send_keys(user)
    password.send_keys(pass_config)

    # Clic sur se connecter
    btn = driver.find_element_by_id('pop_login')

    btn.click()
    time.sleep(1)
    jscode2 ="console.log($('#label_wlan_basic_settings').click())"
    driver.execute_script(jscode2)
    time.sleep(2)

    #Change le password
    inputPass = driver.find_element_by_id('ssid_wpa_key')
    inputPass.clear()
    inputPass.send_keys(mypass)

    # validation du changement de password
    valid = driver.find_element_by_id('apply_button')
    valid.click()
    driver.close()

    # tout c'est bien passé on sauvegarde le mot de passe
    savePassword(mypass)


def choicePass(label_entry):
    """Choisi un mot de passe dans le dictionaire de mot de passe contenue dans le fichier all_passwords.txt"""
    dict_pass = open('all_passwords.txt', 'r')

    all_passwords = dict_pass.readlines()

    if len(all_passwords) == 0:
        displayMess("Le dictionnaire de mot est vide", 'Aucun Mot Trouvé')
        return 0

    # on choisit un mot au hasard dans la liste de mot
    word = all_passwords[random.randint(0, len(all_passwords)-1)]
    word = sub(r"[\n]*", "", word) # suppression du \n (entrée à la ligne)

    if len(word) >= 6:
        passwords_generate = word + generateChars(2, 2)
    else:
        ecart = 9 - len(word)
        passwords_generate = word + generateChars(ecart, ecart)

    label_entry.delete(0, tkinter.END)  # suppression de la chaine qui etait la deja
    label_entry.insert(0, passwords_generate)  # on insert le nouveau mot de passe generer

    dict_pass.close()

def savePassword(password):
    """Fonction permettant de sauvegarder le mot de passe generé dans le fichier password_generate.txt"""

    # si le mot de passe est vide on n'a rien à sauvegarder et l'ancien mot de passe reste le même
    if password == '':
        return 0

    # recuperation du contenue du fichier
    with open('config.config', 'rb') as file_pass:
        monpikle = pickle.Unpickler(file_pass)
        content = monpikle.load()

    # ajout ou modification de l'ancien mot de passe
    content['last_pass'] = password

    # ecriture du nouveau contenue
    with open('config.config', 'wb') as file_pass:
        monpikle = pickle.Pickler(file_pass)
        monpikle.dump(content)


def valiPass(label_entry):
    # recup du mdp
    password = label_entry.get()

    # change le mdp via le naviguateur chrome
    controlChrome(password)

def selectLastPass():
    """Cette fonction renvoi le dernier mot de passe generer par le programme en recuperant directement
        le password dans le fichier password_generate.txt"""

    try:
        with open('config.config', 'rb') as file:
            mon_unpickler = pickle.Unpickler(file)
            content = mon_unpickler.load()
    except FileNotFoundError:
        displayMess("Le fichier config.config n'a pas été rétrouvé", 'Non Retrouve')
        return ''
    except EOFError:
        return ''

    try:
        password = content['last_pass']
    except KeyError:
        password = ''

    return password

def interfaceAddWord(window):
    """Permet d'ajouter un mot à la liste de mot"""
    # nettoyage de l'ecran
    interfaceClean(window)

    # affiche la bar de naviguation
    bar(window)

    label_welcome = tkinter.Label(text="Ajouter des mots au dictionnaires",
                          font=('Helvetica', 20), bg='#4065A4', fg='white')
    label_welcome.pack()

    # champ pour entrer le mot à ajouter
    label_word = tkinter.Label(text='Entrer le mot:',
                               font=('Helvetica', 20), bg='#4065A4', fg='white')
    label_word.place(x=50, y=150)

    entry_word = tkinter.Entry(font=('Helvetica', 20), bg='#4065A4', fg='white')
    entry_word.place(x=250, y=150)

    button_word = tkinter.Button(text='Ajouter', font=('Helvetica', 20), bg='#4065A4', fg='white',
                                 command=partial(addWord, entry_word))
    button_word.place(x=450, y=200)

    # acces a la liste des mots
    button_list = tkinter.Button(text='Acceder a la liste',
                                 font=('Helvetica', 20), bg='#4065A4', fg='white',
                                 command=partial(afficheListes, window)
                                 )
    button_list.place(x=500, y=500)

def addWord(entry):
    """Ajoute un mot un dictionnaire"""

    file_dict = open('all_passwords.txt', 'a+')

    # recuperation du mot
    word = entry.get()

    # on verifie si c'est le premier mot à creer
    if len(file_dict.readlines()) == 0:
        # on ajoute une entrée au debut du mot pour passer à la ligne
        word = '\n' + word

    # ajout du mot dans le dictionnaire
    file_dict.write(word)

    #nettoyage du champ
    entry.delete(0, tkinter.END)

    file_dict.close()

def interfaceDelWord(window):
    """Permet de supprimer un mot à la liste de mot"""

    # nettoyage de l'ecran
    interfaceClean(window)

    # affiche la bar de naviguation
    bar(window)

    label_welcome = tkinter.Label(text="Supprimer des mots au dictionnaires",
                          font=('Helvetica', 20), bg='#4065A4', fg='white')
    label_welcome.pack()

    # champ pour entrer le mot à ajouter
    label_word = tkinter.Label(text='Entrer le mot:',
                               font=('Helvetica', 20), bg='#4065A4', fg='white')
    label_word.place(x=50, y=150)

    entry_word = tkinter.Entry(font=('Helvetica', 20), bg='#4065A4', fg='white')
    entry_word.place(x=250, y=150)

    button_word = tkinter.Button(text='Supprimer', font=('Helvetica', 20), bg='#4065A4', fg='white',
                                 command=partial(delWord, entry_word))
    button_word.place(x=450, y=200)

    # acces a la liste des mots
    button_list = tkinter.Button(text='Acceder a la liste',
                                 font=('Helvetica', 20), bg='#4065A4', fg='white',
                                 command=partial(afficheListes, window)
                                 )
    button_list.place(x=500, y=500)

def delWord(entry_word):
    """Supprime le mot entré dans le dictionnaire"""

    # on ouvre d'abord le fichier en mode lecture

    try:
        file_dict = open('all_passwords.txt', 'r+')
        all_words = file_dict.readlines()
        file_dict.close()  # fermeture du fichier
    except FileNotFoundError:
        displayMess("Le fichier all_passwords.txt n'a pas été rétrouvé.")
        all_words = []
        return 0


    word = entry_word.get()

    try:
        all_words[-1] += '\n'
        index_word = all_words.index(word + '\n')
    except IndexError:
        displayMess("Le mot n'a pas été rétrouver", 'Non Retrouver')
        return 0
    except ValueError:
        displayMess("Le mot n'a pas été rétrouver", 'Non Retrouver')
        return 0

    # verifie si ce n'est pas le dernier mot de liste qu'il veut supprimer
    if index_word != len(all_words)-1:
        word += '\n'
        all_words.remove(word)
    else:
        word += '\n'
        all_words.remove(word)
        #enlever le saut de ligne au nouveau de fin
        last_word = sub(r"[\n]*", "", all_words[-1])
        del all_words[len(all_words)-1]
        all_words.insert(len(all_words), last_word)

    # reouverture du fichier mais en mode ecriture pour pouvoir supprimer tous les mots et les réecrire
    file_dict = open('all_passwords.txt', 'w')

    #suppression du saut de ligne pour le dernier mot
    all_words[-1] = sub(r"[\n]*", "", all_words[-1])

    # convertir la liste en chaine de carractere
    all_words_str = ''.join(all_words)

    file_dict.write(all_words_str)

    file_dict.close()

    entry_word.delete(0, tkinter.END)


def afficheListes(window, start=0, running=True):
    """Affiche tous les mots presents dans le dictionnaire"""

    interfaceClean(window)

    bar(window)

    try:
        file_dict = open('all_passwords.txt', 'r')
        words = file_dict.readlines()
        file_dict.close()
    except FileNotFoundError:
        displayMess("Le fichier all_passwords.txt n'a pas été rétrouvé")
        # retour d'un dictionnaire vide
        words = []

    if len(words) <= 0:
        nbr_words = 0
    else:
        nbr_words = len(words)-1

    # on affiche le nombre de mot
    tkinter.Label(text='Nombre de mot: '+str(nbr_words), font=('Helvetica', 15), bg='#4065A4',
                                fg='white').pack()

    x=10
    y=50
    nbr_words_dis = 0

    if len(words) == 0:
        running = False

    # on affiche que 100 mots
    stop = start+100
    while running:
            tkinter.Label(window, text=words[start], font=('Helvetica', 15), bg='#4065A4',
                          fg='white').place(x=x, y=y)
            start += 1
            y += 30

            # si les mots ont atteint le bord de la fenetre on contunu à coté
            if y >= 550:
                x += 125
                y = 50

            if start == stop or start == len(words):
                running = False


    # un boutton pour passer à la page suivant
    if start != len(words):
        tkinter.Button(window, text='SUIVANT', font=('Helvetica', 15), bg='#4065A4',
                            fg='white', command=partial(afficheListes, window, start)).place(x=660, y=515)

    #tkinter.Button(window, text='Retour au Debut', font=('Helvetica', 15), bg='#4065A4', fg='white', command=partial(afficheListes, window)).place(x=600, y=515)


def displayMess(mess, title='ERREUR'):
    """Affiche un message"""

    box = tkinter.messagebox.Message()

    box.show(message=mess, title=title)
