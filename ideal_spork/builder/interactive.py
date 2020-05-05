# interactive helpers

# select an item from a list
def select_from_list(items, name="Thing"):
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
            print("Not a number")
            continue
        if val > count:
            print("Selection out of range")
            continue
        break
    return items[val]
