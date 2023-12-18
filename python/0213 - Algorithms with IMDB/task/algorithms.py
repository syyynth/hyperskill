import sys


def linear_search(movies, r):
    for title, rating in movies:
        if rating == r:
            print(f'{title} - {rating}')


def bubble_sort(data):
    for i in range(len(data)):
        for j in range(len(data) - 1):
            if data[j][1] > data[j + 1][1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    # this, or making merge sort in-place :x
    return data


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


def get_data(path):
    with open(path, encoding='U8') as f:
        data = []
        for movie in f:
            title, rating = movie.strip().rsplit(',', maxsplit=1)
            data.append((title.strip('"'), float(rating)))
        return data


if len(sys.argv) == 1:
    binary_search(merge_sort(get_data('movies.csv')), 6)
else:
    sort_algo = {
        'bubble': bubble_sort,
        'merge': merge_sort
    }
    search_algo = {
        'linear': linear_search,
        'binary': binary_search
    }
    try:
        data = get_data(sys.argv[1])
        _sort = sys.argv[2]
        _search = sys.argv[3]
        _rating = float(sys.argv[4])
        search_algo[_search](sort_algo[_sort](data), _rating)
    except:
        print('Example of a run: python.exe algorithms.py movies.csv bubble binary 6.6')
