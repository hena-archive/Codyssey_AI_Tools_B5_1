from DataStructure.double_linked_list import DoubleLinkedList 

class HashMap:
    # 생성자
    def __init__(self, size = 16):
        self.size = size
        self.key_count = 0
        self.keys = []
        self.load_factor = 0.75  # 기본 로드 팩터 설정
        self.threshold = int(self.size * self.load_factor)

        for _ in range(size):
            self.keys.append(DoubleLinkedList())  # 각 버킷을 리스트로 초기화

    # 메서드
    def put(self, key, value):
        print(f"Putting key: {key}, value: {value}")
        print(f"Hash index for key '{key}': {hash(key)} : {hash(key) % self.size}")
        index = hash(key) % self.size
        self.keys[index].insert_back((key, value))

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

        # 갱신
        self.threshold = int(self.size * self.load_factor)

        for _ in range(self.size):
            self.keys.append(DoubleLinkedList())

        for double_linked_list in old_keys:
            k, v = node.get_data()
            self.put(k, v) if self.size > self.threshold else None

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

        double_linked_list.print_list()
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
        dl = self.keys[index]

        dl.find()
        # print(f"Checking node with key: {node.get_data()[0]}")

    def contains_key(self, key):
        index = self.get_index(key)
        for dl in self.keys[index]:
            if dl.get_data_node(key):
                return True
        return False

    def get_key_count(self):
        return self.key_count


    def print_all(self):
        for i in range(self.size):
            print(f"Bucket {i}: ", end="")
            self.keys[i].print_list()
            print()

    def get_keys_array(self):
        pass
