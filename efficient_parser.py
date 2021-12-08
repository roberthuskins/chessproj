from pgn_parser import pgn, parser
from pgn_parser.pgn import Actions
import chess.pgn as pgnP
import re
import io
import numpy as np

FILE_NAME = "rated_2021.pgn"
# "rated_2021.pgn"

language = set([])
rejected_pgns = 0
translator_dictionary = {"0":0}
translator_ind = 1

csv_out = open("NEW_formatted_chess_50thousand.csv", 'a', encoding='utf-8')
csv_out.write("average_elo,encoded_pgn\n")
gameno = 0
elo_target = []
# Each game block is 17 lines long
# meanning we can just take get the
# info starting from a certain line, 
# and do the same for all of the others.
white_elo = -1
black_elo = -1
valid_pgn = False
correct_size = True

    
with open(FILE_NAME) as file:  
    
    for line in file:
        if gameno >= 50000: break
        try:
            if (line.startswith("[WhiteElo")):
                white_elo = int(line[11:-3])
                continue
            if (line.startswith("[BlackElo")):
                black_elo = int(line[11:-3])
                continue
            
            if (line.startswith("1. ") and (white_elo != -1 and black_elo != -1)):
                # print(game)
                game = line
                game = re.sub("[\{}].*?[\}]", "", game)
                game = re.sub("[\()}].*?[\)]", "", game)
                game = re.sub(" \d+\.\.\.", "", game).replace("  "," ")
                game = re.split("\d+\.", game)

                correct_size = True
                out = []
                
                for move in game[1:]:
                    try:
                        white, black = move.strip().split()
                        if (white not in language):
                            language.add(white)
                            translator_dictionary[white] = translator_ind
                            translator_ind += 1
                    
                        if (black not in language):
                            language.add(black)
                            translator_dictionary[black] = translator_ind
                            translator_ind += 1
                        
                        out.append(str(translator_dictionary[white]))
                        out.append(str(translator_dictionary[black]))
                        
                    except ValueError:
                        white, black, end = move.strip().split() 
                        if (white not in language):
                            language.add(white)
                            translator_dictionary[white] = translator_ind
                            translator_ind += 1
                        
                        if (black not in language):
                            language.add(black)
                            translator_dictionary[black] = translator_ind
                            translator_ind += 1
                            
                        if (end not in language):
                            language.add(end)
                            translator_dictionary[end] = translator_ind
                            translator_ind += 1
                        
                        out.append(str(translator_dictionary[white]))
                        out.append(str(translator_dictionary[black]))
                        out.append(str(translator_dictionary[end]))
                
                length = len(out)
                
                if(length > 120):
                    correct_size = False
                else:
                    for i in range(120 - length):
                        out.append("0")
                
                formatted_pgn = " ".join(out)    
                # DONE GETTING GAME MOVES

                if(correct_size):
                    average_elo = (white_elo + black_elo)/2
                    csv_out.write("{},{}\n".format(average_elo, formatted_pgn))
                    
                gameno+=1
                if (gameno % 1000 == 0):
                    print("Current Game Being Formatted: {}".format(gameno))
                    print("Average Elo: {}".format(average_elo))
                    print("Rejected: {}".format(rejected_pgns))
                    
                # DONE PROCESSING GAME RESET VARS
                white_elo = -1
                black_elo = -1
                valid_pgn = False
                correct_size = True
            
        except ValueError as ve:
            #sometimes the elos have questionmarks when the player is new or something
            # print(line)
            # print("Value:", ve)
            rejected_pgns += 1
        except SyntaxError as se:
            #when the regex doesn't work for the add_words thing it raises a ParseError. will look into this later
            # print(line)
            # print("SYNTAX:", se)
            rejected_pgns += 1
        except IndexError as e:
            print("DONE WITH DATA")
            break

print("Rejected PGNS: {}".format(rejected_pgns))
print("Total Games processed: {}".format(gameno))

print(csv_out)
csv_out.close()

f = open("NEW_language_50thousand.txt", "w")
f.write(str(translator_dictionary))
f.close()







'''
def translate(pgn):
    out = []
    movetext = parser.parse(pgn, actions=Actions()).movetext
    
    for move in movetext:
        if (move.white.san not in language):
            language.add(move.white.san)
            translator_dictionary[move.white.san] = translator_ind
            translator_ind += 1
        
        if (move.black.san not in language):
            language.add(move.black.san)
            translator_dictionary[move.black.san] = translator_ind
            translator_ind += 1
        
        out.append(translator_dictionary[move.white.san])
        out.append(translator_dictionary[move.black.san])
    
    length = len(out)
    
    if(length > 120):
        return False, ""
    
    if(length < 120):
        for i in range(120-length):
            out.append("0")
    
    out = np.array(out)
    return True, " ".join(np.array(out))
'''

