package sorucevap;

import java.util.Scanner;

public class sorular {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		Scanner n = new Scanner(System.in);

		int k = 5;

		String[] sorular = new String[k];
		sorular[0] = "Verilerden hangisi tamsayı tipidir ?";
		sorular[1] = "Verilerden hangisi ondalık sayıları saklamak için kullanabilir ?";
		sorular[2] = "Veri tiplerinden hangisi ture/false vardır ?";
		sorular[3] = "Verilerden hangisi karkater değer saklayabilir ?";
		sorular[4] = "Verilerden hangisi bir döngü komutu değildir";

		String[][] seçenekler = { { "int", "double", "char", "String" }, { "int", "double", "char", "String" },
				{ "int", "double", "boolean", "String" }, { "for", "do", "do-while", "switch" },
				{ "for", "do", "do-while", "switch" } };

		String[][] cevapanaktarı = { { "int" }, { "double" }, { "boolean" }, { "char" }, { "switch" } };

		boolean[] soruKontrol = new boolean[k];

		int sayaç = 0;

		do {
			int soruNo = (int) (Math.random() * 5);
			if (!(soruKontrol[soruNo])) {
				soruKontrol[soruNo] = true;
				System.out.println((soruNo + 1) + ".soru:" + sorular[soruNo]);
				for (int i = 0; i < seçenekler[soruNo].length; i++) {
					System.out.println((i + 1) + " . " + seçenekler[soruNo][i]);
				}
				System.out.println("cevabınızı girin (1-4) : ");
				int cevapIndex = n.nextInt() - 1;// kullanıcıdan alınan cevap
				if (seçenekler[soruNo][cevapIndex].equals(cevapanaktarı[soruNo][0])) {
					System.out.println("Doğru cevap!");
				} else {

					System.out.println("Yanlış ceavp.Doğru cevap :" + cevapanaktarı[soruNo][0]);
				}
				sayaç++;

			}

		} while (sayaç < 5);
	}
}