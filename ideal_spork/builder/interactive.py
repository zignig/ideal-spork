# interactive helpers

__all__ = ["select_from_list", "get_name"]

# select an item from a list
def select_from_list(items, name="Thing", as_num=False):
    " select by number "
    count = len(items)
    val = 0
    while True:
        print("\nPlease select a", name)
        print()
        for num, item in enumerate(items):
            print("{:>4}  {}".format(num, item))
        print()
        val = input("Select from " + str(count) + " " + name + ">")
        try:
            val = int(val)
        except:
            print("\nNot a number")
            continue
        if val > (count - 1):
            print("Selection out of range")
            continue
        break
    if as_num:
        return val
    else:
        return items[val]


def get_name(prompt, default):
    " ask for a name with defaults"
    val = input(prompt + " (default=" + default + ") >")
    if val == "":
        val = default
    return val
