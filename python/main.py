from DataStructure.double_linked_list import DoubleLinkedList

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

def main():
    print("Testing DoubleLinkedList...")
    test_linked_list()
    

if __name__ == "__main__":
    main()
