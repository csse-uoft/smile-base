from owlready2 import ObjectProperty, DataProperty, AnnotationProperty, rdfs, ConstrainedDatatype, Thing 

class hasOneStr(DataProperty):
    rdfs.comment = ["Desc for the object"]
    range = [str]

class hasListOfStrs(DataProperty):
    rdfs.comment = ["Desc for the object"]
    range = [str]

class hasOneInt(DataProperty):
    rdfs.comment = ["Desc for the object"]
    range = [int]

class hasListOfInts(DataProperty):
    rdfs.comment = ["Desc for the object"]
    range = [int]

class hasOneURI(ObjectProperty):
    rdfs.comment = ["Desc for the object"]
    range = [Thing]

class hasListOfURIs(ObjectProperty):
    rdfs.comment = ["Desc for the object"]
    range = [Thing]

class hasOneFloat(DataProperty):
    rdfs.comment = ["Desc for the object"]
    range = [float]

class hasListOfFloats(DataProperty):
    rdfs.comment = ["Desc for the object"]
    range = [float]
    

