import re, os
from owlready2 import default_world, ObjectProperty, DataProperty, rdfs, Thing 
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)

with smile:
    from ...ontology.extra import *
    from py2graphdb.Models.graph_node import GraphNode
    from py2graphdb.utils.db_utils import SPARQLDict, _resolve_nm, encode_inst, resolve_nm_for_dict, PropertyList
    from .ks_input import KsInput
    from .ks_output import KsOutput

class Ks(GraphNode):
    """
    A db Model class that defines the schema for Knowledge Source.
    Instances of this class are created only once when the database is created.

    ...

    Attributes
    ----------
    __tablename__ : str
        The name of the database table
    id : SQLAlchemy.Column
        A unique ID for the knowledge source type
    name : SQLAlchemy.Column
        The name of the knowledge source
    inputs : SQLAlchemy.relationship
        Relationship with knowledge source input data levels
    outputs : SQLAlchemy.relationship
        Relationship with knowledge source output data levels
    """
    klass = 'smile.Ks'
    super_relations = GraphNode.relations
    klass_relations = {
        'name' : {'pred':smile.hasName, 'cardinality':'one'},
        'py_name' : {'pred':smile.hasPyName, 'cardinality':'one'},
        'ks_ars' : {'pred':smile.hasKSARs, 'cardinality':'many'},
        'group_input' : {'pred':smile.isGroupInput, 'cardinality':'one'},
        'inputs' : {'pred':smile.hasInputDataLevels, 'cardinality':'many'},
        'outputs' : {'pred':smile.hasOutputDataLevels, 'cardinality':'many'},
    }
    relations = {**klass_relations, **super_relations}

    def __init__(self, inst_id=None, inst=None, keep_db_in_synch=True) -> None:
        super().__init__(inst_id=inst_id, inst=inst, keep_db_in_synch=keep_db_in_synch)
       
    from py2graphdb.utils import db_utils
    def_file_path = os.path.dirname(db_utils.__file__) + '/_model_getters_setters_deleters.py'
    imported_code = open(def_file_path).read()
    exec(imported_code)


    ALL_KS_FORMATS = {
        # 'Parse/Query': ['ParseQuery', False, ['Query'], ['Text']], #SearchTextGraph
        # 'Search Text Graph': [None, False, ['Text_Field'], ['Text_Field']], #SearchTextGraph
        # 'Search Ontology Graph': [None, False, ['Ner'], ['Rel']], #SearchOntologyGraph
        # # 'Query Input': ['QueryInput', ['Query'], ['Text']],
        # 'Parse/Tokenize': ['ParseTokenize', False, ["Text"], ["Word", "Pos", "Dep", "CoRef"]],
        # 'QA-0 (Text)(Organization)': ['Qa0Ner', False, ["Text"], ["Organization"]],
        # 'QA-0 (Sentence)(Organization)': ['Qa0Ner', False, ["Sentence"], ["Organization"]],
        # 'QA-0 (Text)(Program)': ['Qa0Ner', False, ["Text"], ["Program"]],
        # 'QA-0 (Sentence)(Program)': ['Qa0Ner', False, ["Sentence"], ["Program"]],
        # 'QA-0 (Outcome)': ['Qa0Ner', False, ["Text"], ["Outcome"]],
        # 'QA-0 (Outcome)': ['Qa0Ner', False, ["Sentence"], ["Outcome"]],
        # 'QA-0 (BeneficialStakeholder)': ['Qa0Ner', False, ["Text"], ["BeneficialStakeholder"]],
        # 'QA-0 (BeneficialStakeholder)': ['Qa0Ner', False, ["Sentence"], ["BeneficialStakeholder"]],
        # 'QA-0 (CatchmentArea)': ['Qa0Ner', False, ["Text"], ["CatchmentArea"]],
        # 'QA-0 (CatchmentArea)': ['Qa0Ner', False, ["Sentence"], ["CatchmentArea"]],

        # # 'QA-0 (Organization)': ['Qa0Ner_Organization', False, ["Text", "Sentence"], ["Organization"]],
        # # 'QA-0 (Program)': ['Qa0Ner_Program', False, ["Text", "Sentence"], ["Program"]],
        # # 'QA-0 (Outcome)': ['Qa0Ner_Outcome', False, ["Text", "Sentence"], ["Outcome"]],
        # # 'QA-0 (Client)': ['Qa0Ner_Client', False, ["Text", "Sentence"], ["Client"]],
        # # 'QA-0 (BeneficialStakeholder)': ['Qa0Ner_BeneficialStakeholder', False, ["Text", "Sentence"], ["BeneficialStakeholder"]],
        # # 'QA-0 (CatchmentArea)': ['Qa0Ner_CatchmentArea', False, ["Text", "Sentence"], ["CatchmentArea"]],

        # # 'QA-1 (NER)': ['Qa1Ner', False, ["Text", "Sentence", "Ner"], ["Ner", "Phrase"]],
        # 'QA-1 (Organization,Text)(Program)': ['Qa1Ner', False, ["Text", "Organization"], ["Program"]],
        # 'QA-1 (Organization,Sentence)(Program)': ['Qa1Ner', False, ["Sentence", "Organization"], ["Program"]],
        # 'QA-1 (Organization,Text)(BeneficialStakeholder)': ['Qa1Ner', False, ["Text", "Organization"], ["BeneficialStakeholder"]],
        # 'QA-1 (Organization,Sentence)(BeneficialStakeholder)': ['Qa1Ner', False, ["Sentence", "Organization"], ["BeneficialStakeholder"]],
        # # 'QA-1 (Organization)(Client)': ['Qa1Ner_Organization_Client', False, ["Text", "Sentence", "Organization"], ["Client"]],
        # # 'QA-1 (Organization)(BeneficialStakeholder)': ['Qa1Ner_Organization_BeneficialStakeholder', False, ["Text", "Sentence", "Organization"], ["BeneficialStakeholder"]],
        # # 'QA-1 (Organization)(Outcome)': ['Qa1Ner_Organization_Outcome', False, ["Text", "Sentence", "Organization"], ["Outcome"]],
        # # 'QA-1 (Organization)(CatchmentArea)': ['Qa1Ner_Organization_CatchmentArea', False, ["Text", "Sentence", "Organization"], ["CatchmentArea"]],


        # 'QA-1 (Program,Text)(Organization)': ['Qa1Ner', False, ["Text", "Program"], ["Organization"]],
        # 'QA-1 (Program,Sentence)(Organization)': ['Qa1Ner', False, ["Sentence", "Program"], ["Organization"]],
        # 'QA-1 (Program,Text)(BeneficialStakeholder)': ['Qa1Ner', False, ["Text", "Program"], ["BeneficialStakeholder"]],
        # 'QA-1 (Program,Sentence)(BeneficialStakeholder)': ['Qa1Ner', False, ["Sentence", "Program"], ["BeneficialStakeholder"]],
        # # 'QA-1 (Program)(Client)': ['Qa1Ner_Program_Client', False, ["Text", "Sentence", "Program"], ["Client"]],
        # # 'QA-1 (Program)(BeneficialStakeholder)': ['Qa1Ner_Program_BeneficialStakeholder', False, ["Text", "Sentence", "Program"], ["BeneficialStakeholder"]],
        # # 'QA-1 (Program)(Outcome)': ['Qa1Ner_Program_Outcome', False, ["Text", "Sentence", "Program"], ["Outcome"]],
        # # 'QA-1 (Program)(CatchmentArea)': ['Qa1Ner_Program_CatchmentArea', False, ["Text", "Sentence", "Program"], ["CatchmentArea"]],


        # 'Text To Sentences': ['TextToSentences', False, ["Text"], ["Sentence","Word"]],
        # 'Find_HighSP_low_NERs': ['Find_HighSP_low_NERs', False, ['Sentence'], ['Ner']],
        # 'Find_LowSP': ['Find_LowSP', False, ['Sentence'], ['Ner']],
        # # 'QA-0 (Phrase)': ['Qa0Phrase', False, ["Text"], ["Phrase"]],
        # # "NERx (NER)": [None, False, ["Text"], ["Ner"]],
        # # "AllenNLP (NER)": ['NerAllenNer', False, ["Text"], ["Ner"]],
        # # "Stanza (NER)": ['NerStanzaNer', False, ["Text"], ["Ner"]],
        # # "Spacy Rob (NER)": ['NerSpacyRobNer', False, ["Text"], ["Ner"]],
        # # "Spacy Trad (NER)": ['NerSpacyTradNer', False, ["Text"], ["Ner"]],
        # # "NERx (Phrase)": [None, False, ["Text"], ["Phrase"]],
        # # "CoRef (Words)": [None, False, ["CoRef", "Word"], ["Word"]], #CoRefWord
        # # "CoRef (SPO)": ['CorefSpo', False, ["Spo"], ["Spo"]],
        # # "Token-to-Keyword": ['TokenToKeyword', ["Word"], ["Taxonomy"]],
        # # "Keyword Match-to-Phrase": [None, False, ["Word"], ["Phrase"]],
        # # "Keyword-to-NER": ['KeywordToNer', False, ["Phrase"], ["Ner"]], #
        # # "Parse-Phrase": ['ParsePhrase', False, ["Phrase"], ["Word"]],
        # # "Parse-List": [None, False, ["Phrase"], ["Phrase"]],
        # # "R^P": [None, True, ["Word"], ["Phrase"]],
        # # "R^T": ["RT", True, ["Word", "Pos", "Dep", "CoRef"], ["Spo"]], # RT
        # # "Expand REL Terms": [None, False ,["Phrase"], ["Rel"]],
        # # "R^E": [None, True, ["Spo"], ["Ner"]],  # 'RE'
        # # "QA-1 (Phrase)": [None, False, ["Ner"], ["Phrase"]],   #'Qa1Phrase'
        # # "QA-1 (NER)": [None, True, ["Ner"], ["Ner"]],     #'Qa1Ner'
        # # "QA-1 (REL)": [None, True, ["Ner"], ["Rel"]],
        # # "QA-2 (NER)": [None, True, ["Ner"], ["Ner"]],
        # # "QA-2 (Phrase)": [None, True, ["Ner"], ["Phrase"]],
        # # "QA-2 (REL)": [None, True, ["Rel", "Ner"], ["Ner"]],
        # # "NER-to-REL": [None, True, ["Ner", "Rel"], ["Ner"]],
        # # "Text-to-Phrase": [None, True, ['CoRef','Dep'], ['Phrase']], #TextToPhrase
    }


    # def __repr__(self):
    #     return '(KsDB) ID: {}, Name: {}, PyName: {}, Grpup: {}, Input level: {}, Output level: {}'.format(
    #         self.inst_id, self.name, self.py_name, self.group_input_levels, self.inputs, self.outputs)

    @classmethod
    def initialize_ks_db(cls):
        """ Initialize knowledge source schema.

        :param this_db: database object
        :return:
        """

        with smile:
            for ks_name in cls.ALL_KS_FORMATS.keys():
                cls.initialize_ks(ks_name)

    @classmethod
    def initialize_ks(cls, ks_name):
        fields = cls.ALL_KS_FORMATS[ks_name]
        py_name = fields[0]
        group_input = fields[1]
        input_levels = fields[2]
        output_levels = fields[3]
        print(ks_name, "\t\t", py_name, "\t", group_input, "\t", input_levels, "\t", output_levels)

        print(cls)
        ks_query = cls(inst_id=encode_inst(f"{ks_name}_{py_name}"))
        ks_query.name=ks_name
        ks_query.py_name=py_name
        ks_query.group_input=group_input
        # ks_query.save()
        for j, input_level in enumerate(input_levels):
            ks_query.inputs = input_level
            ks_input_query = KsInput(keep_db_in_synch=True)
            ks_input_query.ks=ks_query.id
            ks_input_query.data_level=input_level
            # ks_input_query.save()
        for k, output_level in enumerate(output_levels):
            ks_query.outputs = output_level
            ks_output_query = KsOutput(keep_db_in_synch=True)
            ks_output_query.ks=ks_query.id
            ks_output_query.data_level=output_level
            # ks_output_query.save()
        # ks_query.save()

