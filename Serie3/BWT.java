import java.util.Arrays;

public class BWT{
    public static String[] getSuffixArray(String input){
        input = input + "$";
        String[] suffixes = new String[input.length()];
        for(int i = input.length()-1; i >= 0; i--){
            suffixes[i] = input.substring(i, input.length());
        }
        return suffixes;
    }

    /*public static class BWTResult {
        char[] bwt;
        String[] suffixArray;

        BWTResult(char[] bwt, String[] suffixArray) {
            this.bwt = bwt;
            this.suffixArray = suffixArray;
        }
    }*/


    public static char[] getBWT(String[] suffixArray){
        char[] bwt = new char[suffixArray.length];

        String text = suffixArray[0];
        Arrays.sort(suffixArray);
        
        for (int i = 0; i < suffixArray.length; i++){
            int pos = text.length() - suffixArray[i].length() - 1;
            if (pos >= 0){
                bwt[i] = text.charAt(pos);
            }
            else {
                bwt[i] = '$';
            }
        }

        System.out.println("Index\tBWT\tSuffix Array"); //Suffix Array includes F
        for (int i = 0; i < suffixArray.length; i++){
            System.out.println(i + "\t" + bwt[i] + "\t" + suffixArray[i]);
        }

        //BWTResult result = new BWTResult(bwt, suffixArray);
        return bwt;
    }

    public static class RanksAndFirst {
        int[] ranks;
        int[] first;
        char[] F;

        RanksAndFirst(int[] ranks, int[] first, char[] F) {
            this.ranks = ranks;
            this.first = first;
            this.F = F;
        }
    }


    public static RanksAndFirst getRanksAndFirst(char[] bwt){
        int[] ranks = new int[bwt.length];
        int[] counts = new int[256]; // Assuming ASCII
        int[] first = new int[256];


        for (int i = 0; i < bwt.length; i++){
            counts[bwt[i]]++;
            ranks[i] = counts[bwt[i]];
        }
        char[] F = bwt.clone();
        Arrays.sort(F);
        int i = 0;
        while (i < bwt.length){
            first[F[i]] = i;
            i = i + counts[F[i]];
        }

        return new RanksAndFirst(ranks, first, F);
    }


    public static String reconstruct(char[] bwt, RanksAndFirst rf) {
        char[] t = new char[bwt.length];
        t[bwt.length - 1] = '$';
        int b = 0;
        for (int i = bwt.length-2; i >= 0; i--) {
            t[i] = bwt[b];
            b = rf.first[bwt[b]] + rf.ranks[b] - 1;
        }
        return new String(t);
    }


    public static void main(String[] args){
        String input = args[0];
        String[] suffixArray = getSuffixArray(input);
        System.out.println("Suffix Array:");
        for(String suffix : suffixArray){
            System.out.println(suffix);
        }
        System.out.println("---");
        char[] bwt = getBWT(suffixArray);
        System.out.println("---");
        RanksAndFirst rf = getRanksAndFirst(bwt);
        String reconstructed = reconstruct(bwt, rf);
        System.out.println("Reconstructed: " + reconstructed);
    }
}
