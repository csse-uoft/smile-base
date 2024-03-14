from owlready2 import default_world
from owlready2 import class_construct as owlclass, OneOf
from .ontology.namespaces import compass, ic, geo, cids, org, time, schema, sch, activity, landuse_50872, i72, owl

class OntologyWrapper:
    """
    The OntologyWrapper class wraps an ontology and its main components. It acts
    As an interface to the Controller. It can be used to identofy differnt NER entities,
    and their related entities. 
    For example, a LogicModel has several properties, each with range entity type, i.e. their class.
        Domain Entity   Property                    Range Entity
        cids.LogicModel cids.hasActivity            cids.Activity
        cids.LogicModel cids.hasCharacteristic      cids.Characteristic
        cids.LogicModel cids.hasInput               cids.Input
        cids.LogicModel cids.hasOutcome             cids.Outcome
        cids.LogicModel cids.hasOutput              cids.Output
        cids.LogicModel cids.hasProgram             cids.Program
        cids.LogicModel cids.hasStakeholder         cids.Stakeholder
        cids.LogicModel cids.hasStakeholderOutcome  cids.StakeholderOutcome
        cids.LogicModel activity.hasResource        activity.Resource
    ...

    Attributes
    ----------
    klass_mapper : dict
        The dictionary used to map OWL classes to NEr entity labels, and which 
        properties to get those labels from.
    klasses : dict
        A colleciton of classes in the ontology, used to make use of the ontology structure easier. 
    """



    # klasses mapped to NER types, and where to get them.
    klass_mapper = {
        cids.Program :  {org.hasName:['program_name'], cids.hasDescription:['program_desc']},
        cids.Service :  {org.hasName:['service_name'], cids.hasDescription:['service_desc'], org.hasName:['need_satisfier']},
        cids.BeneficialStakeholder : {cids.hasCharacteristic:['client'], cids.hasDescription:['client_desc']},
        cids.Organization : {org.hasName:['organization'], cids.hasDescription:['organization_desc']},
        cids.StakeholderOutcome    : {cids.hasDescription:['stakeholder_outcome']},
        cids.Input   :  {org.hasName:['service_input']},
        cids.Output  :  {org.hasName:['service_output']},
        cids.Outcome  :  {org.hasName:['service_outcome']},
        cids.Stakeholder : {org.hasName:['stakeholder']},
        # landuse_50872.LandArea : {landuse_50872.parcelHasLocation:['catchment_area']},
    }


    def __init__(self):
        """Initiatialize the OntologyWrapper() class."""
        self.klasses = {}

    def get_LogicModel(self):
        """return the root of the Compass ontology, namely the Logic Model
        return: cids.LogicModel
        """
        return cids.LogicModel

    def get_properties(self,klass):
        """ Get properties for an OWL class.
        klass : Object
            The object for which properites are extracted.
        :return : props as a list of property definitions
        """
        # [prop for prop in list(klass.INDIRECT_get_class_properties()) if isinstance(prop, owlclass.Restriction)]        
        props = []
        if not isinstance(klass,str) and 'is_a' in klass.__dict__.keys():
            props = [prop for prop in klass.__dict__['is_a'] if isinstance(prop, owlclass.Restriction)]        
        return props
    def collect_klass_properties(self,klass):
        """
        Method for recursively collecting al properites of the given klass, and its subproperties. 
        Results are stored in self.klasses.

        klass : Object
            Class to be searched for properties.
        :return
        """
        ow = self
        try:
            klasses = klass.Classes
        except AttributeError:
            klasses = [klass]

        for klass in klasses:
            if klass in ow.klasses.keys():
                continue
            ow.klasses[klass] = {}
            for prop1 in ow.get_properties(klass):
                try:
                    klasses2 = prop1.value.Classes
                except:
                    if isinstance(prop1.value, OneOf):
                        klasses2 = prop1.value.instances
                    else:
                        klasses2 = [prop1.value]
                prop2 = prop1.property

                ow.klasses[klass][prop2] = klasses2
                for klass2 in klasses2:
                    # if not isinstance(klass2, str) and 
                    if klass != klass2 and klass2 not in ow.klasses.keys():
                        ow.collect_klass_properties(klass2)

    def show_klasses(self):
        """Display the collected self.klasses."""
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(self.klasses)


if __name__ == '__main__':
    ontology = OntologyWrapper()
    klass = ontology.get_LogicModel()
    ontology.collect_klass_properties(klass)
    ontology.show_klasses()

    graph = ontology.klasses#[cids.LogicModel]
    s = Search(graph, debug=True)
    s.children(['root1','root2',klass])


    res = []
    for k,v in ontology.klasses.items():
        for k2,v2 in v.items():
            for v3 in v2:
                if org.hasName == k2:
                    print(k,k2,v2, v3)

def getPropertyChain(prop, w=default_world) :
        chain = []
        rdfGraph = w.as_rdflib_graph()
        obj = rdfGraph.value(URIRef(prop.iri), OWL.propertyChainAxiom)
        while obj != RDF.nil :
                chain.append(IRIS[str(rdfGraph.value(obj, RDF.first))])
                obj = rdfGraph.value(obj, RDF.rest)
        return(chain)