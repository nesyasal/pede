from pathlib import Path
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.chunker import chunk_markdown
from core.metadata_extractor import ArticleMetadata

md_path = Path('data/markdown/jurnal_random_forest.md')
meta_path = Path('data/metadata/jurnal_random_forest.json')
markdown = md_path.read_text(encoding='utf-8')
meta_data = json.loads(meta_path.read_text(encoding='utf-8'))
article_meta = ArticleMetadata(
    article_id=meta_data.get('article_id',''),
    filename=meta_data.get('filename',''),
    title=meta_data.get('title','Untitled'),
    authors=[a.strip() for a in meta_data.get('authors','').split(',') if a.strip()],
    doi=meta_data.get('doi'),
    journal=meta_data.get('journal'),
    publication_date=meta_data.get('publication_date'),
    total_pages=meta_data.get('total_pages',0),
)

configs = [
    {'chunk_size': 500, 'chunk_overlap': 100},
    {'chunk_size': 750, 'chunk_overlap': 150},
    {'chunk_size': 1000, 'chunk_overlap': 200},
    {'chunk_size': 1250, 'chunk_overlap': 250},
    {'chunk_size': 1500, 'chunk_overlap': 300},
]

results = []
for cfg in configs:
    chunks = chunk_markdown(markdown, article_meta, chunk_size=cfg['chunk_size'], chunk_overlap=cfg['chunk_overlap'])
    lengths = [len(c.content) for c in chunks]
    types = {}
    headers = set()
    for c in chunks:
        types[c.content_type] = types.get(c.content_type, 0) + 1
        headers.add(c.section_header)
    results.append({
        'chunk_size': cfg['chunk_size'],
        'chunk_overlap': cfg['chunk_overlap'],
        'num_chunks': len(chunks),
        'avg_length': round(sum(lengths)/len(lengths),1) if lengths else 0,
        'min_length': min(lengths) if lengths else 0,
        'max_length': max(lengths) if lengths else 0,
        'table_chunks': types.get('table',0),
        'references_chunks': types.get('references',0),
        'figure_chunks': types.get('figure_caption',0),
        'text_chunks': types.get('text',0),
        'unique_sections': len(headers),
    })

print(json.dumps(results, indent=2))
