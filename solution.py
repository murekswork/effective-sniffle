ex = [2,3,4,5,10]

def solution(input: list[int], target: int):
	work_list = input
	input_s = input.copy()
	result = list()
	for i in work_list:
		work_list.remove(i)
		n = target - i
		if n in work_list:
			result.append(input_s.index(i))
			result.append(input_s.index(n))
			return print('got_it', result)
		print(input)
		print('miss', 'checked', i)
	print(result)

solution(ex, 15)
	
