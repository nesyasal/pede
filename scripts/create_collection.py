import os
import sys
# ensure project root is importable when running this script directly
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)
os.chdir(project_root)

from core.vector_store import VectorStore

vs = VectorStore()
vs.ensure_collection()
print("OK: collection ensured")
import os
os.chdir(r"d:\kuliah\Semester 6\pede")
from core.vector_store import VectorStore

vs = VectorStore()
vs.ensure_collection()
print("OK: collection ensured")
