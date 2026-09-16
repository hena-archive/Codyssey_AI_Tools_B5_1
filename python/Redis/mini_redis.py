from DataStructure.hash_map import HashMap
from DataStructure.min_heap import MinHeap
from DataStructure.double_linked_list import DoubleLinkedList

import time

class MiniRedis:
    def __init__(self):
        self.hash_map = HashMap()
        self.priority_queue = MinHeap()

        # key만 저장해도 될 거 같음.
        self.recent_use_list = DoubleLinkedList()

        self.total_bytes = 0

    

    def run(self):
        while True:
            # 사용자 입력 받기
            request = input("mini-redis> ")
            
            print(time.time())

            response = self._handle_request(request)
            print(response)

    def _parse_args(self, args):
        command = ""
        new_args = []

        if args[0] == "SET" or args[0] == "GET" or args[0] == "DEL" or args[0] == "EXISTS" or args[0] == "KEYS" or args[0] == "DBSIZE":
            command = args[0]
            new_args = args[1:]
            
        elif args[0] == "CONFIG" or args[0] == "INFO":
            command = args[0] + " " +args[1]
            new_args = args[2:]
            
        elif args[0] == "EXPIRE" or args[0] == "TTL":
            command = args[0]
            new_args = args[1:]
        else:
            print("Error\n")
        return command, new_args

    def _check_parse_validate(self, command, args):
        if command == "SET":
            return True
        elif command == "GET":
            return True
        elif command == "DEL":
            return True
        elif command == "EXISTS":
            return True
        elif command == "KEYS":
            return True
        elif command == "DBSIZE":
            return True
        return False


    def _handle_request(self, request):
        args = request.split()

        # 대충 파싱해보기
        command, args = self._parse_args(args)

        # 제대로 들어왔는지 확인하기
        check_flag = self._check_parse_validate(command, args)
        if check_flag == False:
            return False

        if command == "SET":
            self._set_command(args[0], args[1])
        if command == "GET":
            self._get_command(args[0])
        if command == "DEL":
            self._delete_command(args[0])

        if command == "DBSIZE":
            self._get_db_size_command()
        if command == "KEYS"
            self._print_all_command()
        self._print_all_command()
        return True

    def _get_command(self, key):
        self.hash_map.get(key)

    def _set_command(self, key, value):
        self.hash_map.put(key, value)

    def _delete_command(self, key):
        self.hash_map.remove(key)

    def _exists_command(self, key):
        return key in self.hash_map

    def _print_all_command(self):
        self.hash_map.print_all()

    def _get_db_size_command(self):
        result = "(integer)"
        sizes = self.hash_map.get_key_count()
        result += str(sizes)
        print(result)

    # 메모리 관리
    def CONFIG SET maxmemory bytes(self):
        pass

    def _print_info_memory_command(self):
        print("used_memory:<number> maxmemory:<number> evicted_keys:<number>")
        pass