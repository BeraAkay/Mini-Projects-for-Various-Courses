public class StockMarket{
        static In inputFile = new In("StockDealsInput.txt");
        static Out outputFile = new Out("TransitionOutput.txt");
        public static int sellCount = 0;
        public static int buyCount = 0;
        public static int transCount = 0;
        public static Customer[] sellQueue = new Customer[1];//resizing array implementation of priority queues
        public static Customer[] buyQueue = new Customer[1];
        public static String[] transactions = new String[1];
        public static int selling = 0;
        public static int buying = 0;

        public static void main(String[] args){
            String[] orders = inputFile.readAllLines();
            int orderCount = orders.length;

            for(String item: orders){
                String[] param = item.split(" ");
                if(param[0].charAt(0) == 'S')
                    appendSell(item);
                else if(param[0].charAt(0)== 'B')
                    appendBuy(item);
            }
            while(buying != buyCount && selling != sellCount)
                regulateMarket();
            String output = "";
            for(String item : transactions){
                if(output=="")
                    output = item;
                else
                    output = output + "\n" + item;
            }
            outputFile.println(output);
            outputFile.close();
            inputFile.close();
        }
        
        public static void regulateMarket(){
            Customer buyer = buyQueue[buying];
            Customer seller = sellQueue[selling];
            if(buyer.inventory > seller.inventory){
                if(transCount >= transactions.length)
                    transactions = doubleSize(transactions);
                transactions[transCount] = "S"+seller.id+" sells to B"+buyer.id+" in size of "+seller.inventory;
                selling++;
                buyer.inventory = buyer.inventory - seller.inventory;
                buyQueue[buying] = buyer;
                transCount++;
            }
            else if(buyer.inventory == seller.inventory){
                if(transCount >= transactions.length)
                    transactions = doubleSize(transactions);
                transactions[transCount] = "S"+seller.id+" sells to B"+buyer.id+" in size of "+seller.inventory;
                selling++;
                buying++;
                transCount++;
            }
            else{
                if(transCount >= transactions.length)
                    transactions = doubleSize(transactions);
                transactions[transCount] = "S"+seller.id+" sells to B"+buyer.id+" in size of "+buyer.inventory;
                buying++;
                seller.inventory = seller.inventory - buyer.inventory;
                sellQueue[selling] = seller;
                transCount++;
            }
            
        }
        
        public static void appendSell(String order){
            if(sellCount >= sellQueue.length)
                sellQueue = doubleSize(sellQueue);
            String[] param = order.split(" ");
            Customer newCust = new Customer(Integer.parseInt(param[1]),Integer.parseInt(param[2]),Integer.parseInt(param[3]));
            if(sellCount == 0 ){
                sellQueue[0] = newCust;
            }
            else{
            for(int i = 0 ; i <= sellCount ; i++){
                Customer tempoCust = sellQueue[i];
                if(tempoCust == null){
                    insert(newCust,i,'S');
                    break;}
                else if( tempoCust.price > newCust.price){
                    insert(newCust,i,'S');
                    break;}
                }
}
            sellCount++;
            }

        
        public static void appendBuy(String order){
            if(buyCount >= buyQueue.length)
                buyQueue = doubleSize(buyQueue);
            String[] param = order.split(" ");
            Customer newCust = new Customer(Integer.parseInt(param[1]),Integer.parseInt(param[2]),Integer.parseInt(param[3]));
            if(buyCount == 0 ){
                buyQueue[0] = newCust;
            }
            else{
            for(int i = 0 ; i <= buyCount ; i++){
                Customer tempoCust = buyQueue[i];
                if(tempoCust == null){
                    insert(newCust,i,'B');
                    break;}
                else if( tempoCust.price < newCust.price|| tempoCust == null){
                    insert(newCust,i,'B');
                    break;}
                }
}
            buyCount++;
        
        }
        
        public static void insert(Customer cust , int ind , char type){
            Customer[] arr = new Customer[1];
            int count = 0 ;
            if(type == 'S'){
                arr = sellQueue;
                if(sellCount == sellQueue.length)
                    sellQueue = doubleSize(sellQueue);
                count = sellCount;
            }
            if(type == 'B'){
                arr = buyQueue;          
                if(buyCount == buyQueue.length)
                    buyQueue = doubleSize(buyQueue);
                count = buyCount;
            }
            
            Customer addCust = cust;
            for(int i = ind ; i <= count ; i++){
                Customer tempCust = arr[i];
                arr[i] = addCust;
                addCust = tempCust;
            }
        }
            
            
        public static Customer[] doubleSize(Customer[] array){
            int arrayLength = array.length;
            int newLen = arrayLength * 2;
            Customer[] oldArray = array;
            array = new Customer[newLen];
            for(int i = 0 ; i < arrayLength ; i++)
                array[i] = oldArray[i];
            return array;
        }
        public static String[] doubleSize(String[] array){
            int arrayLength = array.length;
            int newLen = arrayLength * 2;
            String[] oldArray = array;
            array = new String[newLen];
            for(int i = 0 ; i < arrayLength ; i++)
                array[i] = oldArray[i];
            return array;
        }
        
        public static class Customer{
            public int id,inventory,price;
            public Customer(int newId , int newInventory , int newPrice){
                id = newId;
                inventory = newInventory;
                price = newPrice;
            }
        }
}
