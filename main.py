from game_logic import*

while True:    #MAIN GAME LOOP
    for event in pygame.event.get(): #PROCESSES EACH EVENT IN THE QUEUE
        if event.type == pygame.QUIT: #CHECKS WHETHER QUIT EVENT HAS BEEN TRIGGERED AND QUITS THE GAME IF TRUE
            pygame.quit()
            sys.exit()
        if GAME_STATE == 'MENU':	#IF GAME STATE IS MENU, CALLS THE GAME_STATE_MENU FUNCTION
            GAME_STATE = game_state_menu(GAME_STATE, event)
        elif GAME_STATE == 'RUNNING':	#IF GAME STATE IS RUNNING, HANDLES THE GAMEPLAYLOGIC
            GAME_STATE = game_state_running(GAME_STATE, event)
        elif GAME_STATE == 'LEADERBOARD':	#IF GAME STATE IS LEADERBOARD, DRAWS THE LEADERBOARD
            GAME_STATE =game_state_leaderboard(GAME_STATE, event)
        elif GAME_STATE == 'GAME OVER':		#IF GAME STATE IS GAME OVER, HANDLES THE GAME OVER LOGIC
            GAME_STATE = game_state_gameover(GAME_STATE, event)
        elif GAME_STATE == 'POST GAME':		#IF GAME STATE IS POST GAME, HANDLES POSTGAME LOGIC WHICH ISSAVING SCORE AND PROMPTING USERNAME INPUT
            GAME_STATE = game_state_postgame(GAME_STATE, event)

