# Direct hash table using a simple identity or modulo hash function

# Let's define the hash table size
TABLE_SIZE = 10

# Create an empty hash table (list with None values)
hash_table = [None] * TABLE_SIZE

# Define a direct hash function (using modulo to fit in table)
def direct_hash(key):
    return key % TABLE_SIZE

# Insert a key-value pair
def insert(key, value):
    index = direct_hash(key)
    hash_table[index] = value
    print(f"Inserted key={key} at index={index}")

# Retrieve a value by key
def get(key):
    index = direct_hash(key)
    return hash_table[index]

