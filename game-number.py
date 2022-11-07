import os
import json
import random
import shutil
from tkinter import *
from tkinter import messagebox

#   easy = reloadData("dif complete", "easy")
#   meduim = reloadData("dif complete", "medium")
#   hard = data["dif complete"]["hard"]
#   extrem = data["dif complete"]["extrem"]

#   firstTry = data["success"]["firstTry"]
#   allDiffcultyWin = data["success"]["allDiffcultyWin"]

jsonPath = os.path.dirname(os.path.abspath(__file__)) # Trouve l'emplacement du fichier data.json sur la machine (en "path absolue" éviter celui du workspace de l'IDE)

def reloadData(path1, path2)->bool: # fontion permettant de garder les données ç jour dans le programme
    with open(f"{jsonPath}\data.json", "r") as x: # Ouvre le fichier en "read" pour lire les données
        global data
        data = json.load(x)

        return data[str(path1)][str(path2)]

nbOfTry = 1
mainFont = ("Orbitron", 10) # police principale de l'application

def difficultyChoice(dif)->int:
    global difChoice
    difChoice = dif
    print(f"Diffculté: {dif}")

    global dataWording
    if difChoice == 1:
        dataWording = str("easy")
    elif difChoice == 2:
        dataWording = str("medium")
    elif difChoice == 3:
        dataWording = str("hard")
    elif difChoice == 4:
        if reloadData("dif complete", "easy") == True and reloadData("dif complete", "medium") == True and reloadData("dif complete", "hard") == True:
            dataWording = str("extrem")
            difWindow.destroy()
            gameNumber()
        else:
            messagebox.showerror(title="Difficulté non débloqué", message="Tu n'as pas encore terminer toutes les difficultés!\n(Easy, Medium, Hard)")
            difWindow.destroy()
            difficulty()

def difficulty():

    global difWindow
    difWindow = Tk()
    difWindow.geometry("435x200")
    difWindow.title("Sélection de la difficulté")

    global allDiffcultyWinCheck
    allDiffcultyWinCheck = 0

    easy = reloadData("dif complete", "easy")
    medium = reloadData("dif complete", "medium")
    hard = reloadData("dif complete", "hard")
    extrem = reloadData("dif complete", "extrem")

    # Widgets
    difficultyLabel = Label(difWindow, text="Difficulté:", font=mainFont)
    easyButton = Button(difWindow, text=f"Facile {difficultyCheck(easy)}", fg="green", font=mainFont, command=lambda: [difficultyChoice(1), difWindow.destroy(), gameNumber()])
    casualButton = Button(difWindow, text=f"Moyen {difficultyCheck(medium)}", fg="orange", font=mainFont, command=lambda: [difficultyChoice(2), difWindow.destroy(), gameNumber()])
    hardButton = Button(difWindow, text=f"Difficile {difficultyCheck(hard)}", fg="red", font=mainFont, command=lambda: [difficultyChoice(3), difWindow.destroy(), gameNumber()])
    extremButton = Button(difWindow, text=f"Extrème {difficultyCheck(extrem)}", fg="black", font=mainFont, command=lambda: difficultyChoice(4))

    mainMenu = Button(difWindow, text="Menu Principal", font=mainFont, fg="#0FA98D" , command=lambda: [difWindow.destroy(), main()])

    difficultyLabel.grid(row=0, column=1, pady=5)
    easyButton.grid(row=1, column=0, pady=20, padx=30)
    casualButton.grid(row=1, column=1, pady=20, padx=30)
    hardButton.grid(row=1, column=2, pady=20, padx=30)
    extremButton.grid(row=2, column=1, pady=20)

    mainMenu.place(x=3, y=170)

    difWindow.resizable(False, False)
    difWindow.mainloop()

def difficultyCheck(difficulty):
    if difficulty == True:
        emojiWording = str("✅")
    elif difficulty == False:
        emojiWording = str("❌")
    
    print(f"Difficulté: {emojiWording}")
    return emojiWording

def gameTry():
    print("gameTry - START")
    global nbOfTry

    try:
        tryNumber = int(tryEntry.get())

        if tryNumber == nbToFind:
            print(f"WIN - {difWording}")

            hintLabel.config(text=f"GAGNÉ - {nbOfTry} essaie(s)", fg=("#A09918"))
            tryEntry.config(state="disabled")
            tryButton.config(text="Recommencer", font=mainFont, fg="#B20E74", command=lambda: [game.destroy(), gameNumber()])

            if nbOfTry <= 1 and reloadData("success", "firstTry") == False:
                data["success"]["firstTry"] = True # change les donnés du succcès sur le programme
                messagebox.showinfo(title="DU PREMIER COUP", message="Bravo tu as réussi à gagner en seulement 1 seul essaie!", icon="info")

            data["dif complete"][dataWording] = True
            with open(f"{jsonPath}\data.json", "w") as x:
                json.dump(data, x, indent=4)
        

            if reloadData("dif complete", "easy") and reloadData("dif complete", "medium") and reloadData("dif complete", "hard") and reloadData("dif complete", "extrem") and reloadData("success", "allDiffcultyWin") == False:
                data["success"]["allDiffcultyWin"] = True
                messagebox.showinfo(title="J'ADORE CE JEUX", message="Bravo tu as réussi à terminer toutes les difficultés du jeu, merci! ;)", icon="info")

                with open(f"{jsonPath}\data.json", "w") as x: # écrit les donnés sur le fichier data.json
                    json.dump(data, x, indent=4)

        else:
            
            if tryNumber > nbToFind:
                print(f"LESS for find - {difWording}")
                hintWording = "PLUS PETIT"
                hintColor = "#0B9A25"
                nbOfTry = nbOfTry + 1 # (nbOfTry =+ 1 non-fonctionel)

            elif tryNumber < nbToFind:
                print(f"MORE for find - {difWording}")
                hintWording = "PLUS GRAND"
                hintColor = "#F02F09"
                nbOfTry = nbOfTry + 1
        
            print(f"ESSAIE: {nbOfTry}")
            tryButton.config(text=f"Essaie n°{nbOfTry}")
            hintLabel.config(text=hintWording, fg=hintColor)

    except ValueError: # si une erreur de valeur apparait
        print("VALLUE ERROR")
        hintLabel.config(text="ENTRER UN NOMBRE VALIDE", fg=("#C10D0D"))
        tryEntry.delete(0, END)

    print("gameTry - END")

def gameNumber():

    global difWording, difNumber
    if difChoice == 1:
        difWording = str("Easy")
        difNumber = int(25)
    elif difChoice == 2:
        difWording = str("Medium")
        difNumber = int(100)
    elif difChoice == 3:
        difWording = str("Hard")
        difNumber = int(500)
    elif difChoice == 4:
        difWording = str("Extrem")
        difNumber = int(1500)
    global nbToFind, nbOfTry
    nbToFind = int(random.randint(0,difNumber))
    print(f"Number To Find: {nbToFind}")
    nbOfTry = 1

    global game
    game = Tk()
    game.geometry("400x225")
    game.title(f"{difWording} / Jeux - Projet Octobre 2022 - NSI")

    #Widgets
    label1 = Label(game, text=f"Le nombre à trouver est entre 0 et {difNumber}:", font=mainFont)
    tryLabel = Label(game, text="Entrer un nombre:", font=mainFont)
    global tryEntry, tryButton, hintLabel
    tryEntry = Entry(game)
    tryButton = Button(game, text=f"Essaie n°{nbOfTry}", command=gameTry, font=mainFont)
    hintLabel = Label(game, text="", font=("Orbitron", 15))
    mainMenu = Button(game, text="Menu Principal", font=mainFont, fg="#0FA98D", command=lambda: [game.destroy(), main()])
    leaveButton = Button(game, text="Quitter", font=mainFont, fg="#A90F0F", command=exit)

    label1.pack()

    tryLabel.pack(pady=(20, 0))
    tryEntry.pack()
    tryButton.pack(pady=7)
    hintLabel.pack(pady=10)

    mainMenu.place(x=3, y=195)
    leaveButton.place(x=330, y=195)

    game.resizable(False, False)
    game.mainloop()
    
def successCheck(sucess)->float:

    if sucess == True:
        wording = str("RÉUSSIE")
        color = str("green")
    elif sucess == False:
        wording = str("ÉCHEC")
        color = str("red")

    return wording, color

def successMenu():

    successWindow = Tk()
    successWindow.title("Succès")

    firstTryLabel = Label(successWindow, text="- Du Premier Coup! (gagner en un seul essai):", font=mainFont)
    wording, wordingColor = successCheck(reloadData("success", "firstTry")) # garder l'affichage des donnés à jour sur lke programme
    firstTryLabelCheck = Label(successWindow, text=wording, fg=wordingColor, font=mainFont)

    allDiffcultyWinLabel = Label(successWindow, text="- J'adore ce Jeux! (gagner sur toute les difficultés):", font=mainFont)
    wording, wordingColor = successCheck(reloadData("success", "allDiffcultyWin"))
    allDiffcultyWinCheck = Label(successWindow, text=wording, fg=wordingColor, font=mainFont)

    firstTryLabel.grid(row=0, column=0, sticky="w", pady=15)
    firstTryLabelCheck.grid(row=0, column=1, sticky="w", padx=12, pady=15)

    allDiffcultyWinLabel.grid(row=1, column=0, sticky="w", pady=15)
    allDiffcultyWinCheck.grid(row=1, column=1, sticky="w", padx=12, pady=15)

    successWindow.resizable(False, False)
    successWindow.mainloop()

def getSucessNumber():
    with open(f"{jsonPath}\data.json", "r") as x: #Ouvre le fichier en "read" pour lire les données
        successDataJson = json.load(x)

    successData = str(successDataJson["success"])
    print(f"sucessData = {successData}")
    successNumber = successData.count("True")

    print(f"SUCCESS NOMBER: {successNumber}")
    return successNumber

def resetProgression():
    resetMessaegBox = messagebox.askquestion(title="Réinitialiser", message="Voulez vous vraiment réinitialiser vos données?", icon="warning")

    if resetMessaegBox == "yes":
        path = os.path.dirname(os.path.abspath(__file__))
        src = (f"{path}\data-restore.json")
        dest = (f"{path}\data.json")

        shutil.copyfile(src, dest) # copie le fichier source dans le fichier destination (écrase les donnés de l'ancien)
        print("DATA RESET")

        successButton.config(text=f"🏆 - succès {getSucessNumber()}/2") # garde l'afficgae à jour
        messagebox.showinfo(title="Réinitialiser", message="Vos données ont été correctement réinitialiser.", icon="info")

def main():
    print("Acess to main function")

    main = Tk()
    main.geometry("400x225")
    main.title("Menu Principal - Projet Octobre 2022 - NSI")


    # Widgets
    titleLabel = Label(main, text="Number Games", font=("Orbitron", 20)) 
    playButton = Button(main, text="PLAY", command=lambda: [main.destroy(), difficulty()], font=("Orbitron", 25), fg="red")
    resetButton = Button(main, text="Réinitialiser Progression", font=("Orbitron", 8), fg="purple", command=resetProgression)
    global successButton
    successButton = Button(main, text=f"🏆 - succès {getSucessNumber()}/2", command=lambda: successMenu(), font=mainFont, fg="#A09918")
    leaveButton = Button(main, text="Quitter", font=mainFont, fg="#A90F0F", command=exit)

    # Dsiplay Widgets
    titleLabel.pack(pady=5)
    playButton.pack(pady=10)
    resetButton.pack()
    successButton.place(x=3, y=195)

    leaveButton.place(x=330, y=195)

    main.resizable(False, False)
    main.mainloop()

def verifyRegister():
    with open(f"{jsonPath}\data.json", "r") as x:
        registerDataJson = json.load(x)

    newUsername = str(newUserEntry.get())
    newPassword = str(newPasswordEntry.get())
    newPasswordCheck = str(newPasswordCheckEntry.get())
    print(f"New Username: {newUsername}\nNew Password: {newPassword}")

    if newPassword == newPasswordCheck and newUsername != newPassword:
        print("newPassword == newPasswordCheck")
        
        print(registerDataJson["users"])
        registerDataJson["users"].update({newUsername: {"username": newUsername,"password": newPassword}}) # update: dictionnary / append: list (4 heures pour comprendre...)

        with open(f"{jsonPath}\data.json", "w") as x:
            json.dump(registerDataJson, x, indent=4) # écrit les données

        messagebox.showinfo(title="Utilisateur Crée", message=f"Le nouvel utilisateur à bien été crée sous le nom de:\n«{newUsername}»")
        registerWindow.destroy()
        login()

    elif newPassword != newPasswordCheck:
        print("newPassword != newPasswordCheckEntry")
        messagebox.showerror(title="Erreur", message=f"Les deux mots de passe sont différents!\nPremier mot de passe: {newPassword}\nSecond mot de passe {newPasswordCheck}", icon="error")
    
    elif newUsername == newPassword:
        print("newUsername == newPassword")
        messagebox.showerror(title="Erreur", message=f"Le nom d'utilisateur et le mot de passe sont les mêmes!\nNom d'utilisateur: {newUsername}\nMot de passe: {newPassword}", icon="error")

def register():
    global registerWindow
    registerWindow = Tk()
    registerWindow.title("Register")

    global newUserEntry, newPasswordEntry, newPasswordCheckEntry, registerInfoLabel
    newUser = Label(registerWindow, text="Nom d'utilisateur:")
    newUserEntry = Entry(registerWindow) # USERNAME = user
    newPassword = Label(registerWindow, text="Mot de passe:")
    newPasswordEntry = Entry(registerWindow, show="*") # pasword = NSI@102022
    newPasswordCheck = Label(registerWindow,text="Mot de passe:")
    newPasswordCheckEntry = Entry(registerWindow, show="*")
    confirmationButton = Button(registerWindow, text="Register", command=verifyRegister)
    registerInfoLabel = Label(registerWindow, text="", fg="red")

    newUser.grid(row=0, column=0, sticky="w")
    newUserEntry.grid(row=0, column=1)

    newPassword.grid(row=1, column=0, sticky="w")
    newPasswordEntry.grid(row=1, column=1)
    newPasswordCheck.grid(row=2, column=0, sticky="w")
    newPasswordCheckEntry.grid(row=2, column=1)

    registerInfoLabel.grid(row=3, column=0)
    confirmationButton.grid(row=3, column=1, pady=3)

    registerWindow.resizable(False, False)
    registerWindow.mainloop()


def verifyLogin():

    with open(f"{jsonPath}\data.json", "r") as x:
        loginDataJson = json.load(x)
    
    userList = list(loginDataJson["users"])
    print(f"userList = {userList}")
    user = userEntry.get()
    userExist = userList.count(user)

    if userExist == 1:
        print(f"user = {user}")
        loginInfoLabel.config(text="")

        password = passwordEntry.get()

        if password == loginDataJson["users"][user]["password"]:
            loginInfoLabel.config(text="")
            print("Login Successful")
            loginWindow.destroy()
            main()
        elif password != loginDataJson["users"][user]["password"]:
            print(f"WRONG PASSWORD ({password})")
            messagebox.showerror(title="Erreur", message=f"Le mot de passe ne correspond pas avec l'utilisateur\nNom d'utilisateur: {user}\nMot de passe: {password}", icon="error")

    elif userExist <= 0:
        print(f"WRONG USER ({user})")
        messagebox.showerror(title="Erreur", message=f"L'utilisateur n'existe pas\nNom d'utilisateur entré: {user}", icon="error")

def login():

    global loginWindow
    loginWindow = Tk()
    loginWindow.title("Login")

    global userEntry, passwordEntry, loginInfoLabel
    user = Label(loginWindow, text="Nom d'utilisateur:")
    userEntry = Entry(loginWindow)
    password = Label(loginWindow, text="Mot de passe:")
    passwordEntry = Entry(loginWindow, show="*") 
    loginButton = Button(loginWindow, text="Login", command=verifyLogin)
    loginInfoLabel = Label(loginWindow, text="")

    registerButton = Button(loginWindow, text="Register", command=lambda: [loginWindow.destroy(), register()])

    user.grid(row=0, column=0, sticky="w")
    userEntry.grid(row=0, column=1)

    password.grid(row=1, column=0, sticky="w")
    passwordEntry.grid(row=1, column=1)

    loginButton.grid(row=2, column=1, pady=3)
    loginInfoLabel.grid(row=2, column=0)

    registerButton.grid(row=3, column=1, pady=3)

    loginWindow.resizable(False, False)
    loginWindow.mainloop()

login()