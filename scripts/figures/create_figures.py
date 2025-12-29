"""
Figure Generation Script for Research Paper
Creates all visualization figures for the SQL Injection Detection project
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import os
import sys
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.patches import Rectangle, Circle, Ellipse
import matplotlib.patches as mpatches

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory
import pathlib
base_path = pathlib.Path(__file__).parent.parent.parent
output_dir = base_path / 'research' / 'figures'
output_dir.mkdir(parents=True, exist_ok=True)
output_dir = str(output_dir)

# Set font for better quality
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

print("=" * 80)
print("Creating Research Figures")
print("=" * 80)

# ============================================
# Figure 1: Complete Project Flowchart
# ============================================
def create_complete_flowchart():
    """Create complete project flowchart"""
    print("\n1. Creating Complete Project Flowchart...")
    
    fig, ax = plt.subplots(figsize=(18, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(5, 13.5, 'Complete Project Workflow', 
            ha='center', va='center', fontsize=22, fontweight='bold')
    
    # Step 1: Start
    start_box = FancyBboxPatch((2.5, 12), 5, 0.9, 
                               boxstyle="round,pad=0.15", 
                               facecolor='lightblue', 
                               edgecolor='black', linewidth=2.5)
    ax.add_patch(start_box)
    ax.text(5, 12.6, 'STEP 1: Original Dataset', 
            ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(5, 12.2, 'Total Samples: 30,919', 
            ha='center', va='center', fontsize=11)
    ax.text(5, 11.9, 'Balance Ratio: 58.26% (Unbalanced)', 
            ha='center', va='center', fontsize=11, style='italic')
    ax.text(5, 11.6, 'Normal: 19,528 (63.19%) | SQLi: 11,391 (36.81%)', 
            ha='center', va='center', fontsize=10)
    
    # Arrow
    ax.arrow(5, 12, 0, -0.4, head_width=0.25, head_length=0.12, 
             fc='black', ec='black', linewidth=2.5)
    
    # Step 2: Preprocessing
    prep_box = FancyBboxPatch((1, 9.5), 8, 1.8, 
                              boxstyle="round,pad=0.15", 
                              facecolor='lightgreen', 
                              edgecolor='black', linewidth=2.5)
    ax.add_patch(prep_box)
    ax.text(5, 11, 'STEP 2: Preprocessing Pipeline', 
            ha='center', va='center', fontsize=15, fontweight='bold')
    ax.text(2.5, 10.4, 'Advanced Cleaning:\n-27 samples removed', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(5, 10.4, 'False Positives:\n+8 corrected', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(7.5, 10.4, 'New Patterns:\n+126 patterns', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(5, 9.9, 'Balancing: Undersampling applied', 
            ha='center', va='center', fontsize=10)
    ax.text(5, 9.6, 'Result: 25,278 samples | Balance: 83.33% (+43% improvement)', 
            ha='center', va='center', fontsize=11, fontweight='bold', style='italic')
    
    # Arrow
    ax.arrow(5, 9.5, 0, -0.4, head_width=0.25, head_length=0.12, 
             fc='black', ec='black', linewidth=2.5)
    
    # Step 3: Vectorization
    vec_box = FancyBboxPatch((1.5, 7.5), 7, 1.4, 
                             boxstyle="round,pad=0.15", 
                             facecolor='lightyellow', 
                             edgecolor='black', linewidth=2.5)
    ax.add_patch(vec_box)
    ax.text(5, 8.6, 'STEP 3: Text Vectorization (TF-IDF)', 
            ha='center', va='center', fontsize=15, fontweight='bold')
    ax.text(3, 8.1, 'Parameters:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(3, 7.8, 'max_features: 10,000\nngram_range: (1, 3)', 
            ha='center', va='center', fontsize=10)
    ax.text(7, 8.1, 'Output:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(7, 7.8, '10,000 feature vectors\nReady for training', 
            ha='center', va='center', fontsize=10)
    
    # Arrow
    ax.arrow(5, 7.5, 0, -0.4, head_width=0.25, head_length=0.12, 
             fc='black', ec='black', linewidth=2.5)
    
    # Step 4: Modeling
    model_box = FancyBboxPatch((0.5, 5), 9, 2, 
                               boxstyle="round,pad=0.15", 
                               facecolor='lightcoral', 
                               edgecolor='black', linewidth=2.5)
    ax.add_patch(model_box)
    ax.text(5, 6.7, 'STEP 4: Model Training & Comparison', 
            ha='center', va='center', fontsize=15, fontweight='bold')
    
    # SVM box
    svm_box = FancyBboxPatch((1.5, 5.3), 3, 1.2, 
                             boxstyle="round,pad=0.1", 
                             facecolor='white', 
                             edgecolor='blue', linewidth=2)
    ax.add_patch(svm_box)
    ax.text(3, 6.1, 'SVM Model', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='blue')
    ax.text(3, 5.8, 'Validation Accuracy: 99.21%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(3, 5.5, 'F1-Score: 99.12% | Precision: 99.88%', 
            ha='center', va='center', fontsize=9)
    ax.text(3, 5.2, 'Training Time: 58.49s', 
            ha='center', va='center', fontsize=9, style='italic')
    
    # LR box
    lr_box = FancyBboxPatch((5.5, 5.3), 3, 1.2, 
                            boxstyle="round,pad=0.1", 
                            facecolor='white', 
                            edgecolor='green', linewidth=2)
    ax.add_patch(lr_box)
    ax.text(7, 6.1, 'Logistic Regression', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='green')
    ax.text(7, 5.8, 'Validation Accuracy: 98.87%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(7, 5.5, 'F1-Score: 98.74% | Precision: 99.88%', 
            ha='center', va='center', fontsize=9)
    ax.text(7, 5.2, 'Training Time: 0.13s', 
            ha='center', va='center', fontsize=9, style='italic')
    
    # Arrow
    ax.arrow(5, 5, 0, -0.4, head_width=0.25, head_length=0.12, 
             fc='black', ec='black', linewidth=2.5)
    
    # Step 5: Evaluation
    eval_box = FancyBboxPatch((1.5, 2.5), 7, 1.6, 
                              boxstyle="round,pad=0.15", 
                              facecolor='lightpink', 
                              edgecolor='black', linewidth=2.5)
    ax.add_patch(eval_box)
    ax.text(5, 3.8, 'STEP 5: Model Evaluation & Selection', 
            ha='center', va='center', fontsize=15, fontweight='bold')
    ax.text(5, 3.4, 'Best Model Selected: SVM (F1-Score: 99.12%)', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(3.5, 3, 'Test Set Results:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(3.5, 2.7, 'Accuracy: 99.53%\nPrecision: 99.77%', 
            ha='center', va='center', fontsize=10)
    ax.text(6.5, 3, 'Additional Metrics:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(6.5, 2.7, 'Recall: 99.19%\nF1-Score: 99.48%', 
            ha='center', va='center', fontsize=10)
    
    # Arrow
    ax.arrow(5, 2.5, 0, -0.4, head_width=0.25, head_length=0.12, 
             fc='black', ec='black', linewidth=2.5)
    
    # Final
    final_box = FancyBboxPatch((2.5, 0.5), 5, 1.2, 
                               boxstyle="round,pad=0.15", 
                               facecolor='gold', 
                               edgecolor='black', linewidth=3)
    ax.add_patch(final_box)
    ax.text(5, 1.3, 'Final Model Ready for Production', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(5, 0.95, 'SVM Model with 99.53% Test Accuracy', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(5, 0.65, 'High Performance | Production Ready', 
            ha='center', va='center', fontsize=11, style='italic')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'complete_project_flowchart.png'))
    print(f"   [OK] Saved: complete_project_flowchart.png")

# ============================================
# Figure 2: Preprocessing Flowchart
# ============================================
def create_preprocessing_flowchart():
    """Create preprocessing flowchart"""
    print("\n2. Creating Preprocessing Flowchart...")
    
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    ax.text(5, 11.5, 'Preprocessing Pipeline - Detailed Steps', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Step 1: Original Dataset
    step1_box = FancyBboxPatch((2, 10), 6, 1, 
                               boxstyle="round,pad=0.15", 
                               facecolor='lightblue', 
                               edgecolor='black', linewidth=2.5)
    ax.add_patch(step1_box)
    ax.text(5, 10.6, 'STEP 1: Original Dataset', 
            ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(5, 10.3, 'Total: 30,919 samples | Balance: 58.26% (Unbalanced)', 
            ha='center', va='center', fontsize=11)
    ax.text(5, 10, 'Normal: 19,528 (63.19%) | SQL Injection: 11,391 (36.81%)', 
            ha='center', va='center', fontsize=10)
    
    ax.arrow(5, 10, 0, -0.4, head_width=0.2, head_length=0.1, 
             fc='black', ec='black', linewidth=2)
    
    # Step 2: Advanced Cleaning
    step2_box = FancyBboxPatch((1, 8.5), 3.5, 1.2, 
                               boxstyle="round,pad=0.15", 
                               facecolor='lightgreen', 
                               edgecolor='black', linewidth=2)
    ax.add_patch(step2_box)
    ax.text(2.75, 9.3, 'STEP 2: Advanced Cleaning', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(2.75, 9, 'Removed: 27 samples', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(2.75, 8.7, 'Reasons:', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(2.75, 8.5, '• Length > 5000 chars: 1\n• Length < 3 chars: 26', 
            ha='center', va='center', fontsize=9)
    
    # Step 3: False Positives
    step3_box = FancyBboxPatch((5.5, 8.5), 3.5, 1.2, 
                                boxstyle="round,pad=0.15", 
                                facecolor='lightyellow', 
                                edgecolor='black', linewidth=2)
    ax.add_patch(step3_box)
    ax.text(7.25, 9.3, 'STEP 3: False Positives', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(7.25, 9, 'Corrected: 8 samples', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(7.25, 8.7, 'Action:', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(7.25, 8.5, 'Re-labeled from\nNormal to SQLi', 
            ha='center', va='center', fontsize=9)
    
    ax.arrow(2.75, 8.5, 2.5, -0.3, head_width=0.15, head_length=0.08, 
             fc='black', ec='black', linewidth=2)
    ax.arrow(7.25, 8.5, -2.5, -0.3, head_width=0.15, head_length=0.08, 
             fc='black', ec='black', linewidth=2)
    
    # Step 4: New Patterns
    step4_box = FancyBboxPatch((1, 6.5), 3.5, 1.2, 
                               boxstyle="round,pad=0.15", 
                               facecolor='lightcoral', 
                               edgecolor='black', linewidth=2)
    ax.add_patch(step4_box)
    ax.text(2.75, 7.3, 'STEP 4: New Patterns', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(2.75, 7, 'Added: 126 patterns', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(2.75, 6.7, 'Source:', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(2.75, 6.5, 'Real-world SQLi\nattack patterns', 
            ha='center', va='center', fontsize=9)
    
    # Step 5: Balancing
    step5_box = FancyBboxPatch((5.5, 6.5), 3.5, 1.2, 
                               boxstyle="round,pad=0.15", 
                               facecolor='lightpink', 
                               edgecolor='black', linewidth=2)
    ax.add_patch(step5_box)
    ax.text(7.25, 7.3, 'STEP 5: Dataset Balancing', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(7.25, 7, 'Method: Undersampling', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(7.25, 6.7, 'Result:', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(7.25, 6.5, 'Balance: 58.26% → 83.33%\n(+43% improvement)', 
            ha='center', va='center', fontsize=9)
    
    ax.arrow(2.75, 6.5, 2.5, -0.3, head_width=0.15, head_length=0.08, 
             fc='black', ec='black', linewidth=2)
    ax.arrow(7.25, 6.5, -2.5, -0.3, head_width=0.15, head_length=0.08, 
             fc='black', ec='black', linewidth=2)
    
    # Step 6: Splitting
    step6_box = FancyBboxPatch((2.5, 4.5), 5, 1.2, 
                               boxstyle="round,pad=0.15", 
                               facecolor='lightgray', 
                               edgecolor='black', linewidth=2)
    ax.add_patch(step6_box)
    ax.text(5, 5.3, 'STEP 6: Data Splitting (Stratified)', 
            ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(3, 5, 'Train: 17,694 (70%)', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(5, 5, 'Validation: 3,792 (15%)', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(7, 5, 'Test: 3,792 (15%)', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(5, 4.7, 'All splits maintain 83.33% balance ratio', 
            ha='center', va='center', fontsize=10, style='italic')
    
    ax.arrow(5, 4.5, 0, -0.4, head_width=0.2, head_length=0.1, 
             fc='black', ec='black', linewidth=2)
    
    # Final Result
    final_box = FancyBboxPatch((2, 2.5), 6, 1.4, 
                               boxstyle="round,pad=0.15", 
                               facecolor='gold', 
                               edgecolor='black', linewidth=3)
    ax.add_patch(final_box)
    ax.text(5, 3.5, 'FINAL: Clean & Balanced Dataset', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(5, 3.1, 'Total Samples: 25,278', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(3.5, 2.8, 'Normal: 13,788 (54.55%)', 
            ha='center', va='center', fontsize=11)
    ax.text(6.5, 2.8, 'SQLi: 11,490 (45.45%)', 
            ha='center', va='center', fontsize=11)
    ax.text(5, 2.6, 'Balance Ratio: 83.33% (Excellent)', 
            ha='center', va='center', fontsize=11, fontweight='bold', style='italic')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'preprocessing_flowchart.png'))
    print(f"   [OK] Saved: preprocessing_flowchart.png")

# ============================================
# Figure 3: Modeling Flowchart
# ============================================
def create_modeling_flowchart():
    """Create modeling flowchart"""
    print("\n3. Creating Modeling Flowchart...")
    
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    ax.text(5, 11.5, 'Modeling Pipeline - Training & Selection', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Step 1: Vectorization
    vec_box = FancyBboxPatch((1.5, 9.5), 7, 1.4, 
                            boxstyle="round,pad=0.15", 
                            facecolor='lightblue', 
                            edgecolor='black', linewidth=2.5)
    ax.add_patch(vec_box)
    ax.text(5, 10.5, 'STEP 1: TF-IDF Vectorization', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(3, 10, 'Input:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(3, 9.7, '25,278 text samples\n(Preprocessed)', 
            ha='center', va='center', fontsize=10)
    ax.text(7, 10, 'Parameters:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(7, 9.7, 'max_features: 10,000\nngram_range: (1, 3)', 
            ha='center', va='center', fontsize=10)
    ax.text(5, 9.4, 'Output: 10,000-dimensional feature vectors', 
            ha='center', va='center', fontsize=11, fontweight='bold', style='italic')
    
    ax.arrow(5, 9.5, 0, -0.4, head_width=0.25, head_length=0.12, 
             fc='black', ec='black', linewidth=2.5)
    
    # Step 2: Training
    train_box = FancyBboxPatch((0.5, 6.5), 9, 2.5, 
                               boxstyle="round,pad=0.15", 
                               facecolor='lightgreen', 
                               edgecolor='black', linewidth=2.5)
    ax.add_patch(train_box)
    ax.text(5, 8.5, 'STEP 2: Model Training on Validation Set', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(5, 8.1, 'Training Set: 17,694 samples | Validation Set: 3,792 samples', 
            ha='center', va='center', fontsize=11)
    
    # SVM box
    svm_box = FancyBboxPatch((1.5, 6.8), 3, 1.4, 
                            boxstyle="round,pad=0.1", 
                            facecolor='white', 
                            edgecolor='blue', linewidth=2.5)
    ax.add_patch(svm_box)
    ax.text(3, 7.8, 'SVM Model', 
            ha='center', va='center', fontsize=13, fontweight='bold', color='blue')
    ax.text(3, 7.5, 'Validation Results:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(3, 7.2, 'Accuracy: 99.21%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(3, 7, 'Precision: 99.88% | Recall: 98.38%', 
            ha='center', va='center', fontsize=9)
    ax.text(3, 6.8, 'F1-Score: 99.12%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(3, 6.6, 'Training Time: 58.49 seconds', 
            ha='center', va='center', fontsize=9, style='italic')
    
    # LR box
    lr_box = FancyBboxPatch((5.5, 6.8), 3, 1.4, 
                           boxstyle="round,pad=0.1", 
                           facecolor='white', 
                           edgecolor='green', linewidth=2.5)
    ax.add_patch(lr_box)
    ax.text(7, 7.8, 'Logistic Regression', 
            ha='center', va='center', fontsize=13, fontweight='bold', color='green')
    ax.text(7, 7.5, 'Validation Results:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(7, 7.2, 'Accuracy: 98.87%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(7, 7, 'Precision: 99.88% | Recall: 97.62%', 
            ha='center', va='center', fontsize=9)
    ax.text(7, 6.8, 'F1-Score: 98.74%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(7, 6.6, 'Training Time: 0.13 seconds', 
            ha='center', va='center', fontsize=9, style='italic')
    
    ax.arrow(5, 6.5, 0, -0.4, head_width=0.25, head_length=0.12, 
             fc='black', ec='black', linewidth=2.5)
    
    # Step 3: Comparison
    comp_box = FancyBboxPatch((2, 4.5), 6, 1.2, 
                             boxstyle="round,pad=0.15", 
                             facecolor='lightyellow', 
                             edgecolor='black', linewidth=2.5)
    ax.add_patch(comp_box)
    ax.text(5, 5.3, 'STEP 3: Model Comparison', 
            ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(3, 5, 'SVM: 99.12% F1-Score', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='blue')
    ax.text(7, 5, 'LR: 98.74% F1-Score', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='green')
    ax.text(5, 4.7, 'Selection Criteria: F1-Score (Best Performance)', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    ax.arrow(5, 4.5, 0, -0.4, head_width=0.25, head_length=0.12, 
             fc='black', ec='black', linewidth=2.5)
    
    # Final Selection
    sel_box = FancyBboxPatch((2.5, 2), 5, 1.6, 
                             boxstyle="round,pad=0.15", 
                             facecolor='gold', 
                             edgecolor='black', linewidth=3)
    ax.add_patch(sel_box)
    ax.text(5, 3.2, 'SELECTED: SVM Model', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(5, 2.8, 'Best F1-Score: 99.12%', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(5, 2.5, 'Ready for Final Test Evaluation', 
            ha='center', va='center', fontsize=11, style='italic')
    ax.text(5, 2.2, 'Advantage: +0.38% F1-Score over LR', 
            ha='center', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'modeling_flowchart.png'))
    print(f"   [OK] Saved: modeling_flowchart.png")

# ============================================
# Figure 4: Evaluation Flowchart
# ============================================
def create_evaluation_flowchart():
    """Create evaluation flowchart"""
    print("\n4. Creating Evaluation Flowchart...")
    
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    ax.text(5, 11.5, 'Evaluation Pipeline - Model Testing & Selection', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Step 1: Models from Training
    ax.text(5, 10.5, 'STEP 1: Trained Models Ready for Evaluation', 
            ha='center', va='center', fontsize=13, fontweight='bold')
    
    # SVM box
    svm_box = FancyBboxPatch((1, 8.5), 3.5, 1.6, 
                            boxstyle="round,pad=0.15", 
                            facecolor='lightblue', 
                            edgecolor='blue', linewidth=2.5)
    ax.add_patch(svm_box)
    ax.text(2.75, 9.6, 'SVM Model', 
            ha='center', va='center', fontsize=13, fontweight='bold', color='blue')
    ax.text(2.75, 9.3, 'Validation Set Results:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(2.75, 9.1, 'Accuracy: 99.21%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(2.75, 8.9, 'Precision: 99.88%', 
            ha='center', va='center', fontsize=10)
    ax.text(2.75, 8.7, 'Recall: 98.38%', 
            ha='center', va='center', fontsize=10)
    ax.text(2.75, 8.5, 'F1-Score: 99.12%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # LR box
    lr_box = FancyBboxPatch((5.5, 8.5), 3.5, 1.6, 
                           boxstyle="round,pad=0.15", 
                           facecolor='lightgreen', 
                           edgecolor='green', linewidth=2.5)
    ax.add_patch(lr_box)
    ax.text(7.25, 9.6, 'Logistic Regression', 
            ha='center', va='center', fontsize=13, fontweight='bold', color='green')
    ax.text(7.25, 9.3, 'Validation Set Results:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(7.25, 9.1, 'Accuracy: 98.87%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(7.25, 8.9, 'Precision: 99.88%', 
            ha='center', va='center', fontsize=10)
    ax.text(7.25, 8.7, 'Recall: 97.62%', 
            ha='center', va='center', fontsize=10)
    ax.text(7.25, 8.5, 'F1-Score: 98.74%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    ax.arrow(2.75, 8.5, 0, -0.5, head_width=0.2, head_length=0.1, 
             fc='black', ec='black', linewidth=2)
    ax.arrow(7.25, 8.5, 0, -0.5, head_width=0.2, head_length=0.1, 
             fc='black', ec='black', linewidth=2)
    
    # Step 2: Comparison
    comp_box = FancyBboxPatch((1.5, 6), 7, 1.4, 
                              boxstyle="round,pad=0.15", 
                              facecolor='lightyellow', 
                              edgecolor='black', linewidth=2.5)
    ax.add_patch(comp_box)
    ax.text(5, 7, 'STEP 2: Model Comparison & Selection', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(3, 6.6, 'SVM Performance:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(3, 6.4, 'F1-Score: 99.12%', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='blue')
    ax.text(7, 6.6, 'LR Performance:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(7, 6.4, 'F1-Score: 98.74%', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='green')
    ax.text(5, 6.2, 'Winner: SVM (Selected based on F1-Score)', 
            ha='center', va='center', fontsize=12, fontweight='bold', style='italic')
    
    ax.arrow(5, 6, 0, -0.5, head_width=0.25, head_length=0.12, 
             fc='black', ec='black', linewidth=2.5)
    
    # Step 3: Test Evaluation
    test_box = FancyBboxPatch((0.5, 3), 9, 2.5, 
                              boxstyle="round,pad=0.15", 
                              facecolor='lightcoral', 
                              edgecolor='black', linewidth=2.5)
    ax.add_patch(test_box)
    ax.text(5, 5, 'STEP 3: Final Test Set Evaluation (Both Models)', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(5, 4.7, 'Test Set: 3,792 samples (Unseen Data)', 
            ha='center', va='center', fontsize=11)
    
    # SVM Test Results
    ax.text(2.5, 4.3, 'SVM Test Results:', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='blue')
    ax.text(2.5, 4.1, 'Accuracy: 99.53%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(2.5, 3.9, 'Precision: 99.77%', 
            ha='center', va='center', fontsize=10)
    ax.text(2.5, 3.7, 'Recall: 99.19%', 
            ha='center', va='center', fontsize=10)
    ax.text(2.5, 3.5, 'F1-Score: 99.48%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # LR Test Results
    ax.text(7.5, 4.3, 'LR Test Results:', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='green')
    ax.text(7.5, 4.1, 'Accuracy: 99.37%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(7.5, 3.9, 'Precision: 100.00%', 
            ha='center', va='center', fontsize=10)
    ax.text(7.5, 3.7, 'Recall: 98.61%', 
            ha='center', va='center', fontsize=10)
    ax.text(7.5, 3.5, 'F1-Score: 99.30%', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    ax.text(5, 3.3, 'Winner: SVM (F1-Score: 99.48% vs 99.30%)', 
            ha='center', va='center', fontsize=11, fontweight='bold', style='italic')
    
    ax.arrow(5, 3.5, 0, -0.5, head_width=0.25, head_length=0.12, 
             fc='black', ec='black', linewidth=2.5)
    
    # Final Result
    final_box = FancyBboxPatch((2, 1), 6, 1.8, 
                               boxstyle="round,pad=0.15", 
                               facecolor='gold', 
                               edgecolor='black', linewidth=3)
    ax.add_patch(final_box)
    ax.text(5, 2.4, 'FINAL MODEL: Production Ready', 
            ha='center', va='center', fontsize=15, fontweight='bold')
    ax.text(5, 2, 'SVM Model with 99.53% Test Accuracy', 
            ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(5, 1.7, 'High Performance Metrics:', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(3.5, 1.5, 'Precision: 99.77%', 
            ha='center', va='center', fontsize=10)
    ax.text(6.5, 1.5, 'Recall: 99.19%', 
            ha='center', va='center', fontsize=10)
    ax.text(5, 1.3, 'F1-Score: 99.48% | Ready for Deployment', 
            ha='center', va='center', fontsize=11, fontweight='bold', style='italic')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'evaluation_flowchart.png'))
    print(f"   [OK] Saved: evaluation_flowchart.png")

# ============================================
# Figure 5: Model Comparison Bar Chart
# ============================================
def create_model_comparison():
    """Create model comparison bar chart"""
    print("\n5. Creating Model Comparison Chart...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    models = ['SVM', 'Logistic\nRegression']
    x = np.arange(len(models))
    width = 0.35
    
    # Validation Set - Accuracy and F1-Score
    val_accuracy = [99.21, 98.87]
    val_f1_score = [99.12, 98.74]
    
    bars1 = ax1.bar(x - width/2, val_accuracy, width, label='Accuracy', 
                    color='steelblue', alpha=0.8)
    bars2 = ax1.bar(x + width/2, val_f1_score, width, label='F1-Score', 
                    color='coral', alpha=0.8)
    
    ax1.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Model Performance Comparison\n(Validation Set)', 
                  fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, fontsize=11)
    ax1.legend(fontsize=10)
    ax1.set_ylim(97, 100)
    ax1.grid(axis='y', alpha=0.3)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%',
                    ha='center', va='bottom', fontsize=9)
    
    # Validation Set - Precision and Recall
    val_precision = [99.88, 99.88]
    val_recall = [98.38, 97.62]
    
    bars3 = ax2.bar(x - width/2, val_precision, width, label='Precision', 
                    color='lightgreen', alpha=0.8)
    bars4 = ax2.bar(x + width/2, val_recall, width, label='Recall', 
                    color='gold', alpha=0.8)
    
    ax2.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Precision and Recall Comparison\n(Validation Set)', 
                  fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(models, fontsize=11)
    ax2.legend(fontsize=10)
    ax2.set_ylim(96, 100)
    ax2.grid(axis='y', alpha=0.3)
    
    for bars in [bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%',
                    ha='center', va='bottom', fontsize=9)
    
    # Test Set - Accuracy and F1-Score
    test_accuracy = [99.53, 99.37]
    test_f1_score = [99.48, 99.30]
    
    bars5 = ax3.bar(x - width/2, test_accuracy, width, label='Accuracy', 
                    color='steelblue', alpha=0.8)
    bars6 = ax3.bar(x + width/2, test_f1_score, width, label='F1-Score', 
                    color='coral', alpha=0.8)
    
    ax3.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax3.set_title('Model Performance Comparison\n(Test Set)', 
                  fontsize=14, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(models, fontsize=11)
    ax3.legend(fontsize=10)
    ax3.set_ylim(98, 100.5)
    ax3.grid(axis='y', alpha=0.3)
    
    for bars in [bars5, bars6]:
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%',
                    ha='center', va='bottom', fontsize=9)
    
    # Test Set - Precision and Recall
    test_precision = [99.77, 100.00]
    test_recall = [99.19, 98.61]
    
    bars7 = ax4.bar(x - width/2, test_precision, width, label='Precision', 
                    color='lightgreen', alpha=0.8)
    bars8 = ax4.bar(x + width/2, test_recall, width, label='Recall', 
                    color='gold', alpha=0.8)
    
    ax4.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Precision and Recall Comparison\n(Test Set)', 
                  fontsize=14, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(models, fontsize=11)
    ax4.legend(fontsize=10)
    ax4.set_ylim(97.5, 100.5)
    ax4.grid(axis='y', alpha=0.3)
    
    for bars in [bars7, bars8]:
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%',
                    ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'model_comparison.png'))
    print(f"   [OK] Saved: model_comparison.png")

# ============================================
# Figure 6: Performance Metrics
# ============================================
def create_performance_metrics():
    """Create performance metrics visualization"""
    print("\n6. Creating Performance Metrics Chart...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    x = np.arange(len(metrics))
    width = 0.35
    
    # SVM Metrics
    svm_val_scores = [99.21, 99.88, 98.38, 99.12]
    svm_test_scores = [99.53, 99.77, 99.19, 99.48]
    
    bars1 = ax1.bar(x - width/2, svm_val_scores, width, 
                   label='Validation Set', color='steelblue', alpha=0.8)
    bars2 = ax1.bar(x + width/2, svm_test_scores, width, 
                   label='Test Set', color='coral', alpha=0.8)
    
    ax1.set_ylabel('Score (%)', fontsize=14, fontweight='bold')
    ax1.set_title('SVM Model Performance Metrics', 
                 fontsize=16, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics, fontsize=12)
    ax1.legend(fontsize=12)
    ax1.set_ylim(97, 100.5)
    ax1.grid(axis='y', alpha=0.3)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Logistic Regression Metrics
    lr_val_scores = [98.87, 99.88, 97.62, 98.74]
    lr_test_scores = [99.37, 100.00, 98.61, 99.30]
    
    bars3 = ax2.bar(x - width/2, lr_val_scores, width, 
                   label='Validation Set', color='lightgreen', alpha=0.8)
    bars4 = ax2.bar(x + width/2, lr_test_scores, width, 
                   label='Test Set', color='gold', alpha=0.8)
    
    ax2.set_ylabel('Score (%)', fontsize=14, fontweight='bold')
    ax2.set_title('Logistic Regression Model Performance Metrics', 
                 fontsize=16, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics, fontsize=12)
    ax2.legend(fontsize=12)
    ax2.set_ylim(96.5, 100.5)
    ax2.grid(axis='y', alpha=0.3)
    
    for bars in [bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'performance_metrics.png'))
    print(f"   [OK] Saved: performance_metrics.png")

# ============================================
# Figure 7: Balance Comparison
# ============================================
def create_balance_comparison():
    """Create balance comparison pie charts"""
    print("\n7. Creating Balance Comparison Chart...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    # Before balancing
    before_sizes = [63.19, 36.81]
    before_labels = ['Normal Queries', 'SQL Injection']
    before_colors = ['lightblue', 'lightcoral']
    
    ax1.pie(before_sizes, labels=before_labels, autopct='%1.2f%%',
            startangle=90, colors=before_colors, textprops={'fontsize': 11})
    ax1.set_title('Dataset Balance - Before\n(Balance Ratio: 58.26%)', 
                  fontsize=14, fontweight='bold')
    
    # After balancing
    after_sizes = [54.55, 45.45]
    after_labels = ['Normal Queries', 'SQL Injection']
    after_colors = ['lightgreen', 'coral']
    
    ax2.pie(after_sizes, labels=after_labels, autopct='%1.2f%%',
            startangle=90, colors=after_colors, textprops={'fontsize': 11})
    ax2.set_title('Dataset Balance - After\n(Balance Ratio: 83.33%)', 
                  fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'balance_comparison.png'))
    print(f"   [OK] Saved: balance_comparison.png")

# ============================================
# Figure 8: Accuracy Timeline
# ============================================
def create_accuracy_timeline():
    """Create accuracy progression timeline"""
    print("\n8. Creating Accuracy Timeline...")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    stages = ['Original\nDataset', 'After\nCleaning', 'After\nBalancing', 
              'SVM\nValidation', 'SVM\nTest']
    accuracy = [58.26, 58.26, 83.33, 99.21, 99.53]
    
    colors = ['lightgray', 'lightblue', 'lightgreen', 'coral', 'gold']
    
    bars = ax.bar(stages, accuracy, color=colors, alpha=0.8, 
                  edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax.set_title('Accuracy Progression Through Project Stages', 
                 fontsize=14, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, (bar, acc) in enumerate(zip(bars, accuracy)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{acc:.2f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Add improvement arrows
    for i in range(len(accuracy)-1):
        if accuracy[i+1] > accuracy[i]:
            ax.annotate('', xy=(i+1, accuracy[i+1]), xytext=(i, accuracy[i]),
                       arrowprops=dict(arrowstyle='->', color='green', lw=2))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_timeline.png'))
    print(f"   [OK] Saved: accuracy_timeline.png")

# ============================================
# Main Function
# ============================================
def main():
    """Generate all figures"""
    print(f"\nOutput directory: {output_dir}")
    print(f"Creating {8} figures...\n")
    
    create_complete_flowchart()
    create_preprocessing_flowchart()
    create_modeling_flowchart()
    create_evaluation_flowchart()
    create_model_comparison()
    create_performance_metrics()
    create_balance_comparison()
    create_accuracy_timeline()
    
    print("\n" + "=" * 80)
    print("[SUCCESS] All figures created successfully!")
    print(f"[INFO] Figures saved in: {output_dir}")
    print("=" * 80)

if __name__ == "__main__":
    main()

