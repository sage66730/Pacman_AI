from searchAgents import PositionSearchProblem, CornersProblem

    if isinstance(problem, PositionSearchProblem):
        return generic(util.Queue(), problem, [])

    elif isinstance(problem, CornersProblem):
        start = problem.startingPosition
        stops = problem.corners
        n = len(stops)
        
        route1st = [ generic(util.Queue(), start, stops[i], problem, []) for i in range(n) ]
        dis1st = [ len(r) for r in route1st ]

        route = [[None for i in range(n)] for j in range(n)]
        dis = [[0 for i in range(n)] for j in range(n)]
        for i in range(n-1):
            for j in range(i+1, n): 
                route[i][j] = generic(util.Queue(), stops[i], stops[j], problem, [])
                route[j][i] = traceBack( route[i][j] )
                dis[i][j] = dis[j][i] = len(route[i][j])

        path = findShortestPath(dis1st, dis, route1st, route, n)
        return path

    else:
        util.raiseNotDefined()

def pathToActions(path):
    from game import Directions

    act = []
    for idx in range(len(path)-1):
        dx = path[idx+1][0] - path[idx][0]
        dy = path[idx+1][1] - path[idx][1]
        if dx==0 and dy ==1: act.append(Directions.NORTH)
        elif dx==0 and dy ==-1: act.append(Directions.SOUTH)
        elif dx==1 and dy ==0: act.append(Directions.EAST)
        elif dx==-1 and dy ==0: act.append(Directions.WEST)
        else: print("path wrong")

    return act

def generic(container, problem, path, prioFn=None):
    start = problem.getStartState()

    check = dict()
    path = { str(start):[] }

    if prioFn: container.push(start, prioFn(start))
    else: container.push(start)
    
    cur = None
    while not container.isEmpty():
        #print(container.list)

        cur = container.pop()
        if not check.get(str(cur), False):
            if problem.isGoalState(cur): break

            check[str(cur)] = True

            for nm, dir, _ in problem.getSuccessors(cur): 
                if not check.get(str(nm), False): 
                    if prioFn: container.push(nm, prioFn(nm))
                    else: container.push(nm)
                if not path.get(str(nm), False):
                    path[str(nm)] = path[str(cur)] + [dir]
        
    return path[str(cur)]

def traceBack(route):
    flip = {"West":"East", "East":"West", "North":"South", "South":"North"}
    back = [ flip[act] for act in route]
    back.reverse()
    return back

def findShortestPath(dis1st, dis, route1st, route, n):
    import itertools
    minDist = float("inf")
    minRoute = None

    permu = list(itertools.permutations( range(n) ))
    
    for p in permu:
        dist = sum([ dis[p[i]][p[i+1]] for i in range(n-1)]) + dis1st[p[0]]
        if dist < minDist:
            minDist = dist
            minRoute = p

    path = route1st[minRoute[0]]
    for i in range(n-1): path += route[minRoute[i]][minRoute[i+1]]

    return path


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    container = util.Queue()
    start = problem.getStartState()

    check = dict()

    container.push((start, [], 0))
    
    while not container.isEmpty():
        #print(container.list)

        cur = container.pop()
        cur_pos = cur[0]
        cur_path = cur[1]

        if not check.get(cur_pos, False):
            if problem.isGoalState(cur_pos): return cur_path

            check[cur_pos] = True

            for nm, dir, _ in problem.getSuccessors(cur_pos): 
                    if not check.get(nm, False): 
                        container.push( (nm, cur_path+[dir]) )
        
    return []
