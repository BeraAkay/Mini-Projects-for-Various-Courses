#A list is defined here
.data
my_array: .word 10, 9, 2, 3, 1, 4, 6, 7, 32
.text
la $s0, my_array    # based address of list loaded into $s0
addi $s1, $zero, 9  # $s1 is set to the size of the list 

# Now you have the size and the base address of the list
# You should be able to find the mean of the list and the diffence between maximum and minimum elements in the list.
# Continue to write your code here
lw $t7, 0($s0)#min
lw $t6, 0($s0)#max as 1st item in array

addi $t1 , $zero, 0#set i for 0, index counter
for : 
beq $t1, $s1, forexit#if i reaches list length , end loop
sll $t2, $t1, 2# adress calculation for index
add $t3 ,$t2 ,$s0
lw $t3, 0($t3)#loading value to check on it
exch:
slt $t4, $t3, $t7#checking how the current item stands against the min and max
slt $t5, $t6, $t3
bne $t4,$zero, min#if min and max needs updating jump to their segments
bne $t5,$zero,max
add $t0, $t0, $t3#add current item to sum
addi $t1, $t1, 1#increment i
j for#restart for segment
forexit:
div $t0, $s1#divide sum by array length
mflo $s2#move the average (floored value) to $s2
sub $s3, $t6,$t7#calculate range(max-min)
j end#pass the min max exchange segments
min:
add $t7,$zero,$t3#update min
j exch#jump back inside the loop
max:
add $t6, $zero, $t3#update max
j exch#jump back inside the loop
end: