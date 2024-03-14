from owlready2 import default_world, onto_path
import os, sys
onto_path.append(os.path.dirname(__file__)+'/ontology_cache/')
try:
    default_world.set_backend(filename='./db.sqlite')
except:
    print("loaded???")
print('Loading/Downloading ontologies, if the script stuck here, try re-run it.')

cids_url='cids.owl'
cids = default_world.get_ontology(cids_url).load(reload=True)

print('Ontology Loaded.')
owl = default_world.get_namespace('http://www.w3.org/2002/07/owl#')
ic = default_world.get_namespace('http://ontology.eil.utoronto.ca/tove/icontact#')
geo = default_world.get_namespace('http://www.w3.org/2003/01/geo/wgs84_pos/')
sch = default_world.get_namespace('https://schema.org/')
org = default_world.get_namespace("http://ontology.eil.utoronto.ca/tove/organization#")
time = default_world.get_namespace("http://www.w3.org/2006/time#")
schema = default_world.get_namespace("https://schema.org/")
dcterms = default_world.get_namespace("http://purl.org/dc/terms/")
activity = default_world.get_namespace('http://ontology.eil.utoronto.ca/tove/activity#')
landuse_50872 = default_world.get_namespace('http://ontology.eil.utoronto.ca/5087/2/LandUse/')
i72 = default_world.get_namespace('http://ontology.eil.utoronto.ca/ISO21972/iso21972#')
oep = default_world.get_namespace("http://www.w3.org/2001/sw/BestPractices/OEP/SimplePartWhole/part.owl#")

