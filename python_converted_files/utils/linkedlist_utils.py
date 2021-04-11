class Node:

    def __init__(self, *args):

        if len(args) == 0:
            self.data = None
            self.next = None
        elif len(args) == 1:
            self.data = args[0]
            self.next = None
        elif len(args) == 2:
            self.data = args[0]
            self.next = args[1]


def create_head_from_list(items: list):
    head = None
    last = None
    while items:
        elem = items.pop(0)
        if head:
            p = Node(elem)
            last.next = p
            last = p
        else:
            head = Node(elem)
            last = head
    
    return head

def traverse_link_list(head):

    p = head
    while p:
        print(p.data)
        p = p.next

def head_to_list(head):

    p = head
    items = []
    while p:
        items.append(p.data)
        p = p.next
    return items