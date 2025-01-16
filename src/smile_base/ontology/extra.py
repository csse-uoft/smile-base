from owlready2 import ObjectProperty, DataProperty, AnnotationProperty, rdfs, ConstrainedDatatype, Thing, Property

from owlready2 import default_world, onto_path
onto_path.append('input/ontology_cache/')
from py2graphdb.config import config as CONFIG
smile = default_world.get_ontology(CONFIG.NM)
rdf_nm =  default_world.get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

# Misc
class hasUUID(DataProperty):
    rdfs.comment = ["UUID for the object, if applicable"]
    range = [str]

# Trace
class hasTraceID(ObjectProperty):
    rdfs.comment = ["Trace this object belongs to."]
    range = [Thing]
    pyrange = ['smile.Trace']
    pydomain = ['smile.Hypothesis', 'smile.KSAR']

# Request
class hasRequest(ObjectProperty):
    rdfs.comment = ["Request for this object."]
    range = [Thing]
    pydomain = ['smile.Request']


# KSAR + Hypothesis
class inputForKSARs(ObjectProperty):
    rdfs.comment = ["KS Instance input for this object."]
    range = [Thing]
    pydomain = ['smile.Hypothesis']
    pyrange = ['smile.KSAR']

class hasInputHypotheses(ObjectProperty):
    rdfs.comment = ["Holds Input Hypotheses objects captured by this object."]
    range = [Thing]
    inverse_property = inputForKSARs
    pydomain = ['smile.KSAR']
    pyrange = ['smile.Hypothesis']

class outputOfKSARs(ObjectProperty):
    rdfs.comment = ["KS Instance for this object."]
    range = [Thing]
    pydomain = ['smile:Hypothesis']
    pyrange = ['smile.KSAR']

class hasOutputHypotheses(ObjectProperty):
    rdfs.comment = ["Holds Input Hypotheses objects captured by this object."]
    range = [Thing]
    inverse_property = outputOfKSARs
    pydomain = ['smile.KSAR']
    pyrange = ['smile.Hypothesis']

# KSAR
class hasKSARStatus(DataProperty):
    rdfs.comment = ["Status for this KS Instance object."]
    range = [int]
    pydomain = ['smile.KSAR']

class hasKSObjectPicklePath(DataProperty):
    rdfs.comment = ["Holds pickle version of KnowledgeSource object for this KS Instance object."]
    range = [str]
    pydomain = ['smile.KSAR']

class hasCycle(DataProperty):
    rdfs.comment = ["Holds cycle number for this KS Instance object."]
    range = [int]
    pydomain = ['smile.KSAR']


class hasTriggerDescription(DataProperty):
    rdfs.comment = ["Trigger description for this KS Instance object."]
    range = [str]
    pydomain = ['smile.KSAR']


# Ks + KSAR
class hasKSARs(ObjectProperty):
    rdfs.comment = ["KS Instances for this object."]
    range = [Thing]
    pydomain = ['smile.Ks']
    pyrange = ['smile.KSAR']

class hasKS(ObjectProperty):
    rdfs.comment = ["KS for this object."]
    range = [Thing]
    inverse_property = hasKSARs
    pydomain = ['smile.KSAR']
    pyrange = ['smile.Ks']

# Ks
class hasName(DataProperty):
    rdfs.comment = ["Name for this object."]
    range = [str]
    pydomain = ['smile.Ks']

class hasPyName(DataProperty):
    rdfs.comment = ["Python Name for this object."]
    range = [str]
    pydomain = ['smile.Ks']

class isGroupInput(ObjectProperty):
    rdfs.comment = ["Whether it takes group input Levels or not."]
    range = [bool]
    pydomain = ['smile.Ks']

class hasInputDataLevels(ObjectProperty):
    rdfs.comment = ["Input Data Types for this object."]
    range = [Thing]
    pydomain = ['smile.Ks']
    pyrange = ['smile.Hypothesis']

class hasOutputDataLevels(ObjectProperty):
    rdfs.comment = ["Output Data Types for this object."]
    range = [Thing]
    pydomain = ['smile.Ks']
    pyrange = ['smile.Hypothesis']
# Hypothesis
class hasCertainty(DataProperty):
    rdfs.comment = ["Certainty value for this object."]
    range = [float]
    pydomain =['smile.Hypothesis']

class hasHypotheses(ObjectProperty):
    rdfs.comment = ["Hypotheses for this object."]
    range = [Thing]
    pydomain = ['smile.Trace']
    pyrange = ['smile.Hypothesis']

class hasRequests(ObjectProperty):
    rdfs.comment = ["Requets for this object."]
    range = [Thing]

##################
# class hasInputDataType(ObjectProperty):
#     rdfs.comment = ["Input Data Types for this object."]
#     range = [Thing]
#     # domain 

# class hasOutputDataType(ObjectProperty):
#     rdfs.comment = ["Output Data Types for this object."]
#     range = [Thing]

class hasDataLevel(DataProperty):
    rdfs.comment = ["Data Type for this object."]
    range = [str]
    pydomain = ['smile.KsInput', 'smile.KsOutput']

class hasCoRefWord(ObjectProperty):
    rdfs.comment = ["Holds Word that acts as CoRef for Word object."]
    range = [Thing]
    pydomain = ['smile.CoRef']    
    pyrange = ['smile.Word']

class hasRefWord(ObjectProperty):
    rdfs.comment = ["Holds Word that acts as main Word object."]
    range = [Thing]
    pydomain = ['smile.CoRef']    
    pyrange = ['smile.Word']

# Text, Sentence, Phrase, Word
class hasContent(DataProperty):
    rdfs.comment = ["Holds text content for an object."]
    range = [str]
    pydomain =['smile.Text', 'smile.Phrase', 'smile.Word', 'smile.Query']


class hasContentLabel(DataProperty):
    rdfs.comment = ["Holds token label for the text an object."]
    range = [str]
    pyrange = ['smile.Word']

class hasIndex(DataProperty):
    rdfs.comment = ["Holds index of a sentence in Text."]
    range = [int]
    pydomain = ['smile.Sentence']


class hasStart(DataProperty):
    rdfs.comment = ["Holds start index of a token an object."]
    range = [int]
    pyrange = ['smile.Word', 'smile.Sentence', 'smile.Phrase']

class hasEnd(DataProperty):
    rdfs.comment = ["Holds end index of a token an object."]
    range = [int]
    pyrange = ['smile.Word', 'smile.Sentence', 'smile.Phrase']

class inText(ObjectProperty):
    rdfs.comment = ["Points to the text hypothesis this object belongs to."]
    range = [Thing]
    pydomain = ['smile.Text']
    pyrange = ['smile.Word', 'smile.Sentence', 'smile.Phrase']

class hasText(ObjectProperty):
    rdfs.comment = ["Holds Word/Phrase for a Sentence object."]
    range = [Thing]
    inverse_property = inText
    pydomain = ['smile.Word', 'smile.Sentence', 'smile.Phrase']
    pyrange = ['smile.Text']

class inSentence(ObjectProperty):
    rdfs.comment = ["Holds Word/Phrase for a Sentence object."]
    range = [Thing]
    pyrange = ['smile.Sentence']
    pydomain = ['smile.Word', 'smile.Sentence', 'smile.Phrase']

class hasSentence(ObjectProperty):
    rdfs.comment = ["Holds Word/Phrase for a Sentence object."]
    range = [Thing]
    inverse_property = inSentence
    pydomain = ['smile.Text']
    pyrange = ['smile.Sentence']


class hasPhrases(ObjectProperty):
    rdfs.comment = ["Holds Word that acts as main Word object."]
    range = [Thing]
    pyrange = ['smile.Phrase']
    pydomain = ['smile.Word', 'smile.Sentence', 'smile.Text']

class hasPos(ObjectProperty):
    rdfs.comment = ["Holds part-of-speach label for main object."]
    range = [Thing]
    pydomain = ['smile.Word']
    pyrange = ['smile.Pos']

class hasNers(ObjectProperty):
    rdfs.comment = ["Holds Ners for main object."]
    range = [Thing]
    pydomain = ['smile.Phrase']
    pyrange = ['smile.Ner']

class hasConcepts(ObjectProperty):
    rdfs.comment = ["Holds Concepts for main object."]
    range = [Thing]
    pydomain = ['smile.Phrase']
    pyrange = ['smile.Characteristic', 'smile.Code', 'smile.Input', 'smile.LogicModel', 'smile.Organization', 'smile.Outcome', 'smile.Output', 'smile.Program', 'smile.Service', 'smile.Stakeholder', 'smile.BeneficialStakeholder']


class hasKsInput(ObjectProperty):
    rdfs.comment = ["Holds KsInput for main object."]
    range = [Thing]

class hasKsOutput(ObjectProperty):
    rdfs.comment = ["Holds KsOutput for main object."]
    range = [Thing]

class hasDepLabel(DataProperty):
    rdfs.comment = ["Holds dependency edge label for main object."]
    range = [str]
    pydomain = ['smile.Dep']

class hasSubjectWord(ObjectProperty):
    rdfs.comment = ["Holds Subject Word for main object."]
    range = [Thing]
    pydomain = ['smile.Dep']
    pyrange = ['smile.Word']

class hasObjectWord(ObjectProperty):
    rdfs.comment = ["Holds Object Word for main object."]
    range = [Thing]
    pydomain = ['smile.Dep']
    pyrange = ['smile.Word']

class hasPhrase(ObjectProperty):
    rdfs.comment = ["Holds Phrase for main object."]
    range = [Thing]
    pyrange = ['smile.Phrase']
    pydomain = ['smile.Ner','smile.Sentence','smile.Word',
               'smile.Characteristic', 'smile.Code', 'smile.Input', 'smile.LogicModel', 'smile.Organization', 'smile.Outcome', 'smile.Output', 'smile.Program', 'smile.Service', 'smile.Stakeholder', 'smile.BeneficialStakeholder']
    
class hasEntity(ObjectProperty):
    rdfs.comment = ["Holds Entity type for main object."]
    range = [str]
    pydomain = ['smile.Ner']

class hasWords(ObjectProperty):
    rdfs.comment = ["Holds Word for main object."]
    range = [Thing]
    pydomain = ['smile.Phrase', 'smile.Pos', 'smile.Sentence']
    pyrange = ['smile.Word']

class hasTag(DataProperty):
    rdfs.comment = ["Holds Tag for main object."]
    range = [str]
    pydomain = ['smile.Pos']


class hasPredOntoRel(DataProperty):
    rdfs.comment = ["Holds RDF Predicate for this tripple's main object."]
    range = [str]
    pydomain = ['smile.Rel']

class hasSubject(ObjectProperty):
    rdfs.comment = ["Holds Subject for main object."]
    range = [Thing]
    pydomain = ['smile.Dep', 'Rel', 'Spo']
    pyrange = ['smile.Word']

class hasObject(ObjectProperty):
    rdfs.comment = ["Holds Object for relation object."]
    range = [Thing]
    pydomain = ['smile.Dep', 'smile.Rel', 'smile.Spo']
    pyrange = ['smile.Word']

class hasPredicate(ObjectProperty):
    rdfs.comment = ["Holds Predicate for relation object."]
    range = [Thing]
    pydomain = ['smile.Rel', 'smile.Spo']
    pyrange = ['smile.Word']

class hasSPO(ObjectProperty):
    rdfs.comment = ["Holds SPO for relation object."]
    range = [Thing]
    pydomain = ['smile.Rel']
    pyrange = ['smile.Spo']

class hasRels(ObjectProperty):
    rdfs.comment = ["Holds Rel objects captured by this object."]
    range = [Thing]
    pyrange = ['smile.Rel']
    pydomain = ['smile.Spo']


class hasKSAR(ObjectProperty):
    rdfs.comment = ["Holds KSAR objects captured by this object."]
    range = [Thing]
    pydomain = ['smile.Ks']
    pyrange = ['smile.KSAR']


class hasOutputHypothesesOrgCertainty(ObjectProperty):
    rdfs.comment = ["Holds original certainty of hypothesis and KSAR."]
    range = [Thing]
    pydomain = ['smile.KSAR']
    pyrange = ['smile.OrgCertainty']

class hasOrgKSAR(ObjectProperty):
    rdfs.comment = ["Holds original certainty of hypothesis and KSAR."]
    range = [Thing]
    pydomain = ['smile.OrgCertainty']
    pyrange = ['smile.KSAR']
    inverse_property = hasOutputHypothesesOrgCertainty

class hasOrgHypothesis(ObjectProperty):
    rdfs.comment = ["Holds original certainty of hypothesis and KSAR."]
    range = [Thing]
    pydomain = ['smile.OrgCertainty']
    pyrange = ['smile.Hypothesis']

class hasOrgCertainty(ObjectProperty):
    rdfs.comment = ["Holds original certainty of hypothesis and KSAR."]
    range = [Thing]
    pydomain = ['smile.OrgCertainty']
    pyrange = ['smile.Hypothesis']
    inverse_property = hasOrgHypothesis

class hasOrgCertaintyValue(DataProperty):
    rdfs.comment = ["Certainty value for this object."]
    range = [float]
    pydomain =['smile.OrgCertainty']

class hasOrgKSAR(ObjectProperty):
    rdfs.comment = ["Holds original certainty of hypothesis and KSAR."]
    range = [Thing]
    pydomain = ['smile.OrgCertainty']
    pyrange = ['smile.KSAR']


class hasInputLevel(ObjectProperty):
    rdfs.comment = ["Holds KSAR objects captured by this object."]
    range = [Thing]

class hasOutputLevel(ObjectProperty):
    rdfs.comment = ["Holds KSAR objects captured by this object."]
    range = [Thing]
