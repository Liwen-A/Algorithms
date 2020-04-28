#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 19:08:09 2020

 Two derterminsistic Algorithms to find the MST of a given graph (and potentially a random one with better performance)
with implemented UnionFind and Boruvka step

@author: liwenouyang
"""

import networkx as nx
import random
import math


class UnionFind:
    """
    A UnionFind data structure used in Boruvka step, implemented with path compression and union by rank
    """
    def __init__(self, graph):
        """
        args: graph: a nx.graph object with nodes labeled by distinct integers
        """
        self.parent ={}
        self.rank ={}
        for i in graph.nodes:
            self.parent[i] = i
            self.rank[i] = 0
     
    def find(self,i):
        """
        args: i: an int as the lable of a node
        returns: the label of the representitive node in the set i belongs to 
        """
        if self.parent[i] == i:
            return i
        return self.find(self.parent[i])

    def union(self, x, y):
        """
        merge the two sets nodes x,y belong to
        """
        xroot = self.find(x)
        yroot = self.find(y)
        if xroot == yroot:
            return 
        if self.rank[xroot] < self.rank[yroot]:
            self.parent[xroot] = yroot
        elif self.rank[xroot] > self.rank[yroot]:
            self.parent[yroot] = xroot
        else:
            self.parent[yroot] = xroot
            self.rank[xroot] += 1

"""two test graphs g and t"""
g = nx.Graph()
g.add_nodes_from(range(7))
g.add_weighted_edges_from([(0,1,12),(1,2,8),(1,3,10),(0,3,5),(1,4,7),(2,4,2)])
g.add_weighted_edges_from([(3,4,15),(3,5,6),(4,5,1),(4,6,9),(5,6,11)])



t = nx.Graph()
t.add_nodes_from(range(9))
t.add_weighted_edges_from([(0,1,4),(0,7,8),(1,7,11),(1,2,8),(7,8,7),
                           (7,6,1),(2,8,2), (2,5,4),(2,3,7),(8,6,6),
                           (6,5,2),(3,5,14),(3,4,9),(5,4,10)])


def getKey(a):
    """
    construct a unique key for an given edge to avoid duplicate edges and loops when contracting nodes during a boruvka step
    """
    if a[0] < a[1]:
        return a
    if a[0] > a[1]:
        return (a[1],a[0])
    else:
        return None
                          
def Boruvka(g): 
    """
    Given a graph, perform one boruvka step on the graph
    returns N: a contracted graph 
            R: the list of edges that are  selected, which by cut property belongs to a MST of G
    """
    if len(g.nodes) <= 1:
        return g, set()
    u = UnionFind(g)
    R= set()
    for n in g.nodes:
        e = min(g.edges(n,data= True), key = lambda x: x[2]['weight'])
        R.add(getKey((e[0],e[1])))
        u.union(e[0],e[1])
    N = nx.Graph()
    d ={}
    for e in g.edges(data = 'weight'):
        k1,k2 = u.find(e[0]),u.find(e[1])
        if k1 != k2 and k1 not in d.keys():
            d[k1] = [e]
        if k1!= k2 and k2 not in d.keys():
            d[k2] = [e]
        if k1!=k2 and k1 in d.keys() and k2 in d.keys():
            d[k1].append(e)
            d[k2].append(e)
    newEdge = set()
    newNodes = set()
    for l in d.values():
        e = min(l, key = lambda x: x[2])
        newEdge.add(e)
        newNodes.add(e[0])
        newNodes.add(e[1])
    N.add_nodes_from(newNodes)
    N.add_weighted_edges_from(newEdge)  
    return N,R

def randomSub(G):
    """
    Get a random subgraph of G by sampling each edge  of G with p = 1/2 
    """
    E = []
    N = set()
    for e in G.edges(data = 'weight'):
        n = random.randint(0,1)
        if n == 1:
            E.append(e)
            N.add(e[0])
            N.add(e[1])
    g = nx.Graph()
    g.add_nodes_from(N)
    g.add_weighted_edges_from(E)
    print(g.edges)
    return g


def fHeavy(G,F):
    """
    A compromise due to my inability to implement linear-time MST verification algorithm. This simply calculate the MST of G
    and characterizes any edge that is not in the MST of G as F-heavy 
    Potential Fix: Linear-time MST verification algorithm provided by Hagerup 
    """
    mst = nx.minimum_spanning_tree(G).edges
    f= []
    for e in G.edges:
        if e not in mst:
            f.append(e)
    return f


def BoruvkaMST(g):
    """A natural extention of Boruvka step that gives us a O(mlogn) MST algorithm
    args: a graph object G
    returns: list of edges of a MST of G
    """
    R = set()
    while not len(Boruvka(g)[1]) == 0:
        n,r = Boruvka(g)
        g = n
        R = R|r
    return R



def hybridMST(g):
    """
    run loglog n boruvka steps to get a contracted graph g', use kruskal's to get the MST of g', which
    combined with results from the boruvka steps, gives the MST of G in O(m loglog n) time. 
    """
    E = set()
    numiter = math.ceil(math.log(math.log(len(g.nodes),2),2))
    for i in range(numiter):
        g1, e = Boruvka(g)
        E = E |e
    t1 = set(nx.minimum_spanning_tree(g1,algorithm = 'prim').edges)
    return t1|E

def randomMST(G):
    """
    The randomized recursive algorithm to calculate MST in expected linear-runtime proposed by Karger, Klein,Tarjan 
    args: A nx graph object 
    returns: the MST of  the contracted graph G' and the set of other edges that belong to the MST of G, which together forms the MST of G
    Note: the implementation is not done because of the lack of an implementation of a  linear time MST verification algorithm 
    """
    pass
    

