def linear_search(movies, r):
    for title, rating in movies:
        if rating == r:
            print(f'{title} - {rating}')


def bubble_sort(data):
    for i in range(len(data)):
        for j in range(len(data) - 1):
            if data[j][1] > data[j + 1][1]:
                data[j], data[j + 1] = data[j + 1], data[j]


def binary_search(movies, rating):
    l = 0
    r = len(movies) - 1

    while l < r:
        mid = (l + r) // 2
        rat = movies[mid][1]
        if rat >= rating:
            r = mid
        else:
            l = mid + 1

    while l < len(movies) and movies[l][1] == rating:
        print(f'{movies[l][0]} - {movies[l][1]}')
        l += 1


def merge(arr1, arr2):
    new_arr = []
    l = r = 0

    while l < len(arr1) and r < len(arr2):
        if arr1[l][1] < arr2[r][1]:
            new_arr.append(arr1[l])
            l += 1
        else:
            new_arr.append(arr2[r])
            r += 1

    new_arr.extend(arr1[l:])
    new_arr.extend(arr2[r:])

    return new_arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    return merge(
        merge_sort(arr[:mid]),
        merge_sort(arr[mid:])
    )


def print_all(movies):
    for title, rating in movies:
        print(f'{title} - {rating}')


with open('../movies.csv', encoding='U8') as f:
    data = []
    for movie in f:
        title, rating = movie.strip().rsplit(',', maxsplit=1)
        data.append((title.strip('"'), float(rating)))
    binary_search(merge_sort(data), 6)
