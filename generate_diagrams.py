#!/usr/bin/env python3
"""
AttriSense - Professional Diagram Generator
Generates high-quality PNG diagrams using Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

def draw_rounded_rectangle(draw, xy, radius=20, fill='white', outline='black', width=2):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill, outline=outline, width=width)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill, outline=outline, width=width)
    draw.ellipse([x1, y1, x1+radius*2, y1+radius*2], fill=fill, outline=outline, width=width)
    draw.ellipse([x2-radius*2, y1, x2, y1+radius*2], fill=fill, outline=outline, width=width)
    draw.ellipse([x1, y2-radius*2, x1+radius*2, y2], fill=fill, outline=outline, width=width)
    draw.ellipse([x2-radius*2, y2-radius*2, x2, y2], fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, fill='black', width=3):
    """Draw an arrow from start to end"""
    x1, y1 = start
    x2, y2 = end
    draw.line([x1, y1, x2, y2], fill=fill, width=width)
    
    # Arrow head
    import math
    angle = math.atan2(y2-y1, x2-x1)
    arrow_size = 15
    arrow_angle1 = angle + math.pi * 5/6
    arrow_angle2 = angle - math.pi * 5/6
    
    p1 = (x2 + arrow_size * math.cos(arrow_angle1), y2 + arrow_size * math.sin(arrow_angle1))
    p2 = (x2 + arrow_size * math.cos(arrow_angle2), y2 + arrow_size * math.sin(arrow_angle2))
    draw.polygon([p1, (x2, y2), p2], fill=fill)

def create_architecture_diagram():
    """Create system architecture diagram"""
    width, height = 1920, 1200
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to load a nice font
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        label_font = ImageFont.truetype("arial.ttf", 22)
        small_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Title
    draw.text((width//2 - 200, 30), "AttriSense System Architecture", fill='#1a1a1a', font=title_font)
    
    # Define colors
    colors = {
        'data': '#E3F2FD',
        'ml': '#F3E5F5', 
        'rag': '#E8F5E9',
        'ai': '#FFF3E0',
        'ui': '#FCE4EC',
        'storage': '#FFFDE7'
    }
    
    # Components with better positioning
    components = [
        {'text': 'Data Generator\ndata_generator.py\nSynthetic HR Data', 'pos': (100, 180), 'size': (320, 140), 'color': colors['data']},
        {'text': 'CSV Data\nlumentum_synthetic_hr.csv\n5000 Employees', 'pos': (100, 380), 'size': (320, 120), 'color': colors['storage']},
        
        {'text': 'Predictive Engine\npredictive_engine.py\nRandom Forest + SMOTE', 'pos': (550, 180), 'size': (320, 140), 'color': colors['ml']},
        {'text': 'SQLite Database\nhr_enterprise.db\nworkforce_predictions', 'pos': (550, 380), 'size': (320, 120), 'color': colors['storage']},
        
        {'text': 'RAG Engine\nrag_engine.py\nFAISS Vectorization', 'pos': (1000, 180), 'size': (320, 140), 'color': colors['rag']},
        {'text': 'FAISS Vector Index\nfaiss_hr_index/\nExit Interview Embeddings', 'pos': (1000, 380), 'size': (320, 120), 'color': colors['storage']},
        
        {'text': 'AI SQL Constructor\nai_sql_constructor.py\nGPT-3.5-turbo NL-to-SQL', 'pos': (550, 600), 'size': (320, 160), 'color': colors['ai']},
        
        {'text': 'Streamlit Dashboard\ndashboard.py\nWeb Interface', 'pos': (550, 850), 'size': (320, 140), 'color': colors['ui']},
    ]
    
    # Draw components
    for comp in components:
        x, y = comp['pos']
        w, h = comp['size']
        draw_rounded_rectangle(draw, (x, y, x+w, y+h), radius=15, fill=comp['color'], outline='#333333', width=3)
        draw.text((x + w//2 - 100, y + h//2 - 30), comp['text'], fill='#1a1a1a', font=label_font, anchor="mm")
    
    # Draw arrows with proper positioning
    arrows = [
        ((260, 320), (260, 380)),      # Data Gen -> CSV
        ((260, 380), (550, 250)),      # CSV -> Predictive
        ((260, 380), (1000, 250)),     # CSV -> RAG
        ((710, 320), (710, 380)),      # Predictive -> SQLite
        ((1160, 320), (1160, 380)),    # RAG -> FAISS
        ((710, 500), (710, 600)),      # SQLite -> AI Constructor
        ((1160, 500), (710, 600)),     # FAISS -> AI Constructor
        ((710, 760), (710, 850)),      # AI Constructor -> Dashboard
    ]
    
    for start, end in arrows:
        draw_arrow(draw, start, end, fill='#333333', width=4)
    
    img.save('doc/architecture_diagram.png')
    print("✅ Architecture diagram created")

def create_execution_flow():
    """Create execution flow diagram"""
    width, height = 1600, 2000
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        step_font = ImageFont.truetype("arial.ttf", 24)
        detail_font = ImageFont.truetype("arial.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        step_font = ImageFont.load_default()
        detail_font = ImageFont.load_default()
    
    # Title
    draw.text((width//2 - 300, 40), "Project Setup & Execution Flow", fill='#1a1a1a', font=title_font)
    
    steps = [
        {'text': 'Setup Phase', 'y': 150, 'color': '#2196F3', 'items': [
            'Create Virtual Environment',
            'Activate Environment', 
            'Install Dependencies',
            'Configure .env with API Key'
        ]},
        {'text': 'Data Pipeline Phase', 'y': 550, 'color': '#FF9800', 'items': [
            'Step 1: python data_generator.py',
            'Step 2: python predictive_engine.py',
            'Step 3: python rag_engine.py',
            'Step 4: streamlit run dashboard.py'
        ]},
        {'text': 'User Interaction Phase', 'y': 1050, 'color': '#4CAF50', 'items': [
            'Access Dashboard at localhost:8501',
            'Tab 1: Predictive Analytics Dashboard',
            'Tab 2: Natural Language to SQL',
            'View Results & Export Insights'
        ]},
    ]
    
    y_pos = 150
    for phase in steps:
        # Phase header
        draw_rounded_rectangle(draw, (100, y_pos, width-100, y_pos+80), 
                             fill=phase['color'], outline='#333333', width=3)
        draw.text((width//2 - 100, y_pos + 40), phase['text'], 
                 fill='white', font=step_font, anchor="mm")
        
        y_pos += 120
        
        # Items
        for i, item in enumerate(phase['items']):
            item_y = y_pos + i * 90
            draw_rounded_rectangle(draw, (150, item_y, width-150, item_y + 70),
                                 fill='#F5F5F5', outline='#999999', width=2)
            draw.text((170, item_y + 35), f"• {item}", fill='#1a1a1a', font=detail_font, anchor="lm")
            
            # Arrow to next
            if i < len(phase['items']) - 1:
                draw_arrow(draw, (width//2, item_y + 70), (width//2, item_y + 90), 
                          fill='#666666', width=3)
        
        y_pos += len(phase['items']) * 90 + 100
    
    img.save('doc/execution_flow.png')
    print("✅ Execution flow diagram created")

def create_tech_stack():
    """Create technology stack diagram"""
    width, height = 1920, 1400
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        category_font = ImageFont.truetype("arial.ttf", 26)
        tech_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        category_font = ImageFont.load_default()
        tech_font = ImageFont.load_default()
    
    # Title
    draw.text((width//2 - 200, 30), "Technology Stack", fill='#1a1a1a', font=title_font)
    
    # Tech stack data
    tech_stack = {
        'Python & Data Science': {
            'color': '#E3F2FD',
            'pos': (50, 150),
            'techs': ['pandas', 'numpy', 'scikit-learn', 'imblearn (SMOTE)']
        },
        'Machine Learning': {
            'color': '#F3E5F5',
            'pos': (500, 150),
            'techs': ['RandomForest', 'Classification Models', 'SMOTE Resampling', 'Model Training']
        },
        'Web Framework': {
            'color': '#FCE4EC',
            'pos': (950, 150),
            'techs': ['Streamlit', 'Interactive UI', 'Real-time Updates', 'Data Visualization']
        },
        'AI & LLM': {
            'color': '#FFF3E0',
            'pos': (50, 700),
            'techs': ['OpenAI GPT-3.5-turbo', 'LangChain Framework', 'SQL Query Generation', 'Prompt Engineering']
        },
        'Vector & Storage': {
            'color': '#E8F5E9',
            'pos': (500, 700),
            'techs': ['FAISS Vector DB', 'SQLite Database', 'Embeddings', 'Vector Search']
        },
        'Visualization': {
            'color': '#FFFDE7',
            'pos': (950, 700),
            'techs': ['Plotly Express', 'Interactive Charts', 'Heatmaps', 'Dashboards']
        }
    }
    
    for category, info in tech_stack.items():
        x, y = info['pos']
        color = info['color']
        
        # Category box
        draw_rounded_rectangle(draw, (x, y, x + 380, y + 480), 
                             fill=color, outline='#333333', width=3)
        
        # Category title
        draw.text((x + 190, y + 30), category, fill='#1a1a1a', 
                 font=category_font, anchor="mm")
        
        # Technologies
        tech_y = y + 100
        for tech in info['techs']:
            draw_rounded_rectangle(draw, (x+20, tech_y, x+360, tech_y + 60),
                                 fill='white', outline='#999999', width=2)
            draw.text((x + 30, tech_y + 30), f"→ {tech}", fill='#1a1a1a', 
                     font=tech_font, anchor="lm")
            tech_y += 80
    
    img.save('doc/technology_stack.png')
    print("✅ Technology stack diagram created")

def main():
    """Generate all diagrams"""
    os.makedirs('doc', exist_ok=True)
    
    print("Generating professional diagrams...")
    print()
    
    create_architecture_diagram()
    create_execution_flow()
    create_tech_stack()
    
    print()
    print("=" * 50)
    print("All diagrams generated successfully!")
    print("Location: doc/")
    print("=" * 50)

if __name__ == "__main__":
    main()
