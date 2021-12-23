nums = {}
def fib(n):
	if n <= 2:
		return 1
	if n in nums:
		return nums[n]
	else:
		num = fib(n-1) + fib(n-2)
		nums[n] = num
		return num


#print(fib(40))

dic = {}
def multi(arr):
	if not arr:
		return 1
	else:
		result = arr[0] * multiply(a[1:0])
def multiply(arr):
	if not arr:
		return 1
	else:
		num = arr[0] * multiply(arr[1:])
		dic[arr[0]] = num
		return num, dic

arr = [3,4,5]
a,b = multiply(arr)
print(a,b)