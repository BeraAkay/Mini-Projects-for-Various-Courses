public class TestEditor{
    private static LinkedList list;
    public static int textLines = 1;
    public static String nextLine;
    public static String[] previousJob = {null,"1"};
    public static String output = "InputFile.txt";
    public static void main(String[] args){
        In inputFile = new In("InputFile.txt");
        String[] input = inputFile.readAllLines();
        list = new LinkedList();
        int i = input.length;
        for (int index = 0 ; index < i ; index++ ){
           TestEditor.whatDo(input[index]);
        }
    }//main end
    
    public static void whatDo(String line){
     if(line!=null){
        output = output + "\n" + previousJob[1]+"> "+line;
        int lenstr  = line.length();
        String[] lineSplit = line.split(" ");
        int len = lineSplit.length;
        if( lenstr != 0 ){
            switch(len){
                case 1:
                    oneLiner(line);
                    break;
                case 2:
                    twoLiner(line);
                    break;
                case 3:
                    threeLiner(line);
                    break;
                default:
                    adder(line);
            }
        }
        else{
            adder("");
        }
        }
     
    }//whatDo end
    
    public static void adder(String line){
        if(previousJob[0] == "A"){
            previousJob[1] = String.valueOf(textLines);
            list.add(line);
        }
        else if(previousJob[0] != null && Integer.parseInt(previousJob[1]) != textLines){
            list.add(line,Integer.parseInt(previousJob[1])-1);
            
        }
        else if(previousJob[0] != null && Integer.parseInt(previousJob[1]) == textLines){
            list.add(line,Integer.parseInt(previousJob[1])-1);
        }
        else{
            list.add(line,Integer.parseInt(previousJob[1])-1);

        }
        previousJob[0] = null;
        textLines++;
        previousJob[1] = String.valueOf(Integer.parseInt(previousJob[1])+1);
    }

    public static String finalFile(){
        String wholeThing = "";
        Node node = list.getFirst();
        for(int i = 0 ; i < textLines ; i++ ){
            if(i != 0)
                wholeThing = wholeThing + "\n";
            if(i!=textLines-1){
                wholeThing = wholeThing + node.getData();
                node = node.getNext();
        }
        }
        return wholeThing;
    }
    
    public static void insertLine(String line){
        int index = Integer.parseInt(previousJob[1]);
        if(index >= textLines){
            for(int i=index ; i>=textLines ; i--){
                list.add("");
            }
        }
        previousJob[0]="I";
        previousJob[1]=String.valueOf(index);
    
    }//insertLine end
    
    public static void deleteLine(int index){
        try{
        list.delete(index);
        textLines--;
        previousJob[1]=String.valueOf(textLines);
        }
        catch(NullPointerException npe){
        }
    }//deleteLine end
    
    public static void listLine(int index){
        try{
            Node indexedNode = list.getTo(index);
            output = output + "\n\t"+(++index) + ">" + indexedNode.getData();}
        catch(NullPointerException npe){
        }
    }//listLine end
    
    public static void appendLine(String line){
        previousJob[0]="A";
    }//appendLine end
    
    public static void saveAs(String filename){
        Out savefile = new Out(filename);
        savefile.print(finalFile());
        savefile.close();
        
        
    }//saveAs end
    
    public static void exit(){
        Out outputFile = new Out("OutputFile.txt");
        outputFile.print(output);
        outputFile.close();
    }//exit end
    
    public static boolean isNumber(String str){
          try{  
              double number = Double.parseDouble(str);  
          }  
          catch(NumberFormatException error){
              return false;  
          }  
          return true;  
    }//end isNumber
    
    public static void oneLiner(String line){
        String[] lineSplit = line.split(" ");
        switch(lineSplit[0].charAt(0)){
            case 'I':
                previousJob[1] = String.valueOf(Integer.parseInt(previousJob[1])-1);
                insertLine(line);
                break;
            case 'L':
                for(int i = 0 ; i < textLines ; i++ ){
                listLine(i);
            }

                break;
            case 'D':
                deleteLine(Integer.parseInt(previousJob[1])-1);

                break;
            case 'A':
                appendLine(line);
                break;
            case 'E':
                exit();

                break;
            default:
                adder(line);
        }
    }//oneLiner end
    
    public static void twoLiner(String line){
        String[] lineSplit = line.split(" ");
        if(isNumber(lineSplit[1])){
            switch(line.charAt(0)){
                case 'I':
                    previousJob[1] = String.valueOf(Integer.parseInt(lineSplit[1]));
                    insertLine(line);

                    break;
                case 'L':
                    listLine( Integer.parseInt(lineSplit[1]) );

                    break;
                case 'D':
                    deleteLine( Integer.parseInt(lineSplit[1])-1 );
                    break;
            }
        }
        else if(line.charAt(0)=='S'){
            saveAs( lineSplit[1] );

        }
        else{
            adder(line);
        }
    }//twoLiner end
    
    public static void threeLiner(String line){
        String[] lineSplit = line.split(" ");
        if(isNumber(lineSplit[1])&&isNumber(lineSplit[2])){
            switch(line.charAt(0)){
                case 'L':
                for(int lines = Integer.parseInt(lineSplit[1]);lines<=Integer.parseInt(lineSplit[2]);lines++){
                    listLine(lines);
                }
                    break;
                case 'D':
                for(int lines=  Integer.parseInt(lineSplit[1]);lines<=Integer.parseInt(lineSplit[2]);lines++){
                    deleteLine(lines);
                }
                    break;
            }
        }
        else{
            adder(line);
        }
    }//threeLiner end


static class LinkedList{
    private Node first;
    private int length;
    
    public LinkedList(){
        first = new Node(null);
        length = 0;  
    }
    
    public int howLong(){
        return length;
    }
    
    public Node getLast(){
        Node last = first;
        while(last.getData() != null){
            last = last.getNext();
        }
        return last;
    }
    
    public Node getFirst(){
        return first;
    }
    
    public Node getTo(int index){
        Node currentNode = first;        
        for(int i = 0 ; i < index ; i++){
            currentNode = currentNode.getNext();
        }
        return currentNode;
    }
    
    public void add(String data){
        if(first.getData() == null)
            first.setData(data);
        else{
        Node last = getTo(length-1);
        Node newLast = new Node(data);
        last.setNext(newLast);
        }
        length++;
    }
    
    public void add(String data, int index){
        if(first.getData() == null)
            first.setData(data);
        else{ 
        Node previousNode = getTo(index-1);
        Node temp = new Node(data);
        if(previousNode.getNext() != null){
        Node currentNode = previousNode.getNext();
        temp.setNext(currentNode);
        }
        previousNode.setNext(temp);
        
        }
        length++;
    }
    
    public void delete(int index){
        if(index == 0){
            Node first  = getFirst();
            first  = null;
        }
        else if(index == length-1){    
            Node newLast = getTo(index-1);
            newLast.setNext(null);

        }
        else{
            Node previousNode = getTo(index-1);
            Node nextNode = previousNode.getNext().getNext();    
            previousNode.setNext(nextNode);
            
        }
        length--;
    }
    
     
    }//LinkedList end
    
    private static class Node{
        Node next;
        String data;
        
        public Node(String newData){
            next = null;
            data = newData;
        }
        
        public Node(String newData, Node nextNode){
            next = nextNode;
            data = newData;
        }
        
        public Node getNext(){
            return next;
        }
        
        public void setNext(Node nextNode){
            next =  nextNode;
        }
        
        public String getData(){
            return data;
        }
        
        public void setData(String newData){
            data = newData;
        }
        
    }//Node end
    
}//END