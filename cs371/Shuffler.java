public class Shuffler{
    public static void main(String[] args){
    }
    public static boolean isShuffle(String args1, String args2 , String args3){
        String[] string1 = args1.split("");
        String[] string2 = args2.split("");
        String[] string3 = args3.split("");
        int str1 = string1.length;
        int str2 = string2.length;
        int str3 = string3.length;
        int net = str1 + str2 ;
        if(net!=(str3+1))
            return false;
        boolean[][] matrix = new boolean[str1][str2];
        matrix[0][0] = true;
        for (int i = 0 ; i < str1 ; i++)
            matrix[i][0] = (string1[i].equals(string3[i]));
        for(int i = 0 ; i < str2 ; i++)
            matrix[0][i] = (string2[i].equals(string3[i]));
        for(int i = 1 ; i < str1 ; i++){
            for(int j = 1 ; j < str2 ; j++){
                boolean minval = matrix[i-1][j-1] || matrix[i][j-1] || matrix[i-1][j];
                matrix[i][j] = minval && ( string3[i+j].equals( string1[i]) || string3[i+j].equals(string2[j]));
            }
        }  
        return matrix [str1-1][str2-1];
    }
}