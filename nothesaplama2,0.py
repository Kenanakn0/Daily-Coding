while True:
    vize_girdi = input ("Vize notunu girin(veya çıkmak için 'q' yaz):")

    if vize_girdi == 'q':
       print("ProgramdaN Çıkılıypr...")
       break
    vize = int (vize_girdi)
    final = int(input("Final notunu girin:"))

    ortalama = (vize*0.4) + (final *0.6)
    print("Ortalamanız:",ortalama)

    if ortalama >=50:
      print("Dersi geçtiniz")
    else:
      print("Dersten kaldınız")

      print("-"*30)