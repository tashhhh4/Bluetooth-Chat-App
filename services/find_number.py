def find_single(nums):
    try:
        found_nums = set()
        for num in nums:
            if num not in found_nums:
                found_nums.add(num)
            else:
                found_nums.remove(num)

        return found_nums.pop()
    except:
        return None

# test
print(find_single([3, 5, 6, 6, 3, 8, 8]))
print(find_single([1]))
print(find_single([5, 5, 6, 6, 0]))
print(find_single([-4, 8, 8]))
print(find_single([8, 8]))