
import re
import os
from glob import glob
from typing import Dict, List


patterns = {
    "cpp": r'#include (\"|<).*(\.h)?(\"|>)'
}

def findParents(fileAddress: str, lang: str = "cpp", maxDepth: int = 500)->List[str]:
    parents = []
    nameMatch = re.compile(r'((?<=<).+?(?=(\.h)?>)|(?<=\").+?(?=(\.h)?\"))') #include for c++

    if lang in patterns:
        patt = re.compile(patterns[lang])
    else:
        raise ValueError("No implementation for the given language.")

    with open(fileAddress) as f:
        count = 0
        while (line := f.readline()) and count < maxDepth: # checking whether the line is an include statement
            if re.match(patt, line):
                res = re.search(nameMatch, line)
                parents.append(res.group(0))
            count+=1
    
    return parents

def constructDiagram(dependencies: Dict[str, set]):

    cache = {}
    def rec(name: str)->set:
        if name in cache:
            return cache[name]

        elif name not in dependencies:
            cache[name] = set()
            return set()

        cache[name] = set() # handles self/circular dependancies
        toIgnore = set()
        for parent in list(dependencies[name]):
            if parent != name:
                toIgnore |= rec(parent)

        cache[name] = dependencies[name] - toIgnore
        return dependencies[name] | toIgnore


    
    
    for f in dependencies:
        rec(f)
        # unvisited = set(dependencies[f])
        # visited = set()
        # while unvisited:
        #     pass
        
    
    return cache

def main(directory: str, excludeSuffix: bool = True):
    files = glob(directory + os.sep + "*")
    dependencies = {}

    for _file in files:
        parents = findParents(_file)
        fName = re.search(r'([^/]*)(\.)(.*)$', _file).group(excludeSuffix)
        
        if fName in dependencies:
            dependencies[fName] |= set(parents) 
            dependencies[fName] -= set([fName])
        else:
            dependencies[fName] = set(parents)
        
    
        # print(f"file: {fName}, parents: {parents}")
    
    # for d in dependencies:
        # print(d, dependencies[d])

    graph = constructDiagram(dependencies)
    for d in graph:
        print(d, graph[d])

if __name__ == "__main__":
    # nameMatchRe = r'((?<=<).+?(?=(\.h)?>)|(?<=\").+?(?=(\.h)?\"))'
    main("/Users/hughparsons/Documents/PROGRAMMING/PROJECTS/biosim4/src")
    # print(findParents("test.cpp"))
    pass
