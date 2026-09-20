from DataStructure.double_linked_list import DoubleLinkedList 
from Redis.entry import Entry

class HashMap:
    # 생성자
    def __init__(self, size = 8):
        self.size = size
        self.key_count = 0
        self.keys = []
        self.load_factor = 0.75  # 기본 로드 팩터 설정
        self.threshold = int(self.size * self.load_factor)

        for _ in range(size):
            self.keys.append(DoubleLinkedList())  # 각 버킷을 리스트로 초기화

    # 메서드
    def put(self, key, value, expire, lru_node_ptr):
        print(f"Putting key: {key}, value: {value}")
        print(f"Hash index for key '{key}': {hash(key)} : {hash(key) % self.size}")
        index = hash(key) % self.size

        new_node = Entry(key, value, expire, lru_node_ptr)

        self.keys[index].insert_back(new_node)

        # key 개수 증가
        self.key_count += 1

        # factor 계산
        if self.threshold <= self.key_count:
            self.rehash()

    def rehash(self):
        """
        해시 맵의 크기를 두 배로 늘리고 모든 키-값 쌍을 재배치합니다.
        """

        # 키 임시 저장
        old_keys = self.keys
        self.size *= 2
        self.keys = []
        self.key_count = 0
        # 갱신
        
        self.threshold = int(self.size * self.load_factor)
        print(f"Test threash:{self.threshold}")

        for _ in range(self.size):
            self.keys.append(DoubleLinkedList())

        for double_linked_list in old_keys:
            datas = double_linked_list.get_list_data()
            for data in datas:

                self.put(data.key, data.value, data.expire_at, data.recent_node)

    # def custom_hash(self, key):
    #     """
    #     사용자 정의 해시 함수를 구현하는 메서드입니다.
    #     이 예제에서는 간단히 문자열의 길이를 해시 값으로 사용합니다.
    #     """

    #     total = 0

    #     for alpha in key:
    #         total += ord(alpha)
    #     return total % self.size

    def get(self, key):
        """
        사용자 정의 해시 함수를 구현하는 메서드입니다.
        이 예제에서는 간단히 문자열의 길이를 해시 값으로 사용합니다.
        """
        
        # 해시 값을 계산하여 해당 버킷의 인덱스를 찾습니다.
        index = hash(key) % self.size

        double_linked_list = self.keys[index]

        find_node = self._find_node(key)
        
        if find_node is None:
            return None
        return find_node
        # for node in double_linked_list:
        #     k, v = node.get_data()
        #     if k == key:
        #         return v

        
        return None

    def get_index(self, key):
        """
        index를 반환하는 메서드입니다.
        """
        return hash(key) % self.size

    def remove(self, key):
        index = self.get_index(key)
        bucket = self.keys[index]

        node = self._find_node(key)
        if node is None:
            return None

        self.key_count -= 1
        
        bucket.remove_node(node)
        return node
        # print(f"Checking node with key: {node.get_data()[0]}")

    def contains_key(self, key):
        
        find_key = self._find_node(key)
        
        if find_key is None:
            return False
        print(find_key.data)
        return True

    def _find_node(self, key):
        index = self.get_index(key)
        bucket = self.keys[index]

        # head는 스킵
        current = bucket.head.next

        while current is not bucket.tail:
            entry = current.data

            if entry.key == key:
                return current

            current = current.next

        return None

    def get_key_count(self):
        return self.key_count

    def get_bucket_count(self):
        return len(self.keys)

    def print_all(self):
        for i in range(self.size):
            print(f"Bucket {i}: ", end="")
            datas = self.keys[i].get_list_data()
            for data in datas:
                print(f"[{data.key}], ", end="")
                
            print()

    def get_keys_array(self):
        pass
