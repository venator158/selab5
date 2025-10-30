"""Inventory management system for tracking stock items."""
import json
from datetime import datetime

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add an item to the inventory.

    Args:
        item: Name of the item to add
        qty: Quantity to add
        logs: List to append log messages to

    Returns:
        bool: True if item was added successfully, False otherwise
    """
    if logs is None:
        logs = []

    # Validation checks
    success = True
    error_msg = ""

    if not isinstance(item, str):
        error_msg = f"Error: Item name must be a string, got {type(item).__name__}"
        success = False
    elif not isinstance(qty, (int, float)):
        error_msg = f"Error: Quantity must be a number, got {type(qty).__name__}"
        success = False
    elif not item or item.strip() == "":
        error_msg = "Error: Item name cannot be empty"
        success = False
    elif qty < 0:
        error_msg = f"Error: Cannot add negative quantity ({qty}) for item '{item}'"
        success = False

    if not success:
        print(error_msg)
    else:
        # Add item to inventory
        stock_data[item] = stock_data.get(item, 0) + qty
        logs.append(f"{datetime.now()}: Added {qty} of {item}")

    return success


def remove_item(item, qty):
    """Remove an item from the inventory.

    Args:
        item: Name of the item to remove
        qty: Quantity to remove

    Returns:
        bool: True if item was removed successfully, False otherwise
    """
    # Validation checks
    success = True
    error_msg = ""

    if not isinstance(item, str):
        error_msg = f"Error: Item name must be a string, got {type(item).__name__}"
        success = False
    elif not isinstance(qty, (int, float)):
        error_msg = f"Error: Quantity must be a number, got {type(qty).__name__}"
        success = False
    elif not item or item.strip() == "":
        error_msg = "Error: Item name cannot be empty"
        success = False
    elif qty <= 0:
        error_msg = f"Error: Quantity to remove must be positive, got {qty}"
        success = False
    elif item not in stock_data:
        error_msg = f"Error: Item '{item}' not found in inventory"
        success = False
    elif stock_data[item] < qty:
        error_msg = f"Error: Cannot remove {qty} of '{item}', only {stock_data[item]} available"
        success = False

    if not success:
        print(error_msg)
    else:
        # Remove item from inventory
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]

    return success


def get_qty(item):
    """Get the quantity of an item in inventory.

    Args:
        item: Name of the item

    Returns:
        int: Quantity of the item, or 0 if not found
    """
    # Validation and result
    result = 0

    if not isinstance(item, str):
        print(f"Error: Item name must be a string, got {type(item).__name__}")
    elif not item or item.strip() == "":
        print("Error: Item name cannot be empty")
    else:
        result = stock_data.get(item, 0)

    return result


def _validate_load_data_inputs(file):
    """Helper function to validate load_data inputs."""
    if not isinstance(file, str):
        return False, f"Error: File path must be a string, got {type(file).__name__}"
    if not file or file.strip() == "":
        return False, "Error: File path cannot be empty"
    return True, ""


def _validate_json_data(data):
    """Helper function to validate loaded JSON data."""
    if not isinstance(data, dict):
        return False, "Error: Invalid data format in file - expected dictionary"

    for key, value in data.items():
        if not isinstance(key, str):
            return False, f"Error: Invalid item name '{key}' - must be string"
        if not isinstance(value, (int, float)) or value < 0:
            return False, (f"Error: Invalid quantity '{value}' for item '{key}' - "
                          f"must be non-negative number")
    return True, ""


def load_data(file="inventory.json"):
    """Load inventory data from a JSON file.

    Args:
        file: Path to the JSON file

    Returns:
        bool: True if data was loaded successfully, False otherwise
    """
    global stock_data  # pylint: disable=global-statement

    # Validate inputs
    valid, error_msg = _validate_load_data_inputs(file)
    if not valid:
        print(error_msg)
        return False

    # Try to load and validate data
    success = False
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.loads(f.read())

        valid, error_msg = _validate_json_data(data)
        if valid:
            stock_data = data
            success = True
        else:
            print(error_msg)

    except FileNotFoundError:
        print(f"Error: File '{file}' not found")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{file}': {e}")
    except PermissionError:
        print(f"Error: Permission denied accessing file '{file}'")
    except (OSError, IOError) as e:
        print(f"Error loading data from '{file}': {e}")

    return success
def save_data(file="inventory.json"):
    """Save inventory data to a JSON file.

    Args:
        file: Path to the JSON file

    Returns:
        bool: True if data was saved successfully, False otherwise
    """
    # Validation checks
    success = True
    error_msg = ""

    if not isinstance(file, str):
        error_msg = f"Error: File path must be a string, got {type(file).__name__}"
        success = False
    elif not file or file.strip() == "":
        error_msg = "Error: File path cannot be empty"
        success = False

    if success:
        try:
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(stock_data, indent=2))
        except PermissionError:
            error_msg = f"Error: Permission denied writing to file '{file}'"
            success = False
        except (OSError, IOError) as e:
            error_msg = f"Error saving data to '{file}': {e}"
            success = False

    if not success:
        print(error_msg)

    return success


def print_data():
    """Print the current inventory report."""
    print("Items Report")
    for item_name in stock_data:
        print(item_name, "->", stock_data[item_name])


def check_low_items(threshold=5):
    """Check for items below a threshold quantity.

    Args:
        threshold: Minimum quantity threshold

    Returns:
        List of items below the threshold, or empty list if error
    """
    # Validation and result
    result = []

    if not isinstance(threshold, (int, float)):
        print(f"Error: Threshold must be a number, got {type(threshold).__name__}")
    elif threshold < 0:
        print(f"Error: Threshold must be non-negative, got {threshold}")
    else:
        for item_name in stock_data:
            if stock_data[item_name] < threshold:
                result.append(item_name)

    return result


def main():
    """Main function to demonstrate the inventory system."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # invalid types, no check
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    print('eval not used')


if __name__ == "__main__":
    main()
