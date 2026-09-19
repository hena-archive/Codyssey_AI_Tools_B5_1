from DataStructure.hash_map import HashMap
from DataStructure.min_heap import MinHeap
from DataStructure.double_linked_list import DoubleLinkedList
from DataStructure.node import Node

import time

class MiniRedis:
    # 생성자
    def __init__(self):
        self.hash_map = HashMap()
        self.ttl = MinHeap()

        # key만 저장해도 될 거 같음.
        self.recent_use_list = DoubleLinkedList()

        self.total_bytes = 0
        self.max_bytes = 10**9
        self.evicted_keys_count = 0

        self.current_time = time.time()


    def run(self):
        while True:
            # 사용자 입력 받기
            request = input("mini-redis> ")
            
            self.current_time = time.time()
            print(self.current_time)
            self._clear_ttl()
            
            response = self._handle_request(request)
            print(response)

    def _parse_args(self, args):
        command = ""
        new_args = []

        if args[0] == "SET" or args[0] == "GET" or args[0] == "DEL" or args[0] == "EXISTS" or args[0] == "KEYS" or args[0] == "DBSIZE":
            command = args[0]
            new_args = args[1:]
            
        elif args[0] == "CONFIG":
            command = args[0] + " " +args[1] + " " + args[2]
            new_args = args[3:]
        elif args[0] == "INFO":
            command = args[0] + " " +args[1]
            new_args = args[2:]

        elif args[0] == "EXPIRE" or args[0] == "TTL":
            command = args[0]
            new_args = args[1:]
        else:
            print(f"Error {args[0]} \n")
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
        elif command == "CONFIG SET maxmemory":
            return True
        elif command == "EXPIRE":
            return True
        elif command == "TTL":
            return True
        return False

    def _print_input_command_and_args(self, command, args):
        print("========================== Input 확인 ===============================")
        print(f"Input Command : {command}")
        print(f"Input args : ")
        for arg in args:
            print(arg)
        print("="*60)
        print()


    def _handle_request(self, request):
        args = request.split()

        # 대충 파싱해보기
        command, args = self._parse_args(args)
        
        self._print_input_command_and_args(command, args)

        # 제대로 들어왔는지 확인하기
        check_flag = self._check_parse_validate(command, args)
        if check_flag == False:
            print("여기냐")
            return False

        result_message = ""

        # String 타입 명령어 6개
        # - SET, GET, DEL, EXISTS, DBSIZE, KEYS
        if command == "SET":
            result_message = self._set_command(args)
        elif command == "GET":
            result_message = self._get_command(args)
        elif command == "DEL":
            result_message = self._delete_command(args)
        elif command == "EXISTS":
            result_message = self._exists_command(args)
        elif command == "DBSIZE":
            result_message = self._get_db_size_command()
        elif command == "KEYS":
            result_message = self._keys_command()

        # 메모리 관리 명령어 (2개)
        # - CONFIG SET maxmemory, INFO memory
        elif command == "CONFIG SET maxmemory":
            result_message = self._config_set_maxmemory(args)
        elif command == "INFO memory":
            pass


        elif command == "EXPIRE":
            result_message = self._set_ttl(args)
        elif command == "TTL":
            result_message = self._get_ttl(args)
        else:
            result_message = "(error) ERR unknown command \"" + command +"\"" 
        # 출력
        print(result_message)
        return True

    def _set_command(self, args):
        # 파라메터 확인
        if len(args) != 2:
            return "(error) ERR wrong number of arguments for '<SET>' command"
       
        key = args[0]
        value = args[1]
    
        # key-value 크기 체크
        key_bytes = self._get_utf8_size(key)
        value_bytes = self._get_utf8_size(value)

        pair_bytes = key_bytes + value_bytes

        # 1. pair_bytes가 max보다 크냐
        if self._check_validate_size(pair_bytes) is False:
            return "(error) OOM command not allowed when used_memory > 'maxmemory"

        # 1. 키가 존재하는 지 확인
        entry = self._find_entry(key)
        if entry is not None:
            
            # lru 원칙에 의해 삭제
            self.recent_use_list.remove_node(entry.recent_node)

            # hash map에서 삭제 
            self.hash_map.remove(key)

            remove_key_bytes = self._get_utf8_size(entry.key)
            remove_value_bytes = self._get_utf8_size(entry.value)
            self.total_bytes -= (remove_key_bytes + remove_value_bytes)
    


        # 2. pair_bytes + total > max 보다 크다면 계속 삭제
        print(pair_bytes + self.total_bytes, self.max_bytes)
        while pair_bytes + self.total_bytes > self.max_bytes:
            data = self._remove_recent_list()
          
            entry = self._find_entry(data)
            self.hash_map.remove(data)
                        
            aa  = self._get_utf8_size(entry.key)
            bb = self._get_utf8_size(entry.value)
            self.total_bytes -= (aa + bb)
            

        # 키를 전달하고 만들어진 노드 반환
        recent_node = self.recent_use_list.insert_front(key)
        print(f"체크 {recent_node.data}")

        print(f"_set command : {key}, {value}, {recent_node}")

        self.hash_map.put(key, value, None, recent_node)

        self.total_bytes += pair_bytes

    # 완료
    def _get_command(self, args):
        if len(args) != 1:
            return "(error) ERR wrong number of arguments for '<GET>' command"
        
        key = args[0]

        entry = self._find_entry(key)
        if entry is None:
            return "(nil)"

        print(f"key: {entry.key}")
        print(f"value: {entry.value}")
        value_string = "\"" + entry.value + "\""

        # 이게 될까?
        if entry.expire_at is not None and entry.expire_at <= self.current_time:
            print("이게 가능하나? 테스트 필요")
            return "get_아몰랑"

        # 노드 앞으로 놓기
        self.recent_use_list.move_to_front(entry.recent_node)

        if entry.expire_at is not None and entry.expire_at <= self.current_time:
            print("이게 가능하나? 테스트 필요")
            return "get_아몰랑"

        return value_string

    def _delete_command(self, args):
        if len(args) != 1:
            return "(error) ERR wrong number of arguments for '<DEL>' command"

        key = args[0]

        entry = self._find_entry(key)
        if entry is None:
            return "(integer) 0"
        else:
            self.recent_use_list.remove_node(entry.recent_node)
            self.hash_map.remove(key)
            return "(integer) 1" 

    def _exists_command(self, args):
        if len(args) != 1:
            return "(error) ERR wrong number of arguments for '<EXISTS>' command"
        key = args[0]
        entry = self._find_entry(key)
        if entry is None:
            return "(integer) 0"
        else:
            return "(integer) 1"

    def _get_db_size_command(self):
        result_message = "(integer)"
        sizes = self.hash_map.get_key_count()
        result_message += str(sizes)
        return result_message

    def _keys_command(self):
        # 있는지 확인
        if self.hash_map.get_key_count() == 0:
            return "(empty array)"
        index = 1
        result_message = ""
        for i in range(self.hash_map.get_bucket_count()):
            dl = self.hash_map.keys[i]
            dl_size = dl.get_node_count()
            for _ in range(dl_size):
                result_message += f"{index}. {dl.get_last_node().data.key}"
                dl.move_to_front(dl.get_last_node()) 
                index += 1
        return result_message


    def _print_all_keys(self):
        self.recent_use_list.print_list()

    def _check_validate_size(self, input_bytes):
        if self.max_bytes == 0:
            return True
            
        if input_bytes <= self.max_bytes:
            return True

        print("말이 안되는 에러")
        return False

    def _find_entry(self, key):
        node = self.hash_map.get(key)
        if node is None:
            return None

        # entry
        return node.data




    def _print_all_command(self):
        self.hash_map.print_all()

    

    def _get_utf8_size(self, text):
        utf_bytes = len(text.encode("utf-8"))
        return utf_bytes

    # 메모리 관리 명령어 (완료)
    def _config_set_maxmemory(self, args):

        if len(args) != 1:
            return "(error) ERR wrong number of arguments for '<CONFIG SET maxmemory>' command"

        try:
            value = int(args[0])
            print(f"_config_set_maxmemory 변환 성공: {value}")
        except ValueError:
            return "(error) ERR value is not an integer or out of range"
            
        # 음수 예외 처리(규정은 없음)
        if value < 0:
            return "[Error] 음수는 불가하다"
        elif value > 0:
            self.max_bytes = 10 ** 9
        else:
            # 값 변경
            self.max_bytes = value

        # Todo 삭제 예정
        self._print_memory_info()
        
        return "OK"

    

    def _set_ttl(self, args):
        if len(args) != 2:
            return "(error) ERR wrong number of arguments for '<TTL>' command"

        key = args[0]

        try:
            seconds = int(args[1])
            print(f"_set_ttl 변환 성공: {seconds}")
        except ValueError:
            return "(error) ERR value is not an integer or out of range"

        # 키 여부 확인
        entry = self._find_entry(key)
        if entry is None:
            return "(integer) 0"

        if seconds <= 0:
            self._delete_command(entry.key)
            return "(integer) 1"

        now_time = time.time()
        next_expire_at = now_time + seconds

        if entry.expire_at is None:
            entry.expire_at = next_expire_at

        elif entry.expire_at >= now_time:
            entry.expire_at = next_expire_at
        

        self.ttl.insert((next_expire_at, key))
        self._print_heap_data()
        return "(integer) 1"

    def _get_ttl(self, args):

        if len(args) != 1:
            return "(error) ERR wrong number of arguments for '<TTL>' command"

        key = args[0]

        # 키 여부 확인
        entry = self._find_entry(key)

        # 키 없는 경우
        if entry is None:
            return "(Integer)-2"
        
        if entry.expire_at is None:
            return "(Integer)-1"
        

        now_time = time.time()
        remain_time = entry.expire_at - now_time

        if remain_time >= 0:
            print(f"남은시간: {int(remain_time)} 초")
            return f"(Integer){int(remain_time)}"
        else:
            self._delete_command([entry.key])

            return "(Integer) 0(만료)"

    def _print_info_memory_command(self):
        pass

    def _remove_recent_list(self):
        data = self.recent_use_list.remove_back()
        return data    

    

    # Debug 용도
    def _print_recent_list(self):
        print("===================== print_recent_list =========================")
        self.recent_use_list.print_list()
        print("=================================================================\n\n")


    def _print_memory_info(self):
        print("===================== print_max_memory_size =====================")
        print(f"current total size : {self.total_bytes} ")
        print(f"max bytes          : {self.max_bytes} ")
        print("=================================================================\n\n")


    def _print_heap_data(self):
        print("===================== print_heap_data =====================")
        self.ttl.print_data()
        print("===========================================================\n\n")

    def _clear_ttl(self):

        print("====================== ttl을 정리합니다 ====================")
        while (True):
            # 빈 경우
            expire_data = self.ttl.extract_min()
            if expire_data is None:
                break

            expire_at, key = expire_data
            entry = self._find_entry(key)
            if entry is None:
                continue

            if entry.expire_at == expire_at:
                print(f"삭제할 키: {entry.key} 삭제할 value:{entry.value}")
                print(f"expire 시간: {entry.expire_at} node:{entry.recent_node}")
                self._delete_command([entry.key])

        print("==========================================================")
        print()
        