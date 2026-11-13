import argparse
import random
import asciibars

def joinlist(list):
    result = ""
    for l in range(len(list)):
        result += (str(list[l])+" ")
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ndice",
                        help="How many of which dice to roll in the form 'NdM', or 'NdM,NdM,...,NdM' for multiple dice types")
    parser.add_argument("-adv", "--advantage",
                        dest="adv",
                        help="Optional argument specifying how many advantage dice to roll (Use [-] for disadvantage) \n Does not work with multiple dice types.")
    parser.add_argument('-s', '--sum',
                    dest="sum",
                    help="Whether or not to show the sum of all dice - Advantage considered",
                    action='store_true')
    parser.add_argument('-m','--mod',
                    dest="modifier",
                    help="Die modifier, if [sum] is used, will add to the sum total instead")
    parser.add_argument('-g',"--graph",
                        dest="graph",
                        help="Enable the creation of an ascii bar graph depicting results.",
                        action='store_true')
    parser.add_argument('-a',"--average",
                        dest="average",
                        help="Show the average score of all rows.",
                        action='store_true')
    parser.add_argument('-hide',
                        dest="hide",
                        help="Hide results of individual rolls (returns nothing with no other args).",
                        action='store_true')
    args = parser.parse_args()
    #setting up argparser for cmd input

    #beginning arg reading
    ndice = args.ndice
    if (ndice.find('d')) == -1:
        raise SyntaxError("Please enter dice type in form 'NdM' (N>=0, M>=1)")
        #error when no NdM found
    if (ndice.find(',')) != -1:
        args.adv = None
        ndice = ndice.replace(',','d')
    ndice = ndice.split("d")
    #converting NdM to a dice type and number

    if (ndice[len(ndice)-1]) == '':
        raise SyntaxError("Missing dice after delimiter (,)")

    for x in range(len(ndice)):
        if ndice[x] == "":
           print("No N found, default: 1")
           ndice[x] = 1
           #default 1 when no N found
        else:
            ndice[x] = int(ndice[x])
    #converting the args to Ints

    #optional arguments
    if args.adv is not None:
        advantage = int(args.adv)
    else:
        advantage = 0
    #checking for advantage

    if args.modifier is not None:
        modifier = int(args.modifier)
    else:
        modifier = 0
    #checking for modifiers

    sum = args.sum
    #checking for the sum tag (true/false)

    average = args.average
    #checking for average tag (true/false)

    graph = args.graph
    #checking for the graph tag (true/false)

    hide = args.hide
    #checking for the hide tag (true/false)
    
    #beginning of output
    rolls = []
    totalDice = 0
    for x in (range(0,int(len(ndice)),2)):
        while len(rolls) < totalDice + ndice[x] + abs(advantage):
            rolls.append(random.randint(1,ndice[x+1]))    
        totalDice += ndice[x]    
    #rolling
    

    if not hide:
        print("Rolls: " + joinlist(rolls))
    #print out roll results

    if ndice[1] == 2:
        coinflip = ["n/a","Heads","Tails"]
        coinresults = []
        for r in range(len(rolls)):
            coinresults.append(coinflip[rolls[r]])
        print("Coin Flips: " + joinlist(coinresults))
    #if the dice type is d2, print coin flip too
        

    modifiedrolls = []
    if modifier != 0 and not sum:
        for r in range(len(rolls)):
            modifiedrolls.append(rolls[r]+modifier)       
        print("Modified Rolls: "+ joinlist(modifiedrolls))   
    #if there is a modifier and [sum] is false, output modified individual rolls         

    rolls.sort(reverse=True)
    if advantage != 0:
        if advantage > 0 : advantageresults = rolls[:-advantage]
        if advantage < 0 : advantageresults = rolls[-advantage:]
        print("Advantage Results: "+joinlist(advantageresults) )
    elif advantage == 0:
        advantageresults = rolls
    #if there is advantage A, roll A extra dice and then take only the top (or bottom if A<0) N rolls

    if sum or average:
        totals = 0
        for r in range(len(advantageresults)):
            totals += advantageresults[r]
    #calculate the sum total (used for average and sum)
    
    if sum :        
        print("Sum: " + str(totals))
        if modifier != 0:
            print("Modified Sum: "+str(totals + modifier))
            #if there is a modifier, add it to the sum and print that too
    #print out the sum total if [sum] is true

    if average:
        average = round(totals / totalDice,2)
        print("Average roll: " + str(average))
        if modifier != 0:
            print("Modified Sum: "+str(average + modifier))

    if graph :
        set = set(rolls)
        rollset = [*set]
        bars = []
        for x in range(len(set)):
            bars.append((str(rollset[x]),rolls.count(rollset[x])))
        asciibars.plot(bars,unit='▓')
