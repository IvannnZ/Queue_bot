from re import search


class User:
    def __init__(self, id_User, name="base_name"):
        self.id_User = id_User
        self.name = name
        self.queues = []

    def set_name(self, new_name):
        self.name = new_name

    def add_to_queue(self, new_queue):
        self.queues.append(new_queue)

    def __str__(self):
        return f"name:{self.name}, ID:{self.id_User}"


class Queue:
    def __init__(self, admin=None):
        self.queue = list()
        self.admin = admin

    def get_admin(self):
        return self.admin

    def add_user(self, new_user: User):
        self.queue.append(new_user)

    def next_in_queue(self):
        if len(self.queue)>=2:
            return self.queue.pop(0), self.queue[0]
        elif len(self.queue) == 1:
            return self.queue.pop(0), None
        else: return None, None
    def __iter__(self):
        yield from self.queue

    def __len__(self):
        return len(self.queue)

    def lenght(self):
        return len(self.queue)


    def search_by_id(self, id_User):
        for i in range(self.lenght()):
            if self.queue[i].id_User == id_User:
                return i
        else:
            return None


class Admin(User):
    def __init__(self, id_Admin, name="Basa_name", name_queue="Base_name", queue=None):
        print(f"admin init: {name}")
        User.__init__(self,id_Admin, name)
        self.admin_queue = Queue(self)
        self.id_Admin = id_Admin
        self.name = name

    def add_user(self, new_user: User):
        self.admin_queue.add_user(new_user)

    def next_in_queue(self):
        return self.admin_queue.next_in_queue()

    def __iter__(self):
        yield from self.admin_queue

    def lenght(self):
        return len(self.admin_queue)

    def search_by_id(self, id_User):
        return self.admin_queue.search_by_id(id_User)

if __name__ == "__main__":
    a = User(1, 1)
    b = User(2, 2)
    c = User(3, 3)
    d = User(4, 4)
    q = Queue(a)
    q.add_user(a)
    q.add_user(b)
    q.add_user(c)
    q.add_user(d)
    print(q.next_in_queue()[0])
    for i in q:
        print(i.name)
    print(q.next_in_queue()[1])
    print(q.lenght())
