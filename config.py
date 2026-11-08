START_TIME_ = 1794096000 #Replace start time with date you would like to start!!!

OFFSET = 24*60*60*7
#1770336000
#1st oct 2026 1790812800
#1767312000
'''RUNS ONCE PER WEEK, EACH BATCH IS A DAY, 7 BATCHES
END_TIME_ = START_TIME_ - 24*60*60*4 #Add*7 to account for an entire weeks worth of data
TIME_STEP_ = 24*60*60
'''
#RUNS once every 2 min, each batch is 20s, 6 batches
END_TIME_ = START_TIME_ - OFFSET #Add*7 to account for an entire weeks worth of data
TIME_STEP_ = OFFSET//7

MAX_RETRIES_ = 10
ALL_MATCH_ = []
TIME_OUT_ = 99
_LOBBY_TYPE_ = 7
_GAME_MODE_ = 22