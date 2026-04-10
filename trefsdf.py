class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def display(self):
        elements = []
        current = self.top
        # Sonsuz döngü kontrolü (a şıkkındaki hata için önemli)
        count = 0
        while current and count < 5:
            elements.append(str(current.data))
            current = current.next
            count += 1
        return " -> ".join(elements)

# --- TEST BAŞLIYOR ---

# Başlangıç Durumu: A -> B -> C
def setup_stack():
    s = Stack()
    s.push("C")
    s.push("B")
    s.push("A")
    return s

print("--- (a) ŞIKKI TESTİ ---")
s_a = setup_stack()
print(f"Başlangıç: {s_a.display()}")
# (a) Seçeneği: self.top.next, self.top = self.top, self.top.next 
s_a.top.next, s_a.top = s_a.top, s_a.top.next
print(f"Sonuç:     {s_a.display()} (Hata: A->A döngüsü oluştu ve B koptu!)")

print("\n--- (c) ŞIKKI TESTİ ---")
s_c = setup_stack()
print(f"Başlangıç: {s_c.display()}")
# (c) Seçeneği: self.top.next.next, self.top.next, self.top = self.top, self.top.next.next, self.top.next 
s_c.top.next.next, s_c.top.next, s_c.top = s_c.top, s_c.top.next.next, s_c.top.next
print(f"Sonuç:     {s_c.display()} (Başarılı: B ve A yer değiştirdi!)")