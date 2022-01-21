import json
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, FOAF, RDFS, OWL

DCT = Namespace("http://purl.org/dc/terms/")
SCHEMA = Namespace("http://schema.org/")

mapPreds = {
    "thisVersionURI": OWL.versionIRI,
    "ontologyRevisionNumber": OWL.versionInfo,
    "ontologyTitle": DCT.title,
    "abstract": DCT.description 
}

# Read in template
file = open("template.json")
config = json.load(file)
file.close()

# Parse ontology file
g = Graph()
g.parse("../glosis_main.ttl")


# Ontology namespace
for s, p, o in g.triples((None, RDF.type, OWL.Ontology)):
    config["ontologyNamespaceURI"] = s

# Title, abstract and similar
for item in mapPreds.items():
    for s, p, o in g.triples((None, item[1], None)):
        config[item[0]] = o


# Creators
for s, dc_creator, creator in g.triples((None, DCT.creator, None)):
    for s2, p2, name in g.triples((creator, FOAF.name, None)):
        config["authors"] += name + ";"
    for s3, p3, uri in g.triples((creator, RDFS.seeAlso, None)):
        config["authorsURI"] += uri + ";"
    for s4, p4, institute in g.triples((creator, SCHEMA.affiliation, None)):
        for s5, p5, inst_name in g.triples((institute, FOAF.name, None)):
            config["authorsInstitution"] += inst_name + ";"
        for s6, p6, inst_uri in g.triples((institute, RDFS.seeAlso, None)):
            config["authorsInstitutionURI"] += inst_uri + ";"

# Contributors
for s, dc_contributor, contributor in g.triples((None, DCT.contributor, None)):
    for s2, p2, name in g.triples((contributor, FOAF.name, None)):
        config["contributors"] += name + ";"
    for s3, p3, uri in g.triples((contributor, RDFS.seeAlso, None)):
        config["contributorsURI"] += uri + ";"
    for s4, p4, institute in g.triples((contributor, schema_affil, None)):
        for s5, p5, inst_name in g.triples((institute, FOAF.name, None)):
            config["contributorsInstitution"] += inst_name + ";"
        for s6, p6, inst_uri in g.triples((institute, RDFS.seeAlso, None)):
            config["contributorsInstitutionURI"] += inst_uri + ";"


# Dump WiDoco config file
textfile = open("glosis_main.config", "w")

for key in config:
    a = textfile.write("%s=%s\n" % (key, config[key]))

textfile.close()

