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
    # domain = Trace
    # range = [Hypothesis, KSAR]

# Request
class hasRequest(ObjectProperty):
    rdfs.comment = ["Request for this object."]
    range = [Thing]
    # domain = [Request]


# KSAR + Hypothesis
class inputForKSARs(ObjectProperty):
    rdfs.comment = ["KS Instance input for this object."]
    range = [Thing]
    # domain = [Hypothesis]
    # range = [KSAR]

class hasInputHypotheses(ObjectProperty):
    rdfs.comment = ["Holds Input Hypotheses objects captured by this object."]
    range = [Thing]
    inverse_property = inputForKSARs
    # domain = [KSAR]
    # range = [Hypothesis]

class outputOfKSARs(ObjectProperty):
    rdfs.comment = ["KS Instance for this object."]
    range = [Thing]
    # domain = [Hypothesis]
    # range = [KSAR]

class hasOutputHypotheses(ObjectProperty):
    rdfs.comment = ["Holds Input Hypotheses objects captured by this object."]
    range = [Thing]
    inverse_property = outputOfKSARs
    # domain = [KSAR]
    # range = [Hypothesis]

# KSAR
class hasKSARStatus(DataProperty):
    rdfs.comment = ["Status for this KS Instance object."]
    range = [int]
    # domain = [KSAR]

class hasKSObjectPicklePath(DataProperty):
    rdfs.comment = ["Holds pickle version of KnowledgeSource object for this KS Instance object."]
    range = [str]
    # domain = [KSAR]

class hasCycle(DataProperty):
    rdfs.comment = ["Holds cycle number for this KS Instance object."]
    range = [int]
    # domain = [KSAR]


class hasTriggerDescription(DataProperty):
    rdfs.comment = ["Trigger description for this KS Instance object."]
    range = [str]
    # domain = [KSAR]


# Ks + KSAR
class hasKSARs(ObjectProperty):
    rdfs.comment = ["KS Instances for this object."]
    range = [Thing]
    # domain = [Ks]
    # range  = [KSAR]

class hasKS(ObjectProperty):
    rdfs.comment = ["KS for this object."]
    range = [Thing]
    inverse_property = hasKSARs
    # domain = [KSAR]
    # range  = [Ks]

# Ks
class hasName(DataProperty):
    rdfs.comment = ["Name for this object."]
    range = [str]
    # domain = [Ks]

class hasPyName(DataProperty):
    rdfs.comment = ["Python Name for this object."]
    range = [str]
    # domain = [Ks]

class isGroupInput(ObjectProperty):
    rdfs.comment = ["Whether it takes group input Levels or not."]
    range = [bool]
    # domain = [Ks]

class hasInputDataLevels(ObjectProperty):
    rdfs.comment = ["Input Data Types for this object."]
    range = [Thing]
    # domain = [Ks]

class hasOutputDataLevels(ObjectProperty):
    rdfs.comment = ["Output Data Types for this object."]
    range = [Thing]
    # domain = [Ks]

# Hypothesis
class hasCertainty(DataProperty):
    rdfs.comment = ["Certainty value for this object."]
    range = [float]
    # domain Hypothesis

class hasHypotheses(ObjectProperty):
    rdfs.comment = ["Hypotheses for this object."]
    range = [Thing]
    # domain = [Trace]
    # range = [Hypothesis]

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


class hasCoRefWord(ObjectProperty):
    rdfs.comment = ["Holds Word that acts as CoRef for Word object."]
    range = [Thing]

class hasRefWord(ObjectProperty):
    rdfs.comment = ["Holds Word that acts as main Word object."]
    range = [Thing]

# Text, Sentence, Phrase, Word
class hasContent(DataProperty):
    rdfs.comment = ["Holds text content for an object."]
    range = [str]
    # domain [Text, Phrase, Word, Query]


class hasContentLabel(DataProperty):
    rdfs.comment = ["Holds token label for the text an object."]
    range = [str]

class hasIndex(DataProperty):
    rdfs.comment = ["Holds index of a sentence in Text."]
    range = [int]


class hasStart(DataProperty):
    rdfs.comment = ["Holds start index of a token an object."]
    range = [int]
class hasEnd(DataProperty):
    rdfs.comment = ["Holds end index of a token an object."]
    range = [int]

class inText(ObjectProperty):
    rdfs.comment = ["Points to the text hypothesis this object belongs to."]
    range = [Thing]

class hasText(ObjectProperty):
    rdfs.comment = ["Holds Word/Phrase for a Sentence object."]
    range = [Thing]
    inverse_property = inText

class inSentence(ObjectProperty):
    rdfs.comment = ["Holds Word/Phrase for a Sentence object."]
    range = [Thing]

class hasSentence(ObjectProperty):
    rdfs.comment = ["Holds Word/Phrase for a Sentence object."]
    range = [Thing]
    inverse_property = inSentence


class hasPhrases(ObjectProperty):
    rdfs.comment = ["Holds Word that acts as main Word object."]
    range = [Thing]

class hasPos(ObjectProperty):
    rdfs.comment = ["Holds part-of-speach label for main object."]
    range = [Thing]

class hasNers(ObjectProperty):
    rdfs.comment = ["Holds Ners for main object."]
    range = [Thing]

class hasConcepts(ObjectProperty):
    rdfs.comment = ["Holds Concepts for main object."]
    range = [Thing]


class hasKsInput(ObjectProperty):
    rdfs.comment = ["Holds KsInput for main object."]
    range = [Thing]

class hasKsOutput(ObjectProperty):
    rdfs.comment = ["Holds KsOutput for main object."]
    range = [Thing]

class hasDepLabel(DataProperty):
    rdfs.comment = ["Holds dependency edge label for main object."]
    range = [str]

class hasSubjectWord(ObjectProperty):
    rdfs.comment = ["Holds Subject Word for main object."]
    range = [Thing]

class hasObjectWord(ObjectProperty):
    rdfs.comment = ["Holds Object Word for main object."]
    range = [Thing]

class hasPhrase(ObjectProperty):
    rdfs.comment = ["Holds Phrase for main object."]
    range = [Thing]

class hasEntity(ObjectProperty):
    rdfs.comment = ["Holds Entity type for main object."]
    range = [str]

class hasWords(ObjectProperty):
    rdfs.comment = ["Holds Word for main object."]
    range = [Thing]

class hasTag(DataProperty):
    rdfs.comment = ["Holds Tag for main object."]
    range = [str]


class hasPredOntoRel(DataProperty):
    rdfs.comment = ["Holds RDF Predicate for this tripple's main object."]
    range = [str]

class hasSubject(ObjectProperty):
    rdfs.comment = ["Holds Subject for main object."]
    range = [Thing]

class hasObject(ObjectProperty):
    rdfs.comment = ["Holds Object for relation object."]
    range = [Thing]

class hasPredicate(ObjectProperty):
    rdfs.comment = ["Holds Predicate for relation object."]
    range = [Thing]

class hasSPO(ObjectProperty):
    rdfs.comment = ["Holds SPO for relation object."]
    range = [Thing]

class hasRels(ObjectProperty):
    rdfs.comment = ["Holds Rel objects captured by this object."]
    range = [Thing]


class hasKSAR(ObjectProperty):
    rdfs.comment = ["Holds KSAR objects captured by this object."]
    range = [Thing]

class hasInputLevel(ObjectProperty):
    rdfs.comment = ["Holds KSAR objects captured by this object."]
    range = [Thing]

class hasOutputLevel(ObjectProperty):
    rdfs.comment = ["Holds KSAR objects captured by this object."]
    range = [Thing]
