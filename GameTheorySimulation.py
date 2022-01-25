import random


def GenerateRandomOpinions(numParties, numPlayers):
    listOfPlayersOpinions = []  # list of lists containing initial preference info
    for player in range(numPlayers):
        playerOpinions = [0] * numParties
        for party in range(numParties):
            playerOpinions[party] = random.randint(-10, 10)  # opinions range from -5 to +5
        listOfPlayersOpinions.append(playerOpinions)
    return listOfPlayersOpinions


def GenerateBiasedOpinions(numParties, numPlayers):
    # want there to be 1 party with ~40% popularity, and 2 smaller parties with ~25% popularity.
    # players who prefer party 2 or 3 are more in favour of the other one than party 1
    listOfPlayersOpinions = []
    for player in range(numPlayers):
        playerOpinions = [0] * numParties
        preference = random.randint(0, 20) # 0-7 = 1, 8-12 = 2, 13-17 = 3, 18-20 = other
        if 0 <= preference <= 7:
            preference = 0
        elif 8 <= preference <= 12:
            preference = 1
        elif 13 <= preference <= 17:
            preference = 2
        elif preference >= 18:
            preference = random.randint(3, numParties-1)
        for party in range(numParties):
            if party == preference:
                playerOpinions[party] = random.randint(6, 10)
            else:
                playerOpinions[party] = random.randint(-10, 4)
        if preference == 1:
            playerOpinions[2] = random.randint(4, 6)
        elif preference == 2:
            playerOpinions[1] = random.randint(4, 6)
        listOfPlayersOpinions.append(playerOpinions)
    return listOfPlayersOpinions

# players vote for the party with the largest OpinionScore x chance of winning/proportion of most liked


def CalculateInitialVotes(listOfPlayersOpinions, partyPopularity):
    for player in range(len(listOfPlayersOpinions)):
        opinions = listOfPlayersOpinions[player]
        for party in range(len(partyPopularity)):
            opinions[party] = opinions[party] * partyPopularity[party] / len(listOfPlayersOpinions)
        listOfPlayersOpinions[player] = opinions
    return listOfPlayersOpinions


def OutcomeSatisfactions(listOfOpinions, partyPopularities):
    # a players satisfaction of the election = Their Preference for the winning party + constant*prefenence for the party they voted for
    numberOfPeople = 0
    for party in range(len(partyPopularities)):
        if partyPopularities[party] > numberOfPeople:
            numberOfPeople = partyPopularities[party]
            mostPopularParty = party
    partyPop = [0]*len(partyPopularities)
    for player in range(len(listOfOpinions)):
        satisfaction = 0
        for party in range(len(partyPopularities)):
            if party == mostPopularParty:
                satisfaction += listOfOpinions[player][party]
            else:
                satisfaction -= listOfOpinions[player][party]
        voteSatisfaction = -10
        for party in range(len(partyPopularities)):
            if party == mostPopularParty:
                potentialSatisfaction = listOfOpinions[player][party]
            else:
                potentialSatisfaction = -listOfOpinions[player][party]
            if potentialSatisfaction > voteSatisfaction:
                preferedVote = party
                voteSatisfaction = potentialSatisfaction
        partyPop[preferedVote] += 1
    print(partyPop)
    return partyPop


def GameTheory(listOfOpinions, partyPopularity): 
    partyPop = [0]*len(partyPopularity)
    maxvotes = max(partyPopularity)
    for party in range(len(partyPopularity)):
        if partyPopularity[party] == maxvotes:
            winningParty = party

    for player in range(len(listOfOpinions)):
        opinions = listOfOpinions[player]
        if opinions[winningParty] < 0:
            numvotes = 0
            for party in range(len(partyPopularity)):
                if opinions[party] > 0:
                    if partyPopularity[party] > numvotes:
                        numvotes = partyPopularity[party]
                        mostlikedpositiveparty = party
            partyPop[mostlikedpositiveparty] += 1
        else:
            for party in range(len(partyPopularity)):
                opinions[party] = opinions[party] * partyPopularity[party] / len(listOfOpinions)
            maxpref = -1
            index = 0
            for party in range(len(partyPopularity)):
                if opinions[party] > maxpref:
                    maxpref = opinions[party]
                    index = party
            partyPop[index] += 1
    print("GT", partyPop)
    return partyPop


def PartyPopularities(
        listOfOpinions, numParties):  # input list of list of opinions. output list with the number of people who prefer each party
    partyPopularity = [0] * numParties
    for player in range(len(listOfOpinions)):
        opinions = listOfOpinions[player]
        maxpref = -1
        index = 0
        for party in range(numParties):
            if opinions[party] > maxpref:
                maxpref = opinions[party]
                index = party
        partyPopularity[index] += 1
    return partyPopularity


def RunSim(numParties, numPlayers):
    InitialOpinions = GenerateBiasedOpinions(numParties, numPlayers)
    InitialPopularity = PartyPopularities(InitialOpinions, numParties)
    print(InitialPopularity)
    NewOpinions, NewPopularity = InitialOpinions, InitialPopularity
    NewGT = NewPopularity
    for i in range(5):
        NewOpinions = CalculateInitialVotes(NewOpinions, NewPopularity)
        NewPopularity = PartyPopularities(NewOpinions, numParties)
        NewGT = GameTheory(InitialOpinions, NewGT)
        print("New Pop", NewPopularity)
    SecondOpinions = CalculateInitialVotes(InitialOpinions, InitialPopularity)
    SecondPopularity = PartyPopularities(SecondOpinions, numParties)
    print(SecondPopularity)
    #pop = OutcomeSatisfactions(SecondOpinions, SecondPopularity)


RunSim(4, 100)
