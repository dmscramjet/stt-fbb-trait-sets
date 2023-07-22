from sttcrew import TraitSetDB

tdb = TraitSetDB(nmin=3, nmax=4, add_portal_only=True)
tdb.prune_nodes(n=1)
tdb.prune_nodes(n=5, is_min=True)


print(tdb[('resourceful','starfleet','inspiring','hero')])
tdb.load_nonportals()
print(tdb[('resourceful','starfleet','inspiring','hero')])
