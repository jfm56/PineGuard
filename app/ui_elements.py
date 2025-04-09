from windsurf import Sidebar, Button, Select, DatePicker

def create_sidebar():
    """Create the application sidebar with analysis tools"""
    sidebar = Sidebar()
    
    # Add layer controls
    layer_control = Select(
        name="active_layers",
        label="Map Layers",
        options=[
            "Land Use",
            "Historical Fires",
            "Vegetation",
            "Wildfire Risk"
        ],
        multiple=True
    )
    
    # Add time period selector
    time_period = DatePicker(
        name="analysis_period",
        label="Analysis Period",
        range=True
    )
    
    # Add analysis button
    analyze_button = Button(
        name="run_analysis",
        label="Calculate Risk",
        primary=True
    )
    
    # Add export button
    export_button = Button(
        name="export_results",
        label="Export Report",
        variant="secondary"
    )
    
    # Add all elements to sidebar
    sidebar.add_element(layer_control)
    sidebar.add_element(time_period)
    sidebar.add_element(analyze_button)
    sidebar.add_element(export_button)
    
    return sidebar
