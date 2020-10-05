class Node:
    def __init__(self,key,value):
        self.value = value
        self.key = key
        self.next = next

class HashTable:
    def __init__(self,capacity):
        self.hash_array = [None] * capacity

    def hash_fn(self,s):
        encoded_string = s.encode()
        result = 0
        for binary_char in encoded_string:
            result += binary_char
        print(result)
        return result
    def hash_index(self, key):
        hash_value = self.hash_fn(key)
        index = hash_value % len(self.hash_array)
        return index

    def put(self,key,value):
        
        index = self.hash_index(key)
        if self.hash_array[index] is not None:
            print("COLLISION ALERT")
        self.hash_array[index] = Node(key,value)

    def get(self,key):
        hash_value = self.hash_fn(key)
        

        index = hash_value % len(self.hash_array)
        return self.hash_array[index].value

table = HashTable(4)
table.put('banana', 'is yellow')
table.put('nabana', "is green")
print(table.hash_array)
print(table.get('banana'))