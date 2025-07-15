"""
Bar chart component for displaying keyword metrics.
"""
from typing import Dict, Any
import plotly.graph_objects as go

def create_keyword_chart(keyword_metrics: Dict[str, Any]) -> go.Figure:
    """
    Create a bar chart for keyword metrics.
    
    Args:
        keyword_metrics: Dictionary with keyword metrics
        
    Returns:
        Plotly figure object
    """
    categories = []
    percentages = []
    
    for category, data in keyword_metrics.items():
        if category != "overall":
            categories.append(category.replace("_", " ").title())
            percentages.append(data["percentage"])
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=percentages,
            marker_color='rgba(31, 119, 180, 0.8)'
        )
    ])
    
    fig.update_layout(
        title="Keyword Coverage by Category (%)",
        xaxis_title="Category",
        yaxis_title="Coverage (%)",
        yaxis=dict(range=[0, 100])
    )
    
    return fig 