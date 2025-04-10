import pytest
from app.ui_elements import (
    UIElement,
    Select,
    DatePicker,
    Button,
    Sidebar,
    create_sidebar
)

def test_ui_element():
    element = UIElement("test", "Test Label")
    assert element.name == "test"
    assert element.label == "Test Label"

def test_select():
    options = ["option1", "option2", "option3"]
    select = Select("test_select", "Test Select", options, multiple=True)
    assert select.name == "test_select"
    assert select.label == "Test Select"
    assert select.options == options
    assert select.multiple is True

def test_date_picker():
    date_picker = DatePicker("test_date", "Test Date", range=True)
    assert date_picker.name == "test_date"
    assert date_picker.label == "Test Date"
    assert date_picker.range is True

def test_button():
    button = Button("test_button", "Test Button", primary=True, variant="primary")
    assert button.name == "test_button"
    assert button.label == "Test Button"
    assert button.primary is True
    assert button.variant == "primary"

def test_sidebar():
    sidebar = Sidebar()
    assert len(sidebar.elements) == 0
    
    element = UIElement("test", "Test")
    sidebar.add_element(element)
    assert len(sidebar.elements) == 1
    assert sidebar.elements[0] == element

def test_create_sidebar():
    sidebar = create_sidebar()
    assert isinstance(sidebar, Sidebar)
    assert len(sidebar.elements) == 4
    
    # Check that all required elements are present
    elements = sidebar.elements
    assert isinstance(elements[0], Select)  # Layer control
    assert isinstance(elements[1], DatePicker)  # Time period
    assert isinstance(elements[2], Button)  # Analyze button
    assert isinstance(elements[3], Button)  # Export button
    
    # Check specific element properties
    layer_control = elements[0]
    assert layer_control.name == "active_layers"
    assert layer_control.multiple is True
    
    time_period = elements[1]
    assert time_period.name == "analysis_period"
    assert time_period.range is True
    
    analyze_button = elements[2]
    assert analyze_button.name == "run_analysis"
    assert analyze_button.primary is True
    
    export_button = elements[3]
    assert export_button.name == "export_results"
    assert export_button.variant == "secondary"
