# AttriSense - Design Decision Document

## Project Overview
This document outlines the architectural and design decisions made for AttriSense, a comprehensive workforce analytics platform combining predictive modeling, natural language querying, and interactive visualization.

## Core Requirements
- **Predictive Analytics**: Identify employees at risk of voluntary turnover
- **Natural Language Interface**: Allow HR users to query data without SQL knowledge
- **Interactive Dashboard**: Provide intuitive visualization of workforce insights
- **Scalable Data Pipeline**: Handle synthetic data generation to real HR data integration
- **Cost-Effective AI**: Use efficient models for production deployment

## Technology Stack Decisions

### Programming Language: Python
**Decision**: Python as the primary language
**Rationale**:
- Rich ecosystem for data science and machine learning
- Excellent libraries for AI/ML (scikit-learn, LangChain, OpenAI)
- Streamlit for rapid web app development
- Strong community support for HR analytics use cases

### Data Storage: SQLite
**Decision**: SQLite for the primary database
**Rationale**:
- Zero-configuration, file-based database
- Sufficient for enterprise-scale HR data (thousands to millions of records)
- Native Python support via sqlite3
- Easy backup and deployment
- SQL standard compliance for complex queries

### Machine Learning: Random Forest + SMOTE
**Decision**: RandomForestClassifier with SMOTE oversampling
**Rationale**:
- **Random Forest**: Robust, interpretable, handles mixed data types well
- **SMOTE**: Addresses class imbalance in turnover data (typically <10% positive cases)
- Better performance than logistic regression for non-linear relationships
- Feature importance analysis for HR insights

### AI Framework: LangChain + OpenAI GPT-3.5-turbo
**Decision**: LangChain for orchestration, GPT-3.5-turbo for text generation
**Rationale**:
- **LangChain**: Mature framework for LLM applications, SQL chain templates
- **GPT-3.5-turbo**: Cost-effective balance of performance and price
- Temperature=0 for deterministic SQL generation
- Structured prompting prevents hallucination

### Vector Database: FAISS
**Decision**: Facebook AI Similarity Search (FAISS) for RAG
**Rationale**:
- High-performance vector similarity search
- CPU-based (faiss-cpu) for easy deployment
- Integrates well with LangChain embeddings
- Local storage avoids cloud dependency

### Web Framework: Streamlit
**Decision**: Streamlit for the dashboard
**Rationale**:
- Python-native, no HTML/CSS/JS required
- Rapid prototyping and deployment
- Built-in components for data visualization
- Excellent for data science applications

## Data Pipeline Architecture

### Synthetic Data Generation
**Decision**: Custom Python script with numpy.random
**Rationale**:
- Reproducible with fixed random seed
- Business logic injection (e.g., Manufacturing turnover rates)
- Easy modification for different scenarios
- No external data dependencies for demos

### Feature Engineering Approach
**Decision**: Minimal features (Tenure, Salary, Department)
**Rationale**:
- Focus on actionable, interpretable features
- Department encoding via categorical codes
- Avoid overfitting with too many features
- Easy to extend with additional HR metrics

### Risk Categorization
**Decision**: Probability thresholds (0.75 High, 0.40 Medium)
**Rationale**:
- Business-aligned risk levels
- Allows for different intervention strategies
- Intuitive for HR stakeholders
- Adjustable based on organizational tolerance

## Security and Privacy Considerations

### API Key Management
**Decision**: Environment variables via python-dotenv
**Rationale**:
- Keeps sensitive keys out of source code
- Supports different environments (dev/prod)
- Industry standard practice
- Easy rotation and management

### Data Privacy
**Decision**: Synthetic data for development
**Rationale**:
- No real employee data exposure
- Demonstrates system capabilities safely
- Easy to replace with real data pipelines
- Compliance with privacy regulations

## Performance Optimizations

### Model Training
**Decision**: Batch training with SMOTE preprocessing
**Rationale**:
- Handles imbalanced data effectively
- One-time training for prediction serving
- Fast inference for real-time dashboards

### SQL Query Limits
**Decision**: Top-k limiting in prompts
**Rationale**:
- Prevents excessive database load
- Faster response times
- User-focused result sets

### Text Chunking for RAG
**Decision**: 150-character chunks with 20-character overlap
**Rationale**:
- Balances context preservation and granularity
- Fits typical sentence/exit interview length
- Allows semantic search without losing meaning

## Deployment and Operations

### Virtual Environment
**Decision**: venv with requirements.txt equivalent
**Rationale**:
- Isolated dependencies
- Reproducible environments
- Standard Python practice

### Local Execution
**Decision**: Desktop application architecture
**Rationale**:
- No cloud infrastructure required
- Easy for HR teams to run locally
- Faster iteration during development
- Lower cost than cloud deployment

## Future Extensibility

### Modular Architecture
**Decision**: Separate scripts for each pipeline stage
**Rationale**:
- Independent execution and testing
- Easy to modify individual components
- Supports CI/CD pipelines
- Clear separation of concerns

### Configuration-Driven Design
**Decision**: Hardcoded parameters with clear documentation
**Rationale**:
- Easy to understand and modify
- No complex configuration files needed
- Transparent business logic

## Risk Mitigation

### Error Handling
**Decision**: Try-catch blocks with user-friendly messages
**Rationale**:
- Graceful failure for end users
- Debugging information for developers
- Prevents application crashes

### Data Validation
**Decision**: Basic data integrity checks
**Rationale**:
- Ensures pipeline reliability
- Catches data quality issues early
- Maintains system stability

## Success Metrics

### Technical Metrics
- Model accuracy on holdout data
- Query response time (<5 seconds)
- Dashboard load time (<2 seconds)

### Business Metrics
- User adoption of NL-to-SQL interface
- Time savings vs manual SQL queries
- Predictive model lift over baseline

## Conclusion
This design balances technical sophistication with practical deployment constraints, creating a production-ready HR analytics system that can scale from prototype to enterprise use. The modular architecture supports future enhancements while maintaining simplicity for new developers.
