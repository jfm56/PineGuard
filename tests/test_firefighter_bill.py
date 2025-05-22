import pytest
import app.firefighter_bill as firefighter_bill

def test_firefighter_bill_module_exists():
    assert hasattr(firefighter_bill, "__doc__")
