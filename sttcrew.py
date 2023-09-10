from copy import deepcopy
import json

class Node:
    """Node represents one node in a combo chain with a sorted tuple of traits
    """
    def __init__(self, traits:list|tuple) -> None:
        self._traits = tuple(sorted(traits))
    
    def __len__(self):
        return len(self._traits)

    def __hash__(self):
        return hash(self._traits)
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return len(self) == len(other) and all(a==b for a,b in zip(self._traits, other._traits))
        elif isinstance(other, (list,tuple,set)):
            return len(self) == len(other) and all(a==b for a,b in zip(self._traits, other))
        else:
            return False
    
    def __repr__(self):
        return f"Node({self._traits})"

    def __str__(self):
        return str(self._traits)


class TraitSetDB:
    def __init__(self, nmin:int=3, nmax:int=4, maxrarity:int=5, add_portal_only:bool=True, crewfile:str='crew.json'):
        self.nmin = nmin
        self.nmax = nmax
        self.maxrarity = maxrarity
        self.add_portal_only = add_portal_only
        self.crewfile = crewfile
        self._crewjson = None
        self._node_crew = {}
        self._load_crew()
    
    def __len__(self):
        return len(self._node_crew)
    
    def __str__(self):
        return str(self._node_crew)
    
    def __iter__(self):
        return iter(self._node_crew)

    def __getitem__(self, key):
        if isinstance(key, Node):
            return self._node_crew[key]
        elif isinstance(key, (list, tuple, set)):
            return self._node_crew[Node(key)]
    
    def values(self):
        return self._node_crew.values()

    def items(self):
        return self._node_crew.items()

    def keys(self):
        return self._node_crew.keys()
    
    def _load_crew(self):
        with open(self.crewfile, 'rb') as f:
            self._crewjson = json.load(f)
        
        for crew in self._crewjson:
            if self.add_portal_only and not crew['in_portal']:
                continue
            if crew['max_rarity'] <= self.maxrarity:
                self._add_crew(crew)
    
    def load_nonportals(self):
        if not self.add_portal_only:
            # already added
            return

        # make sure there is crew data
        if self._crewjson is None:
            with open(self.crewfile, 'rb') as f:
                self._crewjson = json.load(f)
        
        for crew in self._crewjson:
            if not crew['in_portal']:
                self._add_crew(crew)

    def _add_node_crew(self, node:Node, crew_name:str, create:bool=True):
        """add a specifice node and crew to the database

        Args:
            node (Node): the node (trait set)
            crew_name (str): name of crew to add
            create (bool, optional): create node in db if non-existent. Defaults to True.
        """
        if node in self._node_crew:
            self._node_crew[node].append(crew_name)
        elif create:
            self._node_crew[node] = [crew_name]
        
    def _add_crew(self, crew:dict):
        """add a crew (from datacore crew.json) to the database

        Args:
            crew (dict): crew from the parsed datacore crew.json 
        """
        create = True if crew['in_portal'] else False
        traits = crew['traits']
        ntraits = len(traits)
        name = crew['name']

        # loop over all the possible trait sets and add to database
        for i in range(ntraits):
            for j in range(i+1, ntraits):
                if self.nmin <= 2 and self.nmax >= 2:
                    nd = Node(traits[i], traits[j])
                    self._add_node_crew(nd, name, create)
                for k in range(j+1, ntraits):
                    if self.nmin <= 3 and self.nmax >=3:
                        nd = Node((traits[i], traits[j], traits[k]))
                        self._add_node_crew(nd, name, create)
                    for l in range(k+1, ntraits):
                        if self.nmin <= 4 and self.nmax >=4:
                            nd = Node((traits[i], traits[j], traits[k], traits[l]))
                            self._add_node_crew(nd, name, create)

    def prune_nodes(self, n:int, del_all_greater:bool=False):
        """prune nodes from db by number of matching crew

        Args:
            n (int): number of matching crew
            del_all_greater (bool): prune all nodes with more than (n) matching crew
        """

        # copy dict since it cannot be modified when iterated over
        dict_copy = deepcopy(self._node_crew)
        for nd, crew in self.items():
            if del_all_greater:
                if len(crew) > n:
                    del dict_copy[nd]
            else:
                if len(crew) < n:
                    del dict_copy[nd]
        
        self._node_crew = dict_copy
    
    def remove_crew_with_most_nodes(self):
        crew_nodes = {}
        # get the nodes for each crew in this db
        for node,crewlist in self._node_crew.items():
            for crew in crewlist:
                if crew in crew_nodes:
                    crew_nodes[crew].append(node)
                else:
                    crew_nodes[crew] = [node]
        
        max_nodes = 0
        max_crew = None

        for crew, nodelist in crew_nodes.items():
            if len(nodelist) > max_nodes:
                max_nodes = len(nodelist)
                max_crew = crew

        max_crew_nodelist = crew_nodes[max_crew]
        for node in max_crew_nodelist:
            self._node_crew.pop(node, None) #is node a string or object? does it matter?
        
        return max_crew, max_nodes
    
    def get_solved_node_crew(self, crew_ids:list[int])->list[str]:
        """Return crew names from the already parsed crew.json for a list
        of archetype ids that come from the ComboChain parsing player.json

        Args:
            crew_ids (list[int]): list of crew ids that solved a node

        Returns:
            list[str]: Names of crew that solved a node
        """
        crewlist = []
        for crew in self._crewjson:
            if crew['archetype_id'] in crew_ids:
                crewlist.append(crew['name'])
        
        return crewlist




        



