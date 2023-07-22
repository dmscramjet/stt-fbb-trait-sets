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
        counts_3traits[ntraits] += 1
    elif ntraits == 4:
        counts_4traits[ntraits] += 1

print(f'# of 3-trait nodes {sum(counts_3traits.values())}')