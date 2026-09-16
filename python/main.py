from DataStructure.double_linked_list import DoubleLinkedList
from DataStructure.hash_map import HashMap

from Redis.mini_redis import MiniRedis

def test_linked_list():
    dl = DoubleLinkedList()

    # Test insertions
    dl.insert_front(10)
    dl.insert_back(20)
    dl.insert_back(30)

    # Test removals
    dl.remove_front()
    dl.remove_back()

    # Test print
    dl.print_list()

def test_hash_map():
    

    hm = HashMap()

    # Test put
    hm.put("apple", 1)
    hm.put("banana", 2)
    hm.put("orange", 3)

    # Test get
    print(hm.get("apple"))   # Should print 1
    print(hm.get("banana"))  # Should print 2
    print(hm.get("orange"))  # Should print 3
    print(hm.get("grape"))   # Should print None

    # Test remove
    hm.remove("banana")
    print(hm.get("banana"))  # Should print None

    hm.print_all()


def main():
    # print("Testing DoubleLinkedList...")
    # test_linked_list()

    # print("\nTesting HashMap...")
    # test_hash_map()

    mini_redis = MiniRedis()

    mini_redis.run()
    

if __name__ == "__main__":
    main()
