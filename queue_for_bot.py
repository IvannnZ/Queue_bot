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
    def __init__(self, name="base_name"):
        self.name = name
        self.queue = Q()

    def set_queue_name(self, new_name):
        self.name = new_name

    def get_queue_name(self):
        return self.name

    def add_user(self, new_user: User):
        self.queue.put(new_user)

    def next_in_queue(self):
        return self.queue.get(), self.queue.queue[0]


class Admin (User, Queue):
    def __init__(self, id, name = "Base_name", name_queue="Base_name", queue = None):
        User.__init__(id,name)
        Queue.__init__(name_queue)
        self.queue = queue


    def set_queue(self,new_queue):
        self.queue = new_queue


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
