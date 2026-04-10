package YeniProje;

import java.util.Scanner;
import java.util.Random;

public class rockpaperscissors {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        String[] seçenek = {"Taş", "Kağıt", "Makas"};

        while (true) {
            System.out.println("Seçiminizi yapın (T:Taş , K:Kağıt , M:Makas , Ç:Çıkış)");
            String userseçenek = scanner.nextLine().toLowerCase();

            if (userseçenek.equals("ç")) {
                System.out.println("Oyundan Çıkış Yaptın !!");
                break;
            }

            if (!userseçenek.equals("t") && !userseçenek.equals("k") && !userseçenek.equals("m")) {
                System.out.println("Geçersiz seçim! Lütfen Taş ise T, Kağıt ise K, Makas ise M seçin.");
                continue;
            }

            String userseçenekString = 
                userseçenek.equals("t") ? "Taş" :
                userseçenek.equals("k") ? "Kağıt" :
                userseçenek.equals("m") ? "Makas" : "Bilinmiyor";

            int pcIndex = random.nextInt(3);
            String pcSeçimi = seçenek[pcIndex];

            System.out.println("Sizin seçiminiz: " + userseçenekString);
            System.out.println("Bilgisayarın seçimi: " + pcSeçimi);

            if (userseçenekString.equals(pcSeçimi)) {
                System.out.println("Berabere");
            } else if (
                (userseçenekString.equals("Taş") && pcSeçimi.equals("Makas")) ||
                (userseçenekString.equals("Kağıt") && pcSeçimi.equals("Taş")) ||
                (userseçenekString.equals("Makas") && pcSeçimi.equals("Kağıt"))
            ) {
                System.out.println("Tebrikler, Siz Kazandınız! :-)");
            } else {
                System.out.println("Bilgisayar kazandı!");
            }
        }

        scanner.close();
    }
}
