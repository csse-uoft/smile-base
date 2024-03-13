from owlready2 import ObjectProperty, DataProperty, AnnotationProperty,FunctionalProperty, rdfs, ConstrainedDatatype, Thing, Property

from owlready2 import default_world, onto_path
onto_path.append('input/ontology_cache/')
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
rdf_nm =  default_world.get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

from pyscript.app.ontology.namespaces import ic, geo, cids, org, time, schema, sch, activity, landuse_50872, i72, owl




class hasServiceCertainty(cids.hasService, FunctionalProperty): # Each drug has a single cost
    range     = [float]

