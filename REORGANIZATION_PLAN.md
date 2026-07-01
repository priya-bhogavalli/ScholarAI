# ScholarAI Folder Reorganization Plan

## Current Issues
1. **Root directory cluttered** - 30+ files in root including test files, setup scripts, and documentation
2. **Duplicate/similar files** - Multiple RAG engines, test files, and setup scripts
3. **Poor separation** - Data, config, and code mixed together
4. **Unclear structure** - Hard to find files and understand project organization

## Proposed New Structure

```
ScholarAI/
├── .github/                          # GitHub workflows and templates
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── config/                           # All configuration files
│   ├── environments/
│   │   ├── .env.dev.template
│   │   ├── .env.local.template
│   │   └── .env.prod.template
│   ├── docker/
│   │   ├── docker-compose.dev.yml
│   │   ├── docker-compose.prod.yml
│   │   └── Dockerfile
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── ssl/
│   ├── monitoring/
│   │   ├── prometheus.yml
│   │   ├── loki-config.yml
│   │   └── promtail-config.yml
│   └── database/
│       └── init.sql
│
├── data/                             # All data files (gitignored)
│   ├── raw/                          # Original uploaded documents
│   │   ├── cocubes/
│   │   ├── mphasis/
│   │   ├── valuelabs/
│   │   └── zenq/
│   ├── processed/                    # Processed documents
│   │   └── documents.json
│   ├── vector_stores/                # Vector database files
│   │   ├── chroma/
│   │   └── qdrant/
│   ├── uploads/                      # Temporary upload directory
│   └── databases/                    # SQLite and other DB files
│       └── scholarai.db
│
├── docs/                             # All documentation
│   ├── README.md                     # Main documentation index
│   ├── guides/
│   │   ├── deployment-guide.md
│   │   ├── development-guide.md
│   │   ├── manual-setup.md
│   │   └── testing-guide.md
│   ├── architecture/
│   │   ├── system-design.md
│   │   └── api-documentation.md
│   └── estimates/
│       ├── project-estimates.md
│       ├── cost-breakdown.md
│       └── llm-cost-comparison.md
│
├── scripts/                          # Operational scripts
│   ├── setup/
│   │   ├── setup-dev.sh
│   │   ├── setup-dev.bat
│   │   ├── setup-prod.sh
│   │   ├── setup-prod.bat
│   │   ├── setup-local.sh
│   │   └── setup-local.bat
│   ├── operations/
│   │   ├── backup.sh
│   │   ├── backup.bat
│   │   ├── scale.sh
│   │   ├── scale.bat
│   │   ├── health-check.sh
│   │   └── health-check.bat
│   ├── data/
│   │   ├── load_documents.py
│   │   └── process_and_load.py
│   └── cli.py                        # Main CLI tool
│
├── src/                              # Source code
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── query.py
│   │       ├── upload.py
│   │       └── health.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── document_processor.py
│   │   ├── rag_engine.py            # Main RAG engine (keep one)
│   │   ├── mock_test_engine.py
│   │   └── vector_stores/
│   │       ├── __init__.py
│   │       ├── base.py
│   │       ├── chroma_store.py
│   │       └── qdrant_store.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── utils/
│       ├── __init__.py
│       ├── embeddings.py
│       └── helpers.py
│
├── tests/                            # All test files
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_document_processor.py
│   │   ├── test_rag_engine.py
│   │   └── test_vector_store.py
│   ├── integration/
│   │   ├── test_api.py
│   │   ├── test_integration.py
│   │   └── test_cli.py
│   ├── performance/
│   │   └── test_performance.py
│   └── examples/
│       ├── test_cocubes.py
│       ├── test_placement_examples.py
│       └── test_with_without_rag.py
│
├── logs/                             # Application logs (gitignored)
│
├── .env                              # Active environment file (gitignored)
├── .gitignore
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── setup.py
└── README.md                         # Main project README
```

## Files to Move/Consolidate

### Root → docs/
- CLIENT_FRIENDLY_BREAKDOWN.md → docs/estimates/cost-breakdown.md
- COMPREHENSIVE_BREAKDOWN.md → docs/estimates/comprehensive-breakdown.md
- DEV-README.md → docs/guides/development-guide.md
- LLM_COST_COMPARISON.md → docs/estimates/llm-cost-comparison.md
- MANUAL_SETUP.md → docs/guides/manual-setup.md
- PROJECT_ESTIMATES.md → docs/estimates/project-estimates.md

### Root → config/
- docker-compose.dev.yml → config/docker/docker-compose.dev.yml
- docker-compose.prod.yml → config/docker/docker-compose.prod.yml
- docker-compose.yml → config/docker/docker-compose.yml
- Dockerfile → config/docker/Dockerfile
- .env.dev.template → config/environments/.env.dev.template
- .env.local.template → config/environments/.env.local.template
- .env.prod.template → config/environments/.env.prod.template

### Root → scripts/
- check_documents.py → scripts/data/check_documents.py
- compare_rag.py → scripts/data/compare_rag.py
- load_documents.py → scripts/data/load_documents.py
- process_and_load.py → scripts/data/process_and_load.py
- setup_local.py → scripts/setup/setup_local.py

### Root → tests/examples/
- test_cocubes.py → tests/examples/test_cocubes.py
- test_openai_key.py → tests/examples/test_openai_key.py
- test_placement_examples.py → tests/examples/test_placement_examples.py
- test_rag_only.py → tests/examples/test_rag_only.py
- test_server.py → tests/examples/test_server.py
- test_with_without_rag.py → tests/examples/test_with_without_rag.py

### Root → data/databases/
- scholarai.db → data/databases/scholarai.db
- chroma_db/ → data/vector_stores/chroma/

### Files to Remove/Consolidate
- minimal_api.py (consolidate into main.py)
- run_local.py (use scripts/setup/setup-local.sh)
- run_minimal.py (remove, use main.py)
- simple_server.py (remove, use main.py)
- start_server.py (remove, use main.py)
- main.py (keep as entry point)

### src/core/ Cleanup
- Keep: rag_engine.py (main implementation)
- Remove: rag_engine_fixed.py, rag_engine_simple.py, simple_rag_engine.py
- Consolidate: simple_embeddings.py → src/utils/embeddings.py
- Consolidate: simple_vector_store.py, chroma_vector_store.py, vector_store.py → src/core/vector_stores/

## Benefits of New Structure

1. **Clear Separation**: Config, code, data, docs, and scripts are clearly separated
2. **Easier Navigation**: Logical grouping makes files easy to find
3. **Better Scalability**: Structure supports growth and new features
4. **Cleaner Root**: Only essential files in root directory
5. **Professional**: Follows industry best practices
6. **Better CI/CD**: Clear structure for automated deployments
7. **Easier Onboarding**: New developers can understand structure quickly

## Migration Steps

1. Create new directory structure
2. Move files to new locations
3. Update import statements in Python files
4. Update docker-compose paths
5. Update documentation references
6. Update .gitignore
7. Test all functionality
8. Remove old/duplicate files
9. Update README with new structure

## Backward Compatibility

- Keep symbolic links for critical files during transition
- Update all documentation with new paths
- Provide migration guide for existing deployments
