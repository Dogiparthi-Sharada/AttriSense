#!/usr/bin/env python3
"""
Git repository initialization and commit script
Initializes git, configures user, adds files, and prepares for GitHub push
"""

import os
from git import Repo
from pathlib import Path

def init_and_commit_repo():
    """Initialize git repository and make initial commit"""
    
    repo_path = Path(".")
    
    print("=" * 60)
    print("AttriSense - Git Setup")
    print("=" * 60)
    print()
    
    # Initialize repository
    print("📦 Initializing git repository...")
    if not (repo_path / '.git').exists():
        repo = Repo.init(repo_path)
        print("   ✅ Git repository initialized")
    else:
        repo = Repo(repo_path)
        print("   ℹ️  Git repository already exists")
    
    # Configure git user
    print("\n👤 Configuring git user...")
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "Sharada Dogiparthi").release()
        git_config.set_value("user", "email", "sharada.dogiparthi@github.com").release()
    print("   ✅ Git user configured")
    
    # Add files respecting .gitignore
    print("\n📝 Adding files to staging area...")
    repo.git.add(A=True)
    
    # Get status
    status = repo.git.status(porcelain=True)
    lines = status.split('\n')
    added_count = len([l for l in lines if l])
    print(f"   ✅ Added {added_count} files/changes to staging")
    
    # Create initial commit
    print("\n💾 Creating initial commit...")
    commit_message = """Initial commit: AttriSense

Comprehensive workforce analytics platform with:
- Predictive turnover risk scoring (Random Forest + SMOTE)
- Natural language to SQL translation (GPT-3.5-turbo + LangChain)
- RAG-enhanced exit interview analysis (FAISS vector search)
- Interactive Streamlit dashboard with Plotly visualizations
- Production-ready architecture with SQLite and FAISS backends

Project Structure:
- data_generator.py: Synthetic HR data generation
- predictive_engine.py: ML turnover prediction model
- rag_engine.py: Vector database for exit interviews
- ai_sql_constructor.py: NL-to-SQL AI agent
- dashboard.py: Streamlit web interface
- doc/: Visual architecture and system diagrams
- requirements.txt: Python dependencies

Setup: See QUICKSTART.md
Design: See DESIGN_DECISIONS.md
Architecture: See doc/ folder for diagrams"""
    
    try:
        repo.index.commit(commit_message)
        print("   ✅ Initial commit created")
    except Exception as e:
        print(f"   ⚠️  Commit note: {e}")
    
    # Show repository information
    print("\n" + "=" * 60)
    print("✅ Git Repository Ready!")
    print("=" * 60)
    print(f"\n📍 Repository location: {repo_path.absolute()}")
    print(f"🔧 Remote: Not yet configured")
    print("\n📖 Next Steps:")
    print("   1. Create repository on GitHub:")
    print("      - Go to https://github.com/new")
    print("      - Name: AttriSense")
    print("      - Description: AI-powered workforce analytics platform")
    print("   2. Add remote and push:")
    print("      git remote add origin git@github.com:Dogiparthi-Sharada/AttriSense.git")
    print("      git branch -M main")
    print("      git push -u origin main")
    print("\n" + "=" * 60)
    
    return repo

if __name__ == "__main__":
    try:
        repo = init_and_commit_repo()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
