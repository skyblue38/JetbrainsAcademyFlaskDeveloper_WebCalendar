def print_list(some_list):
    i = 0
    while i in range(len(some_list)):
        # print(type(some_list[i]))
        if isinstance(some_list[i], str):
            if some_list[i].isdigit():
                sl1 = int(some_list[i])
            else:
                print()
        else:
            sl1 = some_list[i]        
        if sl1 % 2 == 0:
            print(some_list[i])
        if sl1 % 3 == 0:
            print(sl1 % 3)
        i += 1
