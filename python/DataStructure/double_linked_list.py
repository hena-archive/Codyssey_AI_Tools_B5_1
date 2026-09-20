from DataStructure.node import Node

class DoubleLinkedList:
    # 생성자
    def __init__(self):
        self.head = Node(-1)
        self.tail = Node(-1)
        
        self.node_count = 0

        self.head.next = self.tail
        self.tail.prev = self.head

    # 요구사항 메서드 인터페이스
    def insert_front(self, data):
        """
        head에 새로운 노드를 추가하는 메서드입니다.
        시간 복잡도 O(1)로, 상수 시간 내에 새로운 노드를 head에 추가할 수 있습니다.
        """

        # 새로운 노드를 생성하고 데이터를 할당합니다.
        new_node = Node(data)

        # 새로운 노드와 head 다음 노드를 연결합니다.
        new_node.next = self.head.next
        self.head.next.prev = new_node

        #궁금하네. 값을 받고 하는 방식이면 어떻게 작동할지.

        # 새로운 노드와 head 노드를 연결합니다.
        new_node.prev = self.head
        self.head.next = new_node

        self.node_count += 1

        return new_node

    def insert_back(self, data):
        """
        tail에 새로운 노드를 추가하는 메서드입니다.
        시간 복잡도 O(1)로, 상수 시간 내에 새로운 노드를 tail에 추가할 수 있습니다.
        """       

        # 새로운 노드를 생성하고 데이터를 할당합니다.
        new_node = Node(data)

        # 새로운 노드와 tail 이전 노드를 연결합니다.
        new_node.prev = self.tail.prev
        self.tail.prev.next = new_node

        # 새로운 노드와 tail 노드를 연결합니다.
        new_node.next = self.tail
        self.tail.prev = new_node
        
        self.node_count += 1

        return new_node

    def remove_front(self):
        """
        head에서 노드를 제거하는 메서드입니다.
        시간 복잡도 O(1)로, 상수 시간 내에 head에서 노드를 제거할 수 있습니다.
        """

        # 리스트가 빈 경우, 제거할 노드가 없으므로 None을 반환합니다.
        if self.head.next is self.tail:
            return None

        # 제거할 노드 임시 저장
        removed_node = self.head.next
        removed_data = removed_node.data

        self.head.next = removed_node.next
        removed_node.next.prev = self.head
  
        self.node_count -= 1

        return removed_data

    def remove_back(self):
        """
        tail에서 노드를 제거하는 메서드입니다.
        시간 복잡도 O(1)로, 상수 시간 내에 tail에서 노드를 제거할 수 있습니다.
        """

        # 리스트가 빈 경우, 제거할 노드가 없으므로 None을 반환합니다.
        if self.tail.prev is self.head:
            return None

        # 제거할 노드 임시 저장
        removed_node = self.tail.prev
        removed_data = removed_node.data

        self.tail.prev = removed_node.prev
        removed_node.prev.next = self.tail

        self.node_count -= 1

        return removed_data

    def remove_node(self, node):
        """
        주어진 노드를 제거하는 메서드입니다.
        시간 복잡도 O(1)로, 상수 시간 내에 주어진 노드를 제거할 수 있습니다.
        """

        # 비정상적인 예외 처리
        if node is None or node.prev is None or node.next is None:
            return None

        node.prev.next = node.next
        node.next.prev = node.prev

        # 심어놓기
        node.prev = None
        node.next = None

        self.node_count -= 1

        return node

    def move_to_front(self, node):
        if node is None or node == self.head:
            return
        self.remove_node(node)
        self.insert_front(node.data)

    def move_to_back(self, node):
        if node is None or node == self.head:
            return
        self.remove_node(node)
        self.insert_back(node.data)

    # 테스트 용도 함수
    def print_list(self):
        current = self.head.next
        while current is not self.tail:
            print(current.data, end=" ")
            current = current.next
        print()

    def get_list_data(self):
        data = []
        current = self.head.next
        while current is not self.tail:
            data.append(current.data)
            current = current.next
        return data

    def get_first_node(self):
        if self.head.next is self.tail:
            return None
        return self.head.next

    def get_last_node(self):
        if self.tail.prev is self.head:
            return None
        return self.tail.prev

    def get_data_node(self, key):
        current = self.head.next
        while current is not self.tail:
            if current.data == key:
                return current
            current = current.next
        return None

    # def get_node_by_search_key(self):


    def get_node_count(self):
        return self.node_count

    def get_node_count_by_travel(self):
        count = 0

        while current is not self.tail:
            count += 1
            current = current.next

        return count