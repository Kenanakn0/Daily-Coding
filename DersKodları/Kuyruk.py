
kuyruk = []
kuyruk.append(10)
kuyruk.append(20)
kuyruk.append(30)
print("Mevcut kuyruk gösterimi:", kuyruk)

kuyruk.pop(0)  
print("Kuyruk:", kuyruk)


class Düğüm:
    def __init__(self, data):
        self.data = data
        self.next = None


class Kuyruk:
    def __init__(self):
        self.başlangıc = None
        self.bitiş = None

    def kuyrukBoşsa(self):
        return self.başlangıc is None

    def ekle(self, eklenecekEleman):
        temp = Düğüm(eklenecekEleman)
        if self.bitiş is None:
            self.başlangıc = self.bitiş = temp
            return
        self.bitiş.next = temp
        self.bitiş = temp

    def elemanSilme(self):
        if self.kuyrukBoşsa():
            return ("Kuyruk boş, silinecek eleman yok.")
        temp = self.başlangıc
        self.başlangıc = temp.next
        def kuyrukGösterimi(self):
            if self.kuyrukBoşsa():
                return ("Kuyruk boş.")
            temp = self.başlangıc
            while temp:
                print(temp.data)
                temp = temp.next

K=kuyruk()
K.ekle(10)
K.ekle(20)
K.ekle(30)
K.ekle(40)
K.ekle(50)
K.kuyrukGösterimi()
K.elemanSilme()
K.kuyrukGösterimi()
K.elemanSilme()
K.kuyrukGösterimi()




