class HashTableEntry:
    """
    Linked List hash table key/value pair
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys
    Implement this.
    """

    def __init__(self, capacity):
        # Your code here
        self.capacity = capacity
        self.hash_list = [None]*self.capacity

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)
        One of the tests relies on this.
        Implement this.
        """
        # Your code here
        return len(self.hash_list)
        # return self.capacity

    def get_load_factor(self):
        """
        Return the load factor for this hash table.
        Implement this.
        """
        # Your code here
        return len([item for item in self.hash_list if item is not None]) / self.capacity

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit
        Implement this, and/or DJB2.
        Based on https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function#FNV-1_hash
        """

        # Your code here
        string_to_bytes = str(key).encode()
        FNV_offset_basis = 14695981039346656037
        FNV_prime = 1099511628211
        for b in string_to_bytes:
            hash_value = FNV_offset_basis*FNV_prime
            hash_value = hash_value ^ b
        return hash_value

    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        Implement this, and/or FNV-1.
        """
        # Your code here

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.fnv1(key) % self.capacity
        # return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.
        Hash collisions should be handled with Linked List Chaining.
        Implement this.
        """
        # Your code here
        #self.hash_list[self.hash_index(key)] = value

        # determine where the hash shoud go
        slot = self.hash_index(key)
        # if that spot is empty, put it in
        if self.hash_list[slot] is None:
            self.hash_list[slot] = HashTableEntry(key, value)
        else:  # there's a collision!
            cur = self.hash_list[slot]
            while cur.next is not None and cur.key != key:
                cur = cur.next
            if cur.key == key:  # replace with new value
                cur.value = value
            else:  # add the new key/value pair
                cur.next = HashTableEntry(key, value)

        # auto resize if load factor too big after adding
        if self.get_load_factor() > .7:
            self.resize(self.capacity*2)

        return self

    def delete(self, key):
        """
        Remove the value stored with the given key.
        Print a warning if the key is not found.
        Implement this.
        """
        # Your code here
        slot = self.hash_index(key)
        cur = self.hash_list[slot]
        if cur is None:  # can't find the key
            print("Couldn't find that key!")
        elif cur.key == key:  # if pointing to key to delete, skip over and point to next
            self.hash_list[slot] = cur.next
        else:  # traverse the list until we find the key and skip over it
            while cur.next.key != key and cur.next is not None:
                cur = cur.next
            if cur.next.key == key:
                cur.next = cur.next.next
            else:
                print("Couldn't find that key!")

        # auto resize if load factor too small after deleting down to a min of 8
        if self.get_load_factor() < .2:
            if self.capacity > 16:
                self.resize(self.capacity//2)
            else:
                self.resize(8)

        # try:
        #     self.hash_list[slot] = None
        # except:
        #     print("Couldn't find that key!")

        return self

    def get(self, key):
        """
        Retrieve the value stored with the given key.
        Returns None if the key is not found.
        Implement this.
        """
        # Your code here
        # try:
        #     return self.hash_list[self.hash_index(key)]
        # except:
        #     return None
        slot = self.hash_index(key)
        try:
            if self.hash_list[slot] is not None:
                cur = self.hash_list[slot]

                while cur.key != key:
                    cur = cur.next
                return cur.value
        except:
            return None

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.
        Implement this.
        """
        # Your code here
        # make list of all values in current hash list
        all_values = [value for value in self.hash_list if value is not None]
        # set the new hash list size and re-initialize the list
        self.capacity = new_capacity
        self.hash_list = [None]*new_capacity
        while all_values:  # loop until list is empty
            # take first value and put into new hash list
            cur = all_values.pop()
            self.put(cur.key, cur.value)
            # process remaining values
            while cur.next is not None:
                cur = cur.next
                self.put(cur.key, cur.value)

        return self


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")