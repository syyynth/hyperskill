from hstest import StageTest, dynamic_test, TestedProgram, WrongAnswer, CheckResult

import time

start_time = time.time()
# Reading Data from File
data = []
with open("movies.csv", "r", encoding="UTF-8") as file:
    for line in file:
        title, rating = line.rstrip().rsplit(',', 1)
        title = title.strip('"')
        data.append((title, float(rating)))


# Merge Sort

def merge_sort(data):
    if len(data) > 1:
        mid = len(data) // 2
        left_array = data[:mid]
        right_array = data[mid:]

        merge_sort(left_array)
        merge_sort(right_array)

        i = 0
        j = 0
        k = 0
        while i < len(left_array) and j < len(right_array):
            if left_array[i][1] <= right_array[j][1]:
                data[k] = left_array[i]
                i += 1
            else:
                data[k] = right_array[j]
                j += 1
            k += 1

        while i < len(left_array):
            data[k] = left_array[i]
            i += 1
            k += 1

        while j < len(right_array):
            data[k] = right_array[j]
            j += 1
            k += 1


merge_sort(data)


# Binary Search
def binary_search(data):
    left = 0
    right = len(data)-1
    mid = (left+right) // 2
    while left <= right:
        if data[mid][1] == 6.0:
            lower_bound = mid-1
            upper_bound = mid+1
            while data[lower_bound-1][1] == 6.0:
                lower_bound=lower_bound-1
            while data[upper_bound+1][1] == 6.0:
                upper_bound=upper_bound+1
            for index in range(lower_bound,upper_bound+1):
                print(f"{data[index][0]} - {data[index][1]}")
            return
        elif data[mid][1] < 6.0:
            left = mid+1
        else:
            right = mid-1
        mid = (left + right) // 2


binary_search(data)

end_time = time.time()
execution_time = end_time-start_time
# print(execution_time)

class Algorithms(StageTest):

    @dynamic_test()
    def test(self):
        result = ['Le clown et ses chiens - 6.0', 'Repas de bébé - 6.0', 'Choque de dos transatlánticos - 6.0',
                     "Grandma's Reading Glass - 6.0",
                     'Soldiers of the Cross - 6.0', 'Jack and the Beanstalk - 6.0',
                     "Les aventures d'un voyageur trop pressé - 6.0",
                     'Hiawatha, the Messiah of the Ojibway - 6.0', 'Le pêcheur de perles - 6.0',
                     'Railroad Smashup - 6.0',
                     "Les débuts d'un chauffeur - 6.0", 'Raffles, the Amateur Cracksman - 6.0',
                     'Flugten fra seraillet - 6.0', 'La Dolores - 6.0',
                     'The Helping Hand - 6.0', "The King's Messenger - 6.0", 'A Smoked Husband - 6.0',
                     'Smert Ioanna Groznogo - 6.0', 'Edgar Allan Poe - 6.0',
                     'The Sacrifice - 6.0', 'The Sealed Room - 6.0', 'The Trick That Failed - 6.0',
                     "Alice's Adventures in Wonderland - 6.0",
                     'The Face at the Window - 6.0', 'Hamlet - 6.0', 'The Man - 6.0',
                     'A Mother\'s Devotion; or, The Firing of the Patchwork Quilt - 6.0',
                     'Never Again - 6.0', 'Re Lear - 6.0', 'Captain Midnight, the Bush King - 6.0',
                     'A Christmas Carol - 6.0', 'Cinderella - 6.0',
                     'Les misérables - Époque 1: Jean Valjean - 6.0', 'La caduta di Troia - 6.0',
                     'The Goddess of Sagebrush Gulch - 6.0',
                     'The Legend of Sleepy Hollow - 6.0', 'Max, professeur de tango - 6.0',
                     'De molens die juichen en weenen - 6.0',
                     'Vampyrdanserinden - 6.0', 'Zigomar contre Nick Carter - 6.0', "'Arriet's Baby - 6.0",
                     "Barney Oldfield's Race for a Life - 6.0", 'The Count of Monte Cristo - 6.0',
                     'From Dusk to Dawn - 6.0',
                     'A Game of Pool - 6.0', 'Granddad - 6.0', 'A House Divided - 6.0', 'The Law and the Outlaw - 6.0',
                     'The Little Tease - 6.0', 'Robin Hood - 6.0', 'Ten Nights in a Barroom - 6.0',
                     'Strashnaya mest - 6.0',
                     "Tess of the D'Urbervilles - 6.0", 'Traffic in Souls - 6.0', 'Two Men of the Desert - 6.0',
                     'Anna Karenina - 6.0',
                     'Cinderella - 6.0', 'Dough and Dynamite - 6.0', 'The Egyptian Mummy - 6.0',
                     'His Musical Career - 6.0',
                     'His New Profession - 6.0', 'The Lost Paradise - 6.0', 'The Masquerader - 6.0',
                     'Tess of the Storm Country - 6.0',
                     'An American Gentleman - 6.0', "Boobley's Baby - 6.0", 'Britain Prepared - 6.0',
                     'A Burlesque on Carmen - 6.0',
                     'Colored Villainy - 6.0', 'The Coward - 6.0',
                     'The Dinosaur and the Missing Link: A Prehistoric Tragedy - 6.0',
                     'How Molly Malone Made Good - 6.0', 'A Jitney Elopement - 6.0', "A Lover's Lost Control - 6.0",
                     'A Lucky Strike - 6.0',
                     "Fatty and Mabel's Simple Life - 6.0", 'Max et le sac - 6.0', 'A Night Out - 6.0',
                     'The Sable Lorcha - 6.0',
                     'When Love Took Wings - 6.0', 'Young Romance - 6.0', 'Bobby Bumps at the Circus - 6.0',
                     'Die Börsenkönigin - 6.0',
                     'Civilization - 6.0', 'Davy Crockett - 6.0', 'Doctoring a Leak - 6.0', "Dolly's Scoop - 6.0",
                     'The Extra Man and the Milk-Fed Lion - 6.0', 'Farkas - 6.0', 'Fången på Karlstens fästning - 6.0',
                     'Gretchen the Greenhorn - 6.0',
                     'The Habit of Happiness - 6.0', 'Hoffmanns Erzählungen - 6.0', 'Hulda from Holland - 6.0',
                     'Into the Primitive - 6.0']
        user_start_time = time.time()
        program = TestedProgram()
        output = program.start()
        user_end_time = time.time()
        user_execution_time = user_end_time-user_start_time
        # print(user_execution_time)
        output = output.rstrip().split('\n')
        if len(output) != 95:
            return CheckResult.wrong("Are you sure you have printed all movies with rating 6 in the expected format?")
        elif '\\n' in output[0]:
            return CheckResult.wrong(r"Please remove \n from the output")
        elif '6.0' not in output[0]:
            return CheckResult.wrong("Convert ratings to float, not integer")
        elif '-' not in output[0]:
            return CheckResult.wrong("Print movie and title separated by a ' - '")
        elif set(output) != set(result):
            return CheckResult.wrong("Are you sure you have printed all movies with rating 6 in the expected format without any quotes?")
        elif abs(execution_time-user_execution_time) > 1:
            return CheckResult.wrong("Please use Merge Sort for sorting and Binary Search for searching.")

        return CheckResult.correct()


if __name__ == '__main__':
    Algorithms().run_tests()
