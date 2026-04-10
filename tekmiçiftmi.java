package say�lar;

import java.util.Scanner;

public class tekmi�iftmi {

	public static void main(String[] args) {

		System.out.println("-----------Tek mi �ift mi ----------------");
		Scanner k = new Scanner(System.in);
		
		System.out.println("Eleman say�s�n� girin : ");
		int elemansay�s� = k.nextInt();
		k.nextLine();
		
		int[] say�lar = new int[elemansay�s�];
		for(int i=0 ; i<say�lar.length ; i++ )
		{
			System.out.println("Dzinin " + i + " .index de�erini girin : ");
			say�lar[i] = k.nextInt();
			k.nextLine();
		}
		for (int de�er : say�lar)
			tekM��iftMi(de�er);
	}
	
	public static void tekM��iftMi(int say�)
	{
		if (say� % 2 == 0)
		{
			System.out.println("girdi�iniz say� " + say� + " olup �ift ve");
			
		}else {
			System.out.println("girdi�iniz say� " + say� + " olup tek ve ");
			
		}
		if(say� > 0 )
		{
			System.out.println("pozitifdir");
		}else {
			System.out.println("negatiftir");
		}
		
		
	}

}
