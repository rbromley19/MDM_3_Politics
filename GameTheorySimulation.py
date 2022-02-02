import random
import matplotlib.pyplot as plt

def GenerateRandomOpinions(numParties, numPlayers):
    listOfPlayersOpinions = []  # list of lists containing initial preference info
    for player in range(numPlayers):
        playerOpinions = [0] * numParties
        for party in range(numParties):
            playerOpinions[party] = round(random.uniform(-10, 10),2)  # opinions range from -10 to +10, to 2dp
        if all(i < 0 for i in playerOpinions): #if person only has negative opinions
            randomSwitch = random.randint(0, numParties-1)
            playerOpinions[randomSwitch] = -playerOpinions[randomSwitch]
        listOfPlayersOpinions.append(playerOpinions)
    return listOfPlayersOpinions


def PartyPopularities(
        listOfOpinions, numParties):  # input list of list of opinions. output list with the number of people who prefer each party
    partyPopularity = [0] * numParties
    for player in range(len(listOfOpinions)):
        opinions = listOfOpinions[player]
        maxpref = -11
        index = 0
        for party in range(numParties):
            if opinions[party] > maxpref:
                maxpref = opinions[party]
                index = party
        partyPopularity[index] += 1
    return partyPopularity

def GameTheoryODE(playersOpinions, partyPopularities): # returns a new list of party opinions
    listOfOpinions = playersOpinions
    #print(listOfOpinions)
    maxvotes = max(partyPopularities)
    alpha = 1
    beta = 1
    for party in range(len(partyPopularities)):
        if partyPopularities[party] == maxvotes:
            winningParty = party

    for player in range(len(playersOpinions)):
        opinions = playersOpinions[player]
        newOpinions = playersOpinions[player]
        if opinions[winningParty] == max(opinions): # If your prefered party is likely to win, you should always vote for them
            newOpinions = opinions
        elif opinions[winningParty] < 0: # use weighting of how much you hate that party
            for party in range(len(partyPopularities)):
                newOpinions[party] += (opinions[party] - opinions[winningParty]) * (partyPopularities[party]/len(playersOpinions)) * alpha
        else:
            for party in range(len(partyPopularities)):
                newOpinions[party] += opinions[party] * (partyPopularities[party]/len(playersOpinions)) * beta
        listOfOpinions[player] = newOpinions
    #print(listOfOpinions)
    return listOfOpinions



def run(numParties, numPlayers):
    listOfPartyPop = []
    opinions = GenerateRandomOpinions(numParties, numPlayers)
    partyPop = PartyPopularities(opinions, numParties)
    listOfPartyPop.append(partyPop)
    for i in range(26):
        opinions = GameTheoryODE(opinions, partyPop)
        partyPop = PartyPopularities(opinions, numParties)
        listOfPartyPop.append(partyPop)
    listOfParties = [1,2,3,4,5,6]
    for i in range(25):
        plt.bar(listOfParties, listOfPartyPop[i])
        plt.ylim(0,600)
        plt.title('Party Votes Changing with Tactical Voting')
        plt.xlabel('Parties')
        plt.ylabel('Number Of Votes')
        plt.savefig('Time = '+ str(i),bbox_inches='tight')
        plt.clf()

import cv2
import numpy as np
import glob
 
img_array = []
for filename in glob.glob('C:/Users/GFOAT/PycharmProjects/*.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

run(6,1000)
