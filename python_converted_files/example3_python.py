from utils.linkedlist_utils import create_head_from_list, head_to_list

def invertir():
    global ptr

    if (ptr.next != None):

        p = ptr  # p, inicialmente guarda la dirección del primer nodo

        q = p.next  # q, inicialmente guarda la dirección del segundo nodo

        r = q.next  # r, inicialmente guarda la dirección del tercer nodo

        while (r != None):

            q.next = p  # inicialmente, el segundo nodo se enlaza con el primero

            p = q

            q = r

            r = r.next

        q.next = p  # en el ciclo anterior falto enlazar el ultimo nodo con el penúltimo

        ptr.next = None  # después de invertir los enlaces, el ultimo nodo se apunta a None

        ptr = q  # el nuevo ptr va a ser el nodo apuntado  por q, es decir el ultimo  de la lista anterior

    else:

        print("debe existir mínimo dos elementos para invertir una lista")


ptr = create_head_from_list([1, 2, 3])
invertir()
print(head_to_list(ptr))
