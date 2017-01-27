.data

.text
addi $t3, $zero , 10 #for loop end value
add $s0, $zero , $zero#sum value
addi $t0 , $zero, 1#i of for loop

for : 

slt $t2, $t3, $t0#checking whether i is smaller than end value ,chechking it like this since it increases by 2
bne $t2, $zero,forex#if i>=endval is true , it jumps to for exit
add $t1, $zero , $zero#setting while loop counter to 0

while : 

slt $t4 , $t0, $t1#checking whether counter is smaller than i of loop
bne $t4, $zero , wexit#if so , jump to while exit
add $s0, $t1 ,$s0#add y to sum
addi $t1,$t1, 1#increase y
j while#restart while segment

wexit:
addi $t0, $t0, 2#icnrese i by 2
j for#restart for segment

forex :

