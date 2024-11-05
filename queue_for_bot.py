from queue import Queue as Q


class User:
    def __init__(self, id, name="base_name"):
        self.id = id
        self.name = name

    def set_name(self, new_name):
        self.name = new_name

    def __str__(self):
        return f"name:{self.name}, ID:{self.id}"


class Queue:
    def __init__(self, admin=None):
        self.queue = list
        self.admin = admin

    def get_admin(self):
        return self.admin

    def add_user(self, new_user: User):
        self.queue.append(new_user)

    def next_in_queue(self):
        return self.queue.get(), self.queue.queue[0]

    def __iter__(self):
        yield from self.queue


class Admin(User, Queue):
    def __init__(self, id, name="Basa_name", name_queue="Base_name", queue=None):
        print(f"admin init: {name}")
        User.__init__(id, name)
        self.queue = Queue(self)


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
