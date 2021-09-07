def startGame():
    import time, os
    valid = False
    while not valid:

        print("WELCOME TO TETRIS")

        #try:
            
        userStart = str(input("WHEN YOUR READY TO START, ENTER 'START' : "))
        if userStart.upper() == "START":
            valid = True
            import login
            username, highscore = login.login()
            import game
            game.play(username, highscore) 
        else:
            print(f"I GAVE YOU ONE INSTRUCTION, ENTER 'START' NOT '{userStart}' ")
            time.sleep(2)
            os.system("cls")
        #except SystemExit as SE:
            #pass
        #except:
        valid = False
        print("WELL SOMETHING JUST BROKE, TRY AGAIN AND IF THIS CONTINUES SPAM ME WITH ANGRY MESSAGES")
        print("THE GAME WILL NOW START AGAIN")
        time.sleep(4)
        os.system("cls")
