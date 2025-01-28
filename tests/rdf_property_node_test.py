# from py2graphdb.config import config as CONFIG
from py2graphdb.config import config as CONFIG
from py2graphdb.utils.misc_lib import *
import tqdm, os

from owlready2 import default_world, onto_path
onto_path.append('input/ontology_cache/')

smile = default_world.get_ontology(CONFIG.NM)
rdf_nm =  default_world.get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

CONFIG.STORE_LOCAL = False

LOG_FILE = CONFIG.LOG_DIR+f"logging_{CONFIG.RUN_LABEL}.txt"    # Log file used to log errors or warnings that should not stop the processing (e.g. invalid address is found)
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

TESTS_N = 9
TEST_I = 0
from owlready2.entity import ThingClass

with smile:
    from pprint import pprint
    import re, hashlib
    import numpy as np
    from src.smile_base.Model.data_level.rdf_property import RDFProperty, SPARQLDict
    from src.smile_base.Model.controller.trace import Trace
    print()

test_name = os.path.basename(__file__).rpartition(r'.')[0]
p_bar = tqdm.tqdm(range(TESTS_N), desc=f"Tests{test_name.rjust(20)}")

# assert False
with smile:
    trace = Trace.generate()
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    rr3 = f"{int(np.random.rand()*10**10)}"
    test_inst0 = RDFProperty()
    test_inst0.subject = rr1
    test_inst0.predicate = rr2
    test_inst0.object = rr3
    assert test_inst0._subject == f"smile.{rr1}"
    assert test_inst0._predicate == f"smile.{rr2}"
    assert test_inst0._object == f"smile.{rr3}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test certainty property
    test_inst0 = RDFProperty()
    test_inst0.certainty = 0.123
    test_inst0.certainty = 0.456
    assert test_inst0._certainty == 0.456
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    # test Hypothesis.find on null
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    rr3 = f"{int(np.random.rand()*10**10)}"
    node = RDFProperty.find(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    assert node is None
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.generate then find on conent
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    rr3 = f"{int(np.random.rand()*10**10)}"
    node_add = RDFProperty.generate(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    node_found = RDFProperty.find(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    inst = SPARQLDict._get(klass="smile.RDFProperty", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_add.trace == inst[smile.hasTraceID][0]
    assert node_add.trace == f"smile.{rr}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()



with smile:
    # test Hypothesis.generate then find on content_label
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    rr3 = f"{int(np.random.rand()*10**10)}"
    node_add = RDFProperty.generate(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    node_found = RDFProperty.find(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    inst = SPARQLDict._get(klass="smile.RDFProperty", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_add.subject == node_found.subject
    assert node_add.predicate == node_found.predicate
    assert node_add.object == node_found.object
    assert node_add.trace == inst[smile.hasTraceID][0]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.generate then find on start and end
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    rr3 = f"{int(np.random.rand()*10**10)}"
    node_add = RDFProperty.generate(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    node_found = RDFProperty.find(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    inst = SPARQLDict._get(klass="smile.RDFProperty", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_add.subject == node_found.subject
    assert node_add.predicate == node_found.predicate
    assert node_add.object == node_found.object
    assert node_add.trace == inst[smile.hasTraceID][0]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.find_generate on new
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    rr3 = f"{int(np.random.rand()*10**10)}"
    node_add = RDFProperty.find(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    node_found = RDFProperty.find_generate(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    inst = SPARQLDict._get(klass="smile.RDFProperty", inst_id=node_found.inst_id)

    assert node_add is None
    assert node_found.inst_id == inst['ID']
    assert node_found.subject == f"smile.{rr1}"
    assert node_found.predicate == f"smile.{rr2}"
    assert node_found.object == f"smile.{rr3}"
    assert node_found.trace == inst[smile.hasTraceID][0]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    # test Hypothesis.find_generate on existing
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    rr3 = f"{int(np.random.rand()*10**10)}"
    node_add = RDFProperty.generate(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    node_found = RDFProperty.find_generate(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    inst = SPARQLDict._get(klass="smile.RDFProperty", inst_id=node_add.inst_id)

    assert node_add.inst_id == node_found.inst_id
    assert node_found.inst_id == inst['ID']
    assert node_found.trace == inst[smile.hasTraceID][0]
    assert node_found.trace == f"smile.{rr}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = f"{int(np.random.rand()*10**10)}"
    rr1 = f"{int(np.random.rand()*10**10)}"
    rr2 = f"{int(np.random.rand()*10**10)}"
    rr3 = f"{int(np.random.rand()*10**10)}"
    node_add = RDFProperty.generate(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    node_found = RDFProperty.find_generate(trace_id=rr, subject_id=rr1, predicate_id=rr2, object_id=rr3)
    inst = SPARQLDict._get(klass="smile.RDFProperty", inst_id=node_add.inst_id)
    hypo = RDFProperty()
    hypo.inst_id = inst['ID']
    hypo.load()
    key_show = f"RDFProperty_{hypo.inst_id}"
    key = int(hashlib.sha256(key_show.encode('utf-8')).hexdigest(), 16) % 10**8
    assert node_add.key_show() == key_show
    assert node_add.key() == key
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

assert TESTS_N == TEST_I

print("\n\n")


