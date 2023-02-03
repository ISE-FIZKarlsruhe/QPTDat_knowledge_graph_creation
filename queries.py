#!/usr/bin/env

import pdb

import rdflib
import pandas


def loadGraph(rootPath):

    g = rdflib.Graph()
    
    g.parse(rootPath + "qptdat.ttl", format="ttl")
    g.parse(rootPath + "source.ttl", format="ttl")
    g.parse(rootPath + "source_quantity.ttl", format="ttl")
    g.parse(rootPath + "diagnostics.ttl", format="ttl")

    return g


def searchSubClasses(g, queryClass):
    q = """
        SELECT ?subClass ?subClassLabel
        WHERE {
            ?subClass rdfs:subClassOf ?queryClass . 
            OPTIONAL {?subClass rdfs:label ?subClassLabel . 
            FILTER (lang(?subClassLabel) = "en") }
        }
        """
    qres = g.query(q, initNs = {"rdfs": rdflib.namespace.RDFS},                        initBindings={"queryClass": queryClass})

    return qres

def searchPropertyRangeRestrictions(g, queryClass):
    q = """
        SELECT ?property ?requiredObject
        WHERE {
            ?queryClass rdfs:subClassOf* ?queryClasses .
            ?property rdfs:domain ?queryClasses .
            ?property rdfs:range ?requiredObject .
        }
        """
    qres = g.query(q, initNs = {"rdfs": rdflib.namespace.RDFS}, initBindings={"queryClass": queryClass})

    return qres



def main():

    g = loadGraph("../ontology/")
    qptDat = rdflib.Namespace("http://plasma-mds.org/qptdat#")
    
    qres = searchSubClasses(g, qptDat.Source)
   
    for x in qres:
        print(x)

    print(10*"=")
    qres = searchPropertyRangeRestrictions(g, qptDat.Source)

    for x in qres:
        print(x)

if __name__ == "__main__":
    main()
