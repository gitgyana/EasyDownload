from metadata import *


print("Testing get() ")
update(integer_key=10, string_key="Initial String")
print("integer_key:", get('integer_key'))  # Expected output: 10
print("string_key:", get('string_key'))    # Expected output: "Initial String"
update(integer_key=20, float_key=1.0)
update(integer_key=30, float_key=0.8)
print("integer_key:", get('integer_key'))  # Expected output: 60
print("float_key:", get('float_key'))      # Expected output: 1.8
print("string_key:", get('string_key'))    # Expected output: "Initial String"

# Test 2: Test `get()` with non-existing keys (should create them with default values)
print("\nTesting get() with non-existing keys...")
print("non_existing_key:", get('non_existing_key', default=''))  # Expected output: '' (default string)
print("another_non_existing_key:", get('another_non_existing_key', default=''))  # Expected output: '' (default string)

# Test 3: Test `get()` with multiple keys at once (some exist, some don't)
print("\nTesting get() with multiple keys (mix of existing and non-existing)...")
print("integer_key and new_key:", get('integer_key', 'new_key'))  # Expected output: { 'integer_key': 10, 'new_key': '' }
print("string_key and missing_key:", get('string_key', 'missing_key'))  # Expected output: { 'string_key': "Initial String", 'missing_key': '' }

# Test 4: Test `update()` with existing keys (update the values)
print("\nTesting update() with existing keys...")
update(integer_key=20, string_key="Updated String")
print("Updated integer_key:", get('integer_key'))  # Expected output: 20
print("Updated string_key:", get('string_key'))    # Expected output: "Updated String"

# Test 5: Test `update()` with new keys (should add new keys to the data)
print("\nTesting update() with new keys...")
update(new_integer_key=100, new_string_key="New String Value")
print("new_integer_key:", get('new_integer_key'))  # Expected output: 100
print("new_string_key:", get('new_string_key'))    # Expected output: "New String Value"

# Test 6: Test `update()` where a non-existing key is passed (should create the key first)
print("\nTesting update() with non-existing keys passed as arguments...")
update(non_existing_key_int=50, non_existing_key_str="Non-existing String")
print("non_existing_key_int:", get('non_existing_key_int'))  # Expected output: 50
print("non_existing_key_str:", get('non_existing_key_str'))  # Expected output: "Non-existing String"

delete()
clear()

# Test 7: Add some initial values
print("\nInitial Data:")
update(integer_key=10, string_key="Initial String", boolean_key=True, float_key=3.14)
print("integer_key:", get('integer_key'))
print("string_key:", get('string_key'))
print("boolean_key:", get('boolean_key'))
print("float_key:", get('float_key'))

# Test 8: Test adding values to a list
print("\nTesting update with list:")
update(list_key=[1, 2, 3])  # Initial list
print("list_key after first update:", get('list_key'))  # Expected output: [1, 2, 3]
update(list_key=[4, 5])  # Adding more values
print("list_key after second update:", get('list_key'))  # Expected output: [1, 2, 3, 4, 5]

# Test 9: Test updating a dictionary
print("\nTesting update with dict:")
update(dict_key={'name': 'John', 'age': 30})  # Initial dictionary
print("dict_key after first update:", get('dict_key'))  # Expected output: {'name': 'John', 'age': 30}
update(dict_key={'location': 'NYC'})  # Adding another key-value pair
print("dict_key after second update:", get('dict_key'))  # Expected output: {'name': 'John', 'age': 30, 'location': 'NYC'}

# Test 10: Test adding invalid type (tuple)
print("\nTesting update with tuple:")
try:
    update(tuple_key=(1, 2, 3))  # Tuples should raise an error
except ValueError as e:
    print(f"Error encountered: {e}")  # Expected to raise ValueError: Unsupported type: <class 'tuple'>

# Test 11: Test updating a boolean value
print("\nTesting update with boolean:")
update(boolean_key=False)  # Update with new boolean value
print("boolean_key after update:", get('boolean_key'))  # Expected output: False

# Test 12: Test updating a string value
print("\nTesting update with string:")
update(string_key="Updated String")  # Update string key
print("string_key after update:", get('string_key'))  # Expected output: "Updated String"

# Test 13: Test updating with a new key-value pair
print("\nTesting update with a new key-value pair:")
update(new_key="New Value")  # Adding a new key-value pair
print("new_key after update:", get('new_key'))  # Expected output: "New Value"

# Test 14: Reset Existing Keys
print("\nTesting reset() with existing keys...")
update(integer_key=10, string_key="Test String")
print("Before reset:")
print("integer_key:", get('integer_key'))  # Expected output: 10
print("string_key:", get('string_key'))    # Expected output: "Test String"
reset('integer_key', 'string_key')
print("After reset:")
print("integer_key:", get('integer_key'))  # Expected output: 0
print("string_key:", get('string_key'))    # Expected output: "" (default string)

# Test 15: Reset Non-Existing Keys
print("\nTesting reset() with non-existing keys...")
reset('non-existing_new_key')
print("non-existing_new_key:", get('non-existing_new_key'))  # Expected output: "" (default string)

# Test 16: Reset Multiple Keys
print("\nTesting reset() with multiple keys (existing and non-existing)...")
update(integer_key=5, another_new_key="Key")
print("integer_key:", get('integer_key'))  # Expected output: 5
print("another_new_key:", get('another_new_key'))  # Expected output: "Key"
reset('integer_key', 'another_new_key')
print("integer_key:", get('integer_key'))  # Expected output: 0
print("another_new_key:", get('another_new_key'))  # Expected output: "" (default string)

# Test 17: Reset Multiple Keys with Mixed Existing and Non-Existing Keys
print("\nTesting reset() with mixed existing and non-existing keys...")
update(string_key="Hello")
print("string_key:", get('string_key'))  # Expected output: "Hello"
reset('string_key', 'non_existin_new_key')
print("string_key:", get('string_key'))  # Expected output: "" (default string)
print("non_existin_new_key:", get('non_existin_new_key'))  # Expected output: "" (default string)


delete()
