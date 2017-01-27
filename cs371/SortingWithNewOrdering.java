public class SortingWithNewOrdering {
        static In orderingFile = new In("NewOrdering.txt");
        static In inputFile = new In("InputNewOrdering.txt");
        
        static Out outputFile = new Out("OutputNewOrdering.txt");
        static String order = orderingFile.readAllLines()[0];
            
        static String[] input = inputFile.readAllLines();
        public static int len = input.length;

        public static void main(String[] args){
            sort(input);
            String output = "";
            for(int ind = 0 ; ind < len ; ind++){
            if(ind == 0)
                output = input[ind];
            else
                output = output + "\n" + input[ind];
            }
            outputFile.println(output);
            outputFile.close();
            inputFile.close();
        }
        public static void sort(String[] input){
            for(int i = 0; i < len ; i++){
                int min = i;
                for(int j = i+1; j < len ; j++){
                    if(comesBefore(input[j],input[min])){
                        min = j;
                    }
                }
                String temp = input[i];
                input[i] = input[min];
                input[min] = temp;
            }
        }
        
        public static boolean comesBefore(String a, String b){
               int x = 0;
               int y = 0;
               int leng = a.length();
               if(leng > b.length() ){
                   leng = b.length();
               }
               for (int i = 0; i < leng && x == y; i++) {
                  x = order.indexOf(a.charAt(i));
                  y = order.indexOf(b.charAt(i));
               }
               int val = x - y;
               if (x == y && a.length() != b.length())
                   val =  a.length() - b.length();

               if(val < 0)
                    return true;
                return false;
        }

}
