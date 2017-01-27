//Mustafa Bera Akay
//214102757
//Reverser

public class Reverser {
    
 public static void main(String [] args){
     
     In toReverse = new In("CsvToReverse.txt");
     String inFile = toReverse.readAll(); //input file is read
     
     String[] lines = inFile.split("\n");//input file is divided into lines
     int lineNo = lines.length;//array length is calculated
     
     String[] reversedLines = new String[lineNo];//empty array is created for reversed lines
     
     for(int index = 0;index<lineNo;index++){
         reversedLines[index]=lineReverser(lines[index]);//reversing function is called for each line
     }
     
      
      String outString = "";//reversed string declaration
 
      for(int index=0;index<=lineNo-1;index++){//combining reversed lines
     
          if(index==0){
             outString=reversedLines[index];//if its the first line no new line added
         }
          else{
             outString+="\r\n"+reversedLines[index];
         }
 }
      Out reversed = new Out("ReverseCsv.txt");//output file
      reversed.print(outString);//string is written to the file
      
 }
 
 public static String lineReverser(String arg){
     String[] items = arg.split(",");//making an array of the elements between the ","s
     
     int amount = items.length;//array length of elements
     
     String[] reverseItems= new String[amount] ;//reverse item list declaration

     for(int index = amount-1 ; index>=0 ; index--){
         reverseItems[amount-1-index] = items[index];//reversing items 
     }
     String revLine = "";
     for (int index=0;index<=amount-1;index++){//combining reversed items
         
         if(index==0){
             revLine=reverseItems[index];//if its the first element we dont start with a ","
         }
         else{
             revLine+=","+reverseItems[index];
         }
     }
     return revLine;//returns the reversed line
 }

}
    
