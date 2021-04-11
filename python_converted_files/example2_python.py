def insertarantes(ptr, elem, dato):

    antep = None

    p = ptr

    while ((p.next != None) and (p.data != elem)):

        antep = p

        p = p.next

    if (p.data == elem):

        q = Node()

        q.data = dato

        q.next = p

        if (p == ptr):

            ptr = q

        else:

            antep.next = q

    else:

        print(elem, "no existe en esta lista")
