#!/usr/bin/env python3
"""
ScholarAI Folder Reorganization Script
Automatically reorganizes the project structure for better maintainability
"""

import os
import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# New directory structure
NEW_DIRS = [
    "config/environments",
    "config/docker",
    "config/nginx",
    "config/monitoring",
    "config/database",
    "data/raw",
    "data/processed",
    "data/vector_stores",
    "data/uploads",
    "data/databases",
    "docs/guides",
    "docs/architecture",
    "docs/estimates",
    "scripts/setup",
    "scripts/operations",
    "scripts/data",
    "src/api/routes",
    "src/core/vector_stores",
    "src/utils",
    "tests/unit",
    "tests/integration",
    "tests/performance",
    "tests/examples",
]

# File movements: (source, destination)
FILE_MOVES = [
    # Documentation
    ("CLIENT_FRIENDLY_BREAKDOWN.md", "docs/estimates/cost-breakdown.md"),
    ("COMPREHENSIVE_BREAKDOWN.md", "docs/estimates/comprehensive-breakdown.md"),
    ("DEV-README.md", "docs/guides/development-guide.md"),
    ("LLM_COST_COMPARISON.md", "docs/estimates/llm-cost-comparison.md"),
    ("MANUAL_SETUP.md", "docs/guides/manual-setup.md"),
    ("PROJECT_ESTIMATES.md", "docs/estimates/project-estimates.md"),
    ("docs/deployment-guide.md", "docs/guides/deployment-guide.md"),
    ("docs/development-deployment.md", "docs/guides/development-deployment.md"),
    ("docs/testing.md", "docs/guides/testing-guide.md"),
    
    # Docker & Config
    ("docker-compose.dev.yml", "config/docker/docker-compose.dev.yml"),
    ("docker-compose.prod.yml", "config/docker/docker-compose.prod.yml"),
    ("docker-compose.yml", "config/docker/docker-compose.yml"),
    ("Dockerfile", "config/docker/Dockerfile"),
    (".env.dev.template", "config/environments/.env.dev.template"),
    (".env.local.template", "config/environments/.env.local.template"),
    (".env.prod.template", "config/environments/.env.prod.template"),
    
    # Monitoring configs
    ("monitoring/prometheus.yml", "config/monitoring/prometheus.yml"),
    ("monitoring/loki-config.yml", "config/monitoring/loki-config.yml"),
    ("monitoring/promtail-config.yml", "config/monitoring/promtail-config.yml"),
    
    # Nginx
    ("nginx/nginx.conf", "config/nginx/nginx.conf"),
    
    # Database
    ("config/init.sql", "config/database/init.sql"),
    
    # Scripts - Setup
    ("scripts/setup-dev.sh", "scripts/setup/setup-dev.sh"),
    ("scripts/setup-dev.bat", "scripts/setup/setup-dev.bat"),
    ("scripts/setup-prod.sh", "scripts/setup/setup-prod.sh"),
    ("scripts/setup-prod.bat", "scripts/setup/setup-prod.bat"),
    ("scripts/setup-local.sh", "scripts/setup/setup-local.sh"),
    ("scripts/setup-local.bat", "scripts/setup/setup-local.bat"),
    
    # Scripts - Operations
    ("scripts/backup.sh", "scripts/operations/backup.sh"),
    ("scripts/backup.bat", "scripts/operations/backup.bat"),
    ("scripts/scale.sh", "scripts/operations/scale.sh"),
    ("scripts/scale.bat", "scripts/operations/scale.bat"),
    ("scripts/health-check.sh", "scripts/operations/health-check.sh"),
    ("scripts/health-check.bat", "scripts/operations/health-check.bat"),
    
    # Scripts - Data
    ("check_documents.py", "scripts/data/check_documents.py"),
    ("compare_rag.py", "scripts/data/compare_rag.py"),
    ("load_documents.py", "scripts/data/load_documents.py"),
    ("process_and_load.py", "scripts/data/process_and_load.py"),
    ("setup_local.py", "scripts/setup/setup_local.py"),
    
    # Tests
    ("test_cocubes.py", "tests/examples/test_cocubes.py"),
    ("test_openai_key.py", "tests/examples/test_openai_key.py"),
    ("test_placement_examples.py", "tests/examples/test_placement_examples.py"),
    ("test_rag_only.py", "tests/examples/test_rag_only.py"),
    ("test_server.py", "tests/examples/test_server.py"),
    ("test_with_without_rag.py", "tests/examples/test_with_without_rag.py"),
    
    # Data
    ("scholarai.db", "data/databases/scholarai.db"),
    ("processed_data/documents.json", "data/processed/documents.json"),
    
    # Core refactoring
    ("src/core/simple_embeddings.py", "src/utils/embeddings.py"),
    ("src/core/chroma_vector_store.py", "src/core/vector_stores/chroma_store.py"),
    ("src/core/vector_store.py", "src/core/vector_stores/base.py"),
]

# Directory movements
DIR_MOVES = [
    ("chroma_db", "data/vector_stores/chroma"),
    ("data/uploads", "data/uploads"),
    ("data/Cocubes-20251221T133352Z-1-001/Cocubes", "data/raw/cocubes"),
    ("data/Mphasis-20251221T133359Z-1-001/Mphasis", "data/raw/mphasis"),
    ("data/Valuelabs-20251221T133404Z-1-001/Valuelabs", "data/raw/valuelabs"),
    ("data/ZenQ-20251221T133409Z-1-001/ZenQ", "data/raw/zenq"),
    ("nginx/ssl", "config/nginx/ssl"),
    ("monitoring/grafana", "config/monitoring/grafana"),
]

# Files to remove (duplicates/obsolete)
FILES_TO_REMOVE = [
    "minimal_api.py",
    "run_local.py",
    "run_minimal.py",
    "simple_server.py",
    "start_server.py",
    "src/core/rag_engine_fixed.py",
    "src/core/rag_engine_simple.py",
    "src/core/simple_rag_engine.py",
    "src/core/simple_vector_store.py",
]

def create_directories():
    """Create new directory structure"""
    print("Creating new directory structure...")
    for dir_path in NEW_DIRS:
        full_path = BASE_DIR / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {dir_path}")

def move_files():
    """Move files to new locations"""
    print("\nMoving files...")
    for src, dst in FILE_MOVES:
        src_path = BASE_DIR / src
        dst_path = BASE_DIR / dst
        
        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            print(f"  ✓ Moved: {src} → {dst}")
        else:
            print(f"  ⚠ Skipped (not found): {src}")

def move_directories():
    """Move directories to new locations"""
    print("\nMoving directories...")
    for src, dst in DIR_MOVES:
        src_path = BASE_DIR / src
        dst_path = BASE_DIR / dst
        
        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            if dst_path.exists():
                shutil.rmtree(dst_path)
            shutil.move(str(src_path), str(dst_path))
            print(f"  ✓ Moved: {src} → {dst}")
        else:
            print(f"  ⚠ Skipped (not found): {src}")

def remove_obsolete_files():
    """Remove duplicate and obsolete files"""
    print("\nRemoving obsolete files...")
    for file_path in FILES_TO_REMOVE:
        full_path = BASE_DIR / file_path
        if full_path.exists():
            os.remove(full_path)
            print(f"  ✓ Removed: {file_path}")
        else:
            print(f"  ⚠ Already removed: {file_path}")

def cleanup_empty_dirs():
    """Remove empty directories"""
    print("\nCleaning up empty directories...")
    for root, dirs, files in os.walk(BASE_DIR, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"  ✓ Removed empty: {dir_path.relative_to(BASE_DIR)}")
            except:
                pass

def create_init_files():
    """Create __init__.py files for Python packages"""
    print("\nCreating __init__.py files...")
    python_dirs = [
        "src/api/routes",
        "src/core/vector_stores",
        "src/utils",
        "tests/unit",
        "tests/integration",
        "tests/performance",
        "tests/examples",
    ]
    
    for dir_path in python_dirs:
        init_file = BASE_DIR / dir_path / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            print(f"  ✓ Created: {dir_path}/__init__.py")

def update_gitignore():
    """Update .gitignore with new structure"""
    print("\nUpdating .gitignore...")
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
scholarai_env/
venv/
ENV/

# Environment
.env
.env.local

# Data
data/raw/
data/processed/
data/vector_stores/
data/uploads/
data/databases/*.db

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml

# Monitoring
config/monitoring/grafana/data/

# Temporary
*.tmp
*.bak
"""
    
    gitignore_path = BASE_DIR / ".gitignore"
    with open(gitignore_path, "w") as f:
        f.write(gitignore_content)
    print("  ✓ Updated .gitignore")

def main():
    """Main reorganization process"""
    print("=" * 60)
    print("ScholarAI Folder Reorganization")
    print("=" * 60)
    
    response = input("\nThis will reorganize your project structure. Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    try:
        create_directories()
        move_files()
        move_directories()
        remove_obsolete_files()
        cleanup_empty_dirs()
        create_init_files()
        update_gitignore()
        
        print("\n" + "=" * 60)
        print("✓ Reorganization completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review the changes")
        print("2. Update import statements in Python files")
        print("3. Update docker-compose file paths")
        print("4. Test the application")
        print("5. Commit the changes")
        
    except Exception as e:
        print(f"\n✗ Error during reorganization: {e}")
        print("Please review and fix manually.")

if __name__ == "__main__":
    main()
