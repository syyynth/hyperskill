from hstest import CheckResult, TestedProgram, StageTest, dynamic_test, WrongAnswer
import string
# test featuring the vigenere cipher with provided clues


def encoder_4(message, keyword):
    # making the encoded message
    # uses a vigenere cypher and the string.ascii_lowercase alphabet string
    # the shift for encoding is determined by the keyword's index, cycling through the keyword
    # spaces ' ' are not present in the string, so they are replaced by 'x's
    message_list = list(message.lower())
    message_list = ['x' if ' ' == letter else letter for letter in message_list]
    message_encoded_list = []
    for message_index in range(len(message_list)):
        keyword_index = message_index % len(keyword)
        letter = message_list[message_index]
        key_letter = keyword[keyword_index]
        letter_ascii_index = string.ascii_lowercase.index(letter)
        key_letter_ascii_index = string.ascii_lowercase.index(key_letter)
        message_encoded_list.append(string.ascii_lowercase[(letter_ascii_index + key_letter_ascii_index) % 26])
    message_encoded = ' '.join(message_encoded_list)
    return message_encoded


class DecipherTest(StageTest):
    test_data = [
        # first message, second message, keyword
        # the keyword must be shorter than the first message
        # will be inputted as:
        #  non-encoded message
        #  the same message as before but encoded in a vigenere cipher
        #  the keyword length
        #  another encoded message
        ['t h e x k e y w o r d x w a s x b', 'less easy', 'b'],
        ['i x h o p e x t h a t x y o u x c a n x f i g u r e x t h i s x o u t', 'please come and eat more pie because i have been feeding the leftovers to my dog and she is getting fat', 'pie'],
        ['s e c r e t x m e s s a g e', 'i am glad that my dog cannot read the vigenere cipher yet', 'secret'],
        ['k e y w o r d', 'this is super fun', 'key'],
        ['s e c r e t s', 'thanks for humoring me with this project', 'word'],
        ['h u s h x h u s h', 'i hope that you had fun too', 'friend'],
        ['i x h a v e x a n x i d e a x f o r x a n x a l t e r n a t i v e x s e c r e t', 'say would you like to make a secret base', 'treehouse'],
        ['w e x c o u l d x m a k e x a x t r e e h o u s e x i n x t h e x w o o d s', 'that way we could talk out loud and look at animals', 'hideyhole'],
        ['w e x c o u l d x d i s g u i s e x o u r s e l v e s x a s x b e a r s', 'if we bring pies along the smell might give us away', 'sniff'],
        ['w e x m i g h t x g e t x s o m e x u n i n v i t e d x g u e s t s', 'but maybe my dog could stop by sometimes', 'dog'],
        ['a l t e r n a t i v e l y', 'maybe we could have multiple rotating treehouses based on the moon to hide better', 'lunar'],
        ['s c r i b b l e x s c r a b b l e', 'i look forward to out future correspondence', 'overnout']
    ]

    @dynamic_test(data=test_data)
    def test(self, *x):
        message_1 = x[0]
        encoded_message_1 = encoder_4(message=x[0].replace(' ', ''), keyword=x[2])
        keyword_length = len(x[2])
        encoded_message_2 = encoder_4(message=x[1], keyword=x[2])

        pr = TestedProgram()
        pr.start()
        output = pr.execute(stdin=f'{keyword_length}\n{message_1}\n{encoded_message_1}\n{encoded_message_2}')
        if not output:
            raise WrongAnswer('Your program did not print anything.')
        if not output.isascii():
            raise WrongAnswer('This string contains non-ascii values.')
        output_cleaned = output.lower().strip().replace(' ', '')
        if x[0].lower().replace('x', ' ').replace(' ', '') in output_cleaned:
            raise WrongAnswer('This may be the first deciphered message. '
                              'Please only print the second deciphered message.')
        check = x[1].lower().replace('x', ' ').replace(' ', '') in output_cleaned
        return CheckResult(check, f'Wrong message returned. \nYou printed: {output}.')


if __name__ == '__main__':
    DecipherTest().run_tests()
