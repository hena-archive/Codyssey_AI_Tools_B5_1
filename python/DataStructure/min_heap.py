class MinHeap:
    # 생성자
    def __init__(self):
        self.data = []

    # 메서드
    def insert(self, value):
        """
        힙에 값을 추가하는 메서드입니다.
        """

        # 배열의 마지막에 값을 추가
        self.data.append(value)

        # 힙 속성을 유지하기 위해 위로 올림
        self._heapify_up()

    def top(self):
        """
        힙에서 최솟값을 반환하는 메서드입니다.
        """

        # 힙이 비어있으면 None을 반환
        if len(self.data) == 0:
            return None

        # 힙의 최솟값은 배열의 첫 번째 요소이므로 반환
        return self.data[0]

    def extract_max(self):
        """
        힙에서 최솟값을 제거하고 반환하는 메서드입니다.
        """

        # root 값 저장
        root = self.top()
        if root is None:
            return None

        # 마지막 요소를 root로 이동
        self.data[0] = self.data.pop()

        # 힙 속성을 유지하기 위해 아래로 내림
        self._heapify_down()
        return root

    def _heapify_up(self):
        """
        힙 속성을 유지하기 위해 마지막 요소를 위로 올리는 메서드입니다.
        """

        index = len(self.data) - 1
        while index > 0:
            parent = (index - 1) // 2
            if self.data[index] < self.data[parent]:
                self.data[index], self.data[parent] = self.data[parent], self.data[index]
                index = parent
            else:
                break

    def _heapify_down(self):
        """
        힙 속성을 유지하기 위해 root 요소를 아래로 내리는 메서드입니다.
        """

        index = 0
        while index < len(self.data):
            # 0-based index에서 왼쪽 자식과 오른쪽 자식의 인덱스를 계산
            left = 2 * index + 1
            right = 2 * index + 2

            # 현재 노드와 자식 노드 중 가장 작은 값을 가진 노드의 인덱스를 찾음
            smallest = index

            # 왼쪽 자식이 존재하고, 왼쪽 자식이 현재 노드보다 작으면 smallest를 왼쪽 자식으로 업데이트
            if left < len(self.data) and self.data[left] < self.data[smallest]:
                smallest = left
            # 오른쪽 자식이 존재하고, 오른쪽 자식이 현재 smallest보다 작으면 smallest를 오른쪽 자식으로 업데이트
            if right < len(self.data) and self.data[right] < self.data[smallest]:
                smallest = right

            # 만약 smallest가 현재 노드의 인덱스와 다르면, 두 노드를 교환하고 index를 smallest로 업데이트
            if smallest != index:
                self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
                index = smallest
            else:
                break