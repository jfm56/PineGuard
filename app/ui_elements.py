from typing import Any

class UIElement:
    def __init__(self, name: str, label: str):
        self.name = name
        self.label = label

class Select(UIElement):
    def __init__(self, name: str, label: str, options: list[str], multiple: bool = False):
        super().__init__(name, label)
        self.options = options
        self.multiple = multiple

class DatePicker(UIElement):
    def __init__(self, name: str, label: str, range: bool = False):
        super().__init__(name, label)
        self.range = range

class Button(UIElement):
    def __init__(self, name: str, label: str, primary: bool = False, variant: str = "primary"):
        super().__init__(name, label)
        self.primary = primary
        self.variant = variant

class Sidebar:
    def __init__(self):
        self.elements: list[UIElement] = []

    def add_element(self, element: UIElement) -> None:
        self.elements.append(element)

def create_sidebar() -> Sidebar:
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
