#A list is defined here
.data
my_array: .word 10, 9, 2, 3, 1, 4, 6, 7, 32
.text
la $s0, my_array    # based address of list loaded into $s0
addi $s1, $zero, 9  # $s1 is set to the size of the list 

# Now you have the size and the base address of the list
# You should implement sorting algorithms that provided to you in assignment guide
# After sorting the array you should be able to find the median of the list
# Continue to write your code here
add $t0, $zero,$zero#set i = 0
while:
beq $t0,$s1,wexit#if i = len , jump to end
add $t1,$t0,$zero#set j = i
add $t2,$t1,$zero#set temp-min-index = j
inwhile:
beq $t1,$s1,inwexit#if j = len , jump to end
sll $t4,$t1,2#index calculation for comparison
sll $t5,$t2,2
add $t4,$s0,$t4
add $t5,$s0,$t5
lw $t4,0($t4)
lw $t5,0($t5)
slt $t6,$t5,$t4
bne $t6,$zero,pass#if a[j]<a[temp-min-index], temp min index = j
add $t2,$t1,$zero
pass:
addi $t1,$t1,1#increment j
j inwhile#restart inner segment
inwexit:
sll $t4,$t0,2#calculating indexes for swap
add $t4,$s0,$t4
lw $t3,0($t4)
sll $t5,$t2,2
add $t5,$s0,$t5
lw $t6, 0($t5)
sw $t6,0($t4)#swap the values
sw $t3,0($t5)
addi $t0,$t0,1#increment i
j while#restart outer segment
wexit:
addi $t4,$zero,2#median index calculation
div $s1,$t4
mflo $s2
sll $s2,$s2,2
add $s2,$s0,$s2
lw $s2,0($s2)#median of array