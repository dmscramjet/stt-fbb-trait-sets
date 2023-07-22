from sttcrew import TraitSetDB

# get the full trait set DB
tdb = TraitSetDB()

# UNM/NM nodes must have between 2-5 matching portal crew
tdb.prune_nodes(n=1)
tdb.prune_nodes(n=5, is_min=True)

# this the full trait set db for UNM/NM
# lets track some stats
counts_3traits = {1:0, 2:0, 3:0, 4:0, 5:0}
counts_4traits = counts_3traits.copy()

# count the distribution over the full database 
for node, crew_list in tdb.items():
    ncrew = len(crew_list)
    ntraits = len(node)
    if ntraits == 3:
        counts_3traits[ncrew] += 1
    elif ntraits == 4:
        counts_4traits[ncrew] += 1

n3traits = sum(counts_3traits.values())
n4traits = sum(counts_4traits.values())

print(f'# of 3-trait nodes: {n3traits}')
for i in range(2,6):
    print(f'{counts_3traits[i]*100/n3traits:5.2f}% match {i} portal crew')

print(f'\n# of 4-trait nodes: {n4traits}')
for i in range(2,6):
    print(f'{counts_4traits[i]*100/n4traits:5.2f}% match {i} portal crew')