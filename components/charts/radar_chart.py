"""
Radar chart component for displaying evaluation scores.
"""
from typing import Dict
import plotly.graph_objects as go

def create_radar_chart(scores: Dict[str, int]) -> go.Figure:
    """
    Create a radar chart for the evaluation scores.
    
    Args:
        scores: Dictionary mapping criteria to scores (1-10)
        
    Returns:
        Plotly figure object
    """
    # Ensure we have scores to display
    if not scores:
        # Create default scores if none provided
        default_scores = {
            "Relevance to Job Description": 5,
            "Skills Match": 5,
            "Experience Match": 5,
            "Education Match": 5,
            "Overall Format and Structure": 5,
            "Action Verbs and Impact": 5,
            "Keyword Optimization": 5
        }
        categories = list(default_scores.keys())
        values = list(default_scores.values())
    else:
        categories = list(scores.keys())
        values = list(scores.values())
    
    # Create figure
    fig = go.Figure()
    
    # Add resume score trace
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Resume',
        line_color='rgba(31, 119, 180, 0.8)',
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    # Add a "perfect score" reference
    fig.add_trace(go.Scatterpolar(
        r=[10] * len(categories),
        theta=categories,
        fill='toself',
        name='Perfect Score',
        line_color='rgba(44, 160, 44, 0.5)',
        fillcolor='rgba(44, 160, 44, 0.1)'
    ))
    
    # Update layout with more explicit configuration
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showticklabels=True,
                ticks='outside'
            )
        ),
        showlegend=True,
        title="Resume Evaluation Scores",
        autosize=True,
        height=400,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    return fig 