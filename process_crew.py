import json

######################################
# how to use this
#  o You need a crew.json file
#    https://github.com/stt-datacore/website/blob/master/static/structured/crew.json
#  o if you want it write all the unique trait set counts to csv files, set write to True
#    - these files are semi-colon delimited becase crew have commas in them
#    - if importing to Google sheets, make sure to choose delimiter as ;

# read in the data
with open('crew.json', 'r', encoding='utf-8') as f:
    allcrew = json.load(f)

# create empty dictionary to hold lists of all crew that match a trait set
trait_set_crew = {}
# create a set to hold all crew names - use set so we can use set operations later
all_crew_names = set()

# loop over all crew
for crew in allcrew:
    # get the trait list
    t = crew['traits']
    ntraits = len(t)
    # collect crew name
    all_crew_names.add(crew['name'])

    # loop over all traits - note that since we only care about trait combinations, we can shorten the trait loops
    for i in range(ntraits):
        for j in range(i+1,ntraits):
            for k in range(j+1,ntraits):
                # create a tuple (which is immutable=hashable for dict) of the trait names
                triplet = tuple(sorted(set([t[i], t[j], t[k]]))) 

                # if this trait triplet is already in our dict, add the crew name to the existing list
                if triplet in trait_set_crew:
                    trait_set_crew[triplet].append(crew['name'])
                # if this trait triplet is new, make a new list if crew is in portal
                elif crew['in_portal']: 
                    trait_set_crew[triplet] = [crew['name']]
                
                # loop over the remaining traits to look at quadruples
                for l in range(k+1,ntraits):
                    quadruplet = tuple(sorted(set([t[i], t[j], t[k], t[l]]))) # sort alphabetically so trait order won't matter

                    # if it exists, add this crew's name to the existing list
                    if quadruplet in trait_set_crew:
                        trait_set_crew[quadruplet].append(crew['name'])
                    # otherwise add new list to dict if crew is in portal
                    elif crew['in_portal']: 
                        trait_set_crew[quadruplet] = [crew['name']]

# now we have a list of every triplet and quadruplet trait combo from portal crew in the game
# tell us how many trait sets in all
print(f'Number of total 3- and 4-trait sets: {len(trait_set_crew)}\n')

# empty dict to store the number of unique trait sets per crew
unique_sets = {}
tot_unique = 0
# loop over the trait tuples
for t, crew_list in trait_set_crew.items():
    # unique trait set has only one crew
    if len(crew_list) == 1:
        crew = crew_list[0]
        tot_unique += 1
        # if crew is in dict, add this trait tuple to that crew's list
        if crew in unique_sets:
            unique_sets[crew].append(t)
        else:  # first time this crew has a unique set, add it to the dict
            unique_sets[crew] = [t]

print(f'Number of 3- and 4-trait sets unique to one crew: {tot_unique}\n')

# crew with no unique trait sets = all_crew - unique_crew
non_unique_crew = all_crew_names.difference(set(unique_sets.keys()))

# now find the top N crew with unique trait combos
num_best = 20
max = [0]*num_best
best = ['']*num_best
# loop over all the unique trait sets
for crew in unique_sets:
    # get number of unique trait sets for this crew
    num_unique = len(unique_sets[crew])
    # list is always sorted low-to-high
    if num_unique > max[0]:
        max[0] = num_unique
        best[0] = crew
        best = [c for _,c in sorted(zip(max,best))]
        max = sorted(max)
    elif num_unique == max[0]:
        # it's a tie, just throw it in there as well
        max.insert(0, num_unique)
        best.append(crew)

# print a CSV with all the data for each crew rarity

# loop over rarities
for i in range(1,6):
    f = open(f'{i}star_unique_trait_sets.csv', 'w')
    f.write('Crew; # Unique Trait Sets\n')
    counts = {}
    # loop over crew
    for crew in allcrew:
        if crew['max_rarity'] == i:
            name = crew['name']
            if name in unique_sets:
                counts[name] = len(unique_sets[name])
    # sort the list by # of unique trait sets descending
    for crew,count in sorted(counts.items(),key=lambda item:item[1],reverse=True):
        f.write(crew+'; '+str(count)+'\n')
    f.close()

# print a summary report
print('-'*30)
print('Best crew for FBB trait matching (# unique trait sets)')
# print out the Top (num_best) crew
for i in range(len(best)-1,len(best)-num_best-1,-1):
    #print(str(best[i]) + ':' + ' '*(29-len(str(best[i]))) + str(max[i]))
    print(str(best[i]) + ': ' + str(max[i]))

print('\n')
print('Crew with no unique trait sets')
bad_crew = {}
# loop over all crew
for crew in allcrew:
    name = crew['name']
    # just do legendaries for now
    if crew['max_rarity'] == 5 and name in non_unique_crew:
        bad_crew[name] = crew['bigbook_tier']

last_tier = 0
# print out the bad crew by Big Book Tier
for crew,tier in sorted(bad_crew.items(),key=lambda item:item[1]):
    if tier == 8:
        # print the header?
        if tier > last_tier:
            last_tier = tier
            print('\n----------Tier 8-----------')
        print(crew)
    elif tier == 9:
        # print the header?
        if tier > last_tier:
            last_tier = tier
            print('\n----------Tier 9-----------')
        print(crew)
    elif tier > 9:
        # print the header?
        if tier > last_tier:
            last_tier = tier
            print('\n----------Tier 10----------')
        print(crew)