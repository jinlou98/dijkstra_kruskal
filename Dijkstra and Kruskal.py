
import sys
import heapq

############################

# DO NOT CHANGE THIS PART!!

############################

def readGraph(input_file):
    with open(input_file, 'r') as f:
        raw = [[float(x) for x in s.split(',')] for s in f.read().splitlines()]
    N = int(raw[0][0])
    m = int(raw[1][0])
    s = int(raw[2][0])
    adj_list = [[] for foo in range(N)]
    for edge in raw[3:]:
        adj_list[int(edge[0])].append((int(edge[1]), edge[2]))
    return N, m, s, adj_list


def writeOutput(output_file, N, s, distances, parents, mst):
    with open(output_file, 'w') as f:
        # output dijkstra
        for i in range(N):
            if i == s:
                f.write('0.0,-\n')
            else:
                f.write(str(distances[i])+','+str(parents[i])+'\n')
        
        # blank space
        f.write('\n')

        #output MST (just neighbors, no edge weights)
        for j in range(N):
            neighbors = []
            for node in mst[j]:
                neighbors.append(str(node[0]))
            # sort for the autograder
            neighbors.sort()
            f.write(','.join(neighbors) +'\n')

# 
def make_undirected_graph(N, adj_list):
    G = {}
    for u in range(N):
        G[u] ={}

    # move our stuff in
    for u in range(N):
        for v in adj_list[u]:
            G[u][v[0]] = v[1]
            G[v[0]][u] = v[1]
    #back to list
    adj_list = ['x' for x in range(N)]
    for u in range(N):
        neighbors = []
        for v in G[u].keys():
            neighbors.append((v, G[u][v]))
        adj_list[u] = list(set(neighbors))
    return adj_list





def Run(input_file, output_file):
    N, m, s, adj_list = readGraph(input_file)
    distances, parents =   dijkstra(N, m, s, adj_list)
    undirected_adj_list = make_undirected_graph(N, adj_list)
    mst = kruskal(N, m, undirected_adj_list)
    writeOutput(output_file, N, s, distances, parents, mst)


############################

# ADD YOUR OWN METHODS HERE (IF YOU'D LIKE)

############################

# def initialize(S):
#     # islands array: name of island head
#     head = [] * S

#     # member array+LL: each entry stores three things
#     member = [] * S

#     for i in range(0,S):
#         head[i] = (i,None)
#         is_the_head = True
#         size = 1
#         tail = head[]
#         member[i] = (is_the_head, size, tail)

#     # return array+LL
#     return head, member


# def find(u, head):
#     c_head = head[u]
#     return c_head


# def union(a, b, head):
#     for i in head:
#         if i == a:
#             i = b

#     return head


def union_find(member, n1, n2):
    p1 = member[n1][1]
    p2 = member[n2][1]

    # case 1: both pointer null
    # different CC'
    if p1 == "None" and p2 == "None":
        return n1, n2

    # case 2: both pointer not null
    elif p1 != "None" and p2 != "None":
        while p1 != "None":
            if member[p1][1] == "None":
                break
            else:
                p1 = member[p1][1]

        while p2 != "None":
            if member[p2][1] == "None":
                break
            else:
                p2 = member[p2][1]

    # case 3: one pointer null and the other one not
    elif p2 != "None" and p1 == "None":
        while p2 != "None":
            if member[p2][1] == "None":
                break
            else:
                p2 = member[p2][1]
        p1 = n1

    # case 4: one point not null and the other one is null
    elif p1 != "None" and p2 == "None":
        while p1 != "None":
            if member[p1][1] == "None":
                break
            else:
                p1 = member[p1][1]
        p2 = n2

    if p1 != p2:
        return p1, p2

    # same CC'
    return False, False

############################

# FINISH THESE METHODS

############################



def dijkstra(N, m, s, adj_list):
    # You are given the following variables:
    # N = number of nodes in the graph
    # m = number of edges in the graph
    # s = source node for the algorithm
    # adj_list = a list of lists of size N, where each index represents a node n
    #               the sublist at index n has a list of two-tuples,
    #               representing outgoing edges from n: (adjacent node, weight of edge)
    #               NOTE: If a node has no outgoing edges, it is represented by an empty list
    #
    # WRITE YOUR CODE HERE:

    # initialize distance and parents
    distances = {}
    parents = {}
    visited = []

    # priority queue
    pq = []
    pi = [sys.maxsize] * N

    #Step 1: For each node, set its distance to infinity
    for i in range(0,N):
        distances[i] = float("inf")
        parents[i] = 'none'
		
    distances[s] = 0
    pi[s] = 0

    # append source node to pq
    heapq.heappush(pq,(0,s))

    while pq != []:
        # all nodes visited
        if len(visited) == N:
            break

        # extract the min
        # x = weight, y = destination
        (x, y) = heapq.heappop(pq)
        
        # update visited
        if y in visited:
            continue

        node = adj_list[y]
        distances[y] = x

        # i = destination   j = weight
        for i in node:
            (m,n) = i
            if m not in visited:
                new_dist = x + n
                prev_dist = pi[m]

                if(new_dist < prev_dist):
                    pi[m] = new_dist
                    parents[m] = y
                    heapq.heappush(pq,(pi[m],m))

        visited.append(y)
        


    # Return two lists of size N, in which each index represents a node n:
    # distances: the shortest distance from s to n
    # parents: the last (previous) node before n on the shortest path
    return distances, parents

def kruskal(N, m, undirected_adj_list):
    # You are given the following variables:
    # N = number of nodes in the graph
    # PLEASE NOTE THAT THE ADJACENCY LIST IS FORMATTED ENTIRELY DIFFERENTLY FROM DIJKSTRA ABOVE
    # undireced_adj_list = a list of lists of size N, where each index represents a node n
    #                       the sublist at index n has a list of two-tuples, representing edges from n: (adjacent node, weight of edge)
    #                       NOTE: Since the graph is undirected, each edge (u,v) is now represented twice in this adjacency list:
    #                               once at index u and once at index v
    #
    # WRITE YOUR CODE HERE:
    edges = []
    visited = []
    member = []
    mst_adj_list = []

    # # sort edges so that w1<w2<...<wm
    # sorted(sort_list.keys(), key=lambda x: sort_list[x][3], reverse=True)

    # # initialize collection of components: each vertex is alone in its component
    # head, member = initialize(N)

    # Initialization
    for i in range(N):
        mst_adj_list.append([])
        # size of members
        member.append([1,"None"])   

    # Edge convertion
    for i in range(len(undirected_adj_list)):
        # check all neighbors
        for j in undirected_adj_list[i]:
            (a,b) = j
            # only push when the dest node hasnt checked yet
            # avoid duplicated edges in edges[]
            if a not in visited:
                # edges (weight, start, destination)
                # sort in the increasing order of weights
                heapq.heappush(edges,(b, i, a))
        # update visited
        visited.append(i)

    # # for e=1 to m   e-edges
    # # let (u,v) be the end points of e
    # # if u,v are in the same connected component
    # # T = T U {e}
    # # merge components of u, v
    # for (x,y,z) in sort_list:
    #     # have same header = in the same CC
    #     if(head[x] != head[y]):
    #         # merge two CC
    #         head = union(x,y,head)


    # walk through the edges
    for i in range(len(edges)):
        (x, y, z) = heapq.heappop(edges)
        #print("current edge = (", b, ",", c, ")")
        
        a, b = union_find(member, y, z)
        
        # two nodes in the same CC'
        if a == False and b == False:
            continue
        else:
            # size y < size z
            if member[a][0] < member[b][0]:
                member[b][0] += member[a][0]
                member[a][1] = b        #update head
            # size y >= size z
            else:
                member[a][0] += member[b][0]
                member[b][1] = a        #update head

            mst_adj_list[z].append((y, x))
            mst_adj_list[y].append((z, x))
            

    # Return the adjacency list for the MST, formatted as a list-of-lists in exactly the same way as undirected_adj_list
    
    return mst_adj_list




#############################
# CHANGE INPUT FILES FOR PART 2 HERE

#############################

def main(args=[]):
    # WHEN YOU SUBMIT TO THE AUTOGRADER, 
    # PLEASE MAKE SURE THE FOLLOWING FUNCTION LOOKS LIKE:
    Run('input', 'output')
    # Run('05_input', '05_output')

    # AFTER YOUR RUN THE AUTOGRADER,
    # you may change comment out the above line
    # and uncomment the Run commend for the graph from part 2
    # that you wish to work on:
    
    # Run('g_randomEdges.txt', 'output_random')
    #Run('g_donutEdges.txt', 'output')
    #Run('g_zigzagEdges.txt', 'output')

if __name__ == "__main__":
    main(sys.argv[1:])    