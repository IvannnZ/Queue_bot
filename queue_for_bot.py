from queue import Queue as Q


class User:
    def __init__(self, id, name="base_name"):
        self.id = id
        self.name = name

    def __str__(self):
        return f"name:{self.name}, ID:{self.id}"


class Queue:
    def __init__(self, admin: User, name = "base_name"):
        self.admin = admin
        self.name = name
        self.queue = Q()

    def add_user(self, new_user: User):
        self.queue.put(new_user)

    def next_in_queue(self):
        return self.queue.get(), self.queue.queue[0]


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

    print(q.next_in_queue()[1])