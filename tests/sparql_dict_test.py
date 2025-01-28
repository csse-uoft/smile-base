from py2graphdb.config import config as CONFIG
from ..app.scripts.misc_lib import *
import tqdm

import os
LOG_FILE = CONFIG.LOG_DIR+f"logging_{CONFIG.RUN_LABEL}.txt"    # Log file used to log errors or warnings that should not stop the processing (e.g. invalid address is found)
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

from owlready2 import default_world, onto_path, Thing
onto_path.append('input/ontology_cache/')

smile = default_world.get_ontology(CONFIG.NM)
rdf_nm =  default_world.get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

CONFIG.STORE_LOCAL = False

TESTS_N = 18
TEST_I = 0

from owlready2.prop import DataProperty, rdfs
with smile:

    class TestThing(Thing):
        pass

    class title(DataProperty):
        rdfs.comment = ["Title for the object"]
        range = [str]

    class desc(DataProperty):
        rdfs.comment = ["Desc for the object"]
        range = [str]


with smile:
    from pprint import pprint
    import re, hashlib
    import numpy as np
    from .db_utils import global_db
    from .db_utils import escape_str, get_instance, get_blank_instance, logger, global_db, \
        global_db_indexed, update_db_index, PropertyList, ObjectDict, get_instance_label, row_to_turtle, \
        smile, rdf_nm, resolve_nm_for_ttl, ObjectDict, PropertyList, encode_inst,\
        SPARQLDict
    print()

test_name = os.path.basename(__file__).rpartition(r'.')[0]
p_bar = tqdm.tqdm(range(TESTS_N), desc=f"Tests{test_name.rjust(20)}")

with smile:
    rr = np.random.rand()
    inst = SPARQLDict._add(klass=smile.TestThing, props={smile.title:'My TestThing', smile.desc:f"this is my trace ({rr})."})
    inst_id1 = inst['ID']

    inst = SPARQLDict._get(klass=smile.TestThing, props={smile.title:'My TestThing', smile.desc:f"this is my trace ({rr})."})
    inst_id2 = inst['ID']
    assert inst_id1 == inst_id2
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = np.random.rand()
    inst = SPARQLDict._add(klass=smile.TestThing, props={smile.title:'My TestThing', smile.desc:f"this is my trace ({rr})."})
    inst_id1 = inst['ID']

    inst = SPARQLDict._get(klass=smile.TestThing, props={smile.title:'My TestThing', smile.desc:f"this is my trace ({rr})."})
    inst_id2 = inst['ID']
    assert inst_id1 == inst_id2
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = np.random.rand()
    inst = SPARQLDict._add(klass=smile.TestThing, props={smile.title:'My TestThing', smile.desc:f"this is my trace ({rr})."})
    inst_id3 = inst['ID']
    assert inst_id1 != inst_id3
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = np.random.rand()
    inst = SPARQLDict._get(klass=smile.TestThing, props={smile.title:'My TestThing', smile.desc:f"this is my trace ({rr})."})
    assert inst is None
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = f"{int(np.random.rand()*10**10)}"
    inst = SPARQLDict._get(klass=smile.TestThing, inst_id = str(rr))
    assert inst is None
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    inst = SPARQLDict._add(klass=smile.TestThing)
    assert 'ID' in inst.keys()
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = f"{int(np.random.rand()*10**10)}"
    inst = SPARQLDict._add(klass=smile.TestThing, inst_id = str(rr))
    assert inst['ID'] == f"smile.{rr}"
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    rr1 = str(int(np.random.rand()*10**10))
    rr2 = f"smile.{rr1}"
    rr3 = resolve_nm_for_ttl(rr2)
    assert f"smile:{rr1}" == rr3
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr1 = str(int(np.random.rand()*10**10))
    rr2 = resolve_nm_for_ttl(rr1)
    assert f"smile:{rr1}" == rr2
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = str(int(np.random.rand()*10**10))
    props = {smile.title:'my new title', smile.desc:f"My desc with {rr}"}
    inst_id = str(int(np.random.rand()*10**10))
    inst_add = SPARQLDict._add(klass=smile.TestThing, inst_id=inst_id, props=props)
    inst_get = SPARQLDict._get(klass=smile.TestThing, inst_id=inst_id)
    assert inst_add == inst_get
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr1 = str(int(np.random.rand()*10**10))
    props = {smile.title:['my new title 1', 'my title 2'], smile.desc:[f"My desc with {rr1}"]}
    rr2 = str(int(np.random.rand()*10**10))
    inst_id = rr2
    inst_add = SPARQLDict._add(klass=smile.TestThing, inst_id=inst_id, props=props)
    inst_id = f"smile.{rr2}"
    inst_get = SPARQLDict._get(klass=smile.TestThing, inst_id=inst_id)
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr1 = str(int(np.random.rand()*10**10))
    props = {smile.title:['my new title 1', 'my title 2'], smile.desc:[f"My desc with {rr1}"]}
    rr2 = str(int(np.random.rand()*10**10))
    inst_id = rr2
    inst_add = SPARQLDict._add(klass=smile.TestThing, inst_id=inst_id, props=props)
    # inst_id = inst_add['ID']
    inst_id = f"smile.{rr2}"
    # inst_get = SPARQLDict._get(klass=smile.TestThing, inst_id=inst_id)
    updated_props = props.copy()
    updated_props[smile.title] = ['my new title 1']
    inst_updated = SPARQLDict._update(klass=smile.TestThing,inst_id=inst_id, drop=updated_props)
    assert inst_updated[smile.title] == ['my title 2']
    assert smile.desc not in inst_updated.keys()
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr1 = str(int(np.random.rand()*10**10))
    props = {smile.title:['my new title 1', 'my title 2'], smile.desc:[f"My desc with {rr1}"]}
    rr2 = str(int(np.random.rand()*10**10))
    inst_id = rr2
    inst_add = SPARQLDict._add(klass=smile.TestThing, inst_id=inst_id, props=props)
    inst_id = inst_add['ID']
    inst_id = f"smile.{rr2}"
    updated_props = props.copy()
    updated_props = {smile.title: ['my title 3', 'my title 4']}
    inst_updated = SPARQLDict._update(klass=smile.TestThing,inst_id=inst_id, add=updated_props)
    assert 4 == len([t for t in inst_updated[smile.title] if t in ['my new title 1', 'my title 2', 'my title 3', 'my title 4']])
    assert inst_updated[smile.desc] == [f"My desc with {rr1}"]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


with smile:
    rr = np.random.rand()
    inst = SPARQLDict._add(klass=smile.TestThing, props={smile.title:None, smile.desc:f"this is my trace ({rr})."})
    inst_id = inst['ID']
    inst2 = SPARQLDict._add(klass=smile.TestThing, inst_id=inst_id)
    assert smile.title not in inst2.keys()
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = np.random.rand()
    inst = SPARQLDict._add(klass=smile.TestThing, props={smile.title:None, smile.desc:f"this is my trace ({rr})."})
    inst_id = inst['ID']
    inst2 = SPARQLDict._add(klass=smile.TestThing, inst_id=inst_id)
    assert list(inst2.keys()) == ['ID', 'is_a', smile.desc, smile.hasUUID]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = np.random.rand()
    inst = SPARQLDict._add(klass=smile.TestThing, props={smile.title:["My title"], smile.desc:f"this is my trace ({rr})."})
    inst_id = inst['ID']
with smile:
    inst2 = SPARQLDict._update(klass=smile.TestThing, inst_id=inst_id, drop={smile.title:["My title"]})
    assert list(inst2.keys()) == ['ID', 'is_a', smile.desc, smile.hasUUID]
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = np.random.rand()
    inst = SPARQLDict._add(klass=smile.TestThing, props={smile.title:["My title"], smile.desc:f"this is my trace ({rr})."})
    inst_id = inst['ID']
    new_props = {smile.title:['My NEW Title'], smile.desc:f"this is my NEW trace ({rr})."}
    inst2 = SPARQLDict._update(klass=smile.TestThing, inst_id=inst_id, add=new_props)
    assert list(inst2.keys()) == ['ID', 'is_a', smile.desc, smile.hasUUID, smile.title]
    assert len(inst2[smile.desc])==2
    assert len(inst2[smile.title])==2
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()

with smile:
    rr = np.random.rand()
    inst = SPARQLDict._add(klass=smile.TestThing, props={smile.title:["My title"], smile.desc:f"this is my trace ({rr})."})
    inst_id = inst['ID']
    new_props = {smile.title:['My NEW Title 1','My NEW Title 2' ], smile.desc:[f"this is my NEW trace ({rr}).", "A NEW desc #2"]}
    inst2 = SPARQLDict._update(klass=smile.TestThing, inst_id=inst_id, new=new_props)
    assert list(inst2.keys()) == ['ID', 'is_a', smile.desc, smile.hasUUID, smile.title]
    assert 'My NEW Title 2' in inst2[smile.title] and 'My NEW Title 1' in inst2[smile.title]
    assert len(inst2[smile.title]) == 2
    assert "A NEW desc #2" in inst2[smile.desc] and f"this is my NEW trace ({rr})." in inst2[smile.desc]
    assert len(inst2[smile.desc]) == 2
    p_bar.n = TEST_I = TEST_I + 1
    p_bar.refresh()


assert TESTS_N == TEST_I

print("\n\n")

