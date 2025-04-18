"""UI elements for the wildfire risk analysis application."""
from typing import List


class UIElement:
    """Base class for UI elements."""
    def __init__(self, name: str, label: str):
        self.name = name
        self.label = label


class Select(UIElement):
    """Select dropdown UI element."""
    def __init__(self, name: str, label: str, options: List[str],
                 multiple: bool = False):
        super().__init__(name, label)
        self.options = options
        self.multiple = multiple


class DatePicker(UIElement):
    """Date picker UI element."""
    def __init__(self, name: str, label: str, date_range: bool = False):
        super().__init__(name, label)
        self.range = date_range


class Button(UIElement):
    """Button UI element."""
    def __init__(self, name: str, label: str, primary: bool = False,
                 variant: str = "primary"):
        super().__init__(name, label)
        self.primary = primary
        self.variant = variant


class Sidebar:
    """Sidebar container for UI elements."""
    def __init__(self):
        self.elements: List[UIElement] = []

    def add_element(self, element: UIElement) -> None:
        """Add a UI element to the sidebar."""
        self.elements.append(element)


def create_sidebar() -> Sidebar:
    """Create the application sidebar with analysis tools."""
    # Add period to docstring to fix flake8 D400
    sidebar = Sidebar()

    # Add layer controls
    layer_control = Select(
        name="active_layers",
        label="Map Layers",
        options=["Land Use", "Historical Fires", "Vegetation", "Wildfire Risk"],
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
