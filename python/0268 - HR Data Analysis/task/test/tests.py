import ast
from hstest.stage_test import List
from hstest import *

answer_1 = {(0, 'high'): {'IT': 193.0,  'management': 196.0,  'marketing': 173.0,  'product_mng': 172.0,  'sales': 190.0,  'support': 214.0,  'technical': 193.0},
            (0, 'low'): {'IT': 198.5,  'management': 208.0,  'marketing': 199.5,  'product_mng': 198.5,  'sales': 198.0,  'support': 194.5,  'technical': 197.0},
            (0, 'medium'): {'IT': 199.0,  'management': 201.0,  'marketing': 185.0,  'product_mng': 202.0,  'sales': 198.0,  'support': 196.0,  'technical': 202.0},
            (1, 'high'): {'IT': 155.0,  'management': 259.0,  'marketing': 148.5,  'product_mng': 149.0,  'sales': 241.5,  'support': 237.0,  'technical': 157.5},
            (1, 'low'): {'IT': 235.0,  'management': 230.5,  'marketing': 155.0,  'product_mng': 218.0,  'sales': 224.5,  'support': 219.0,  'technical': 244.0},
            (1, 'medium'): {'IT': 198.0,  'management': 235.0,  'marketing': 157.0,  'product_mng': 154.5,  'sales': 225.0,  'support': 221.0,  'technical': 232.0}}

answer_2 = {('max', 'last_evaluation', 0): {2: 1.0, 4: 1.0, 5: 1.0, 6: 1.0, 10: 1.0},
            ('max', 'last_evaluation', 1): {2: 0.99, 4: 0.9, 5: 0.91, 6: 0.71, 10: 0.94},
            ('max', 'satisfaction_level', 0): {2: 1.0, 4: 1.0, 5: 1.0, 6: 1.0, 10: 0.99},
            ('max', 'satisfaction_level', 1): {2: 0.94,  4: 0.94,  5: 0.82,  6: 0.81,  10: 0.85},
            ('mean', 'last_evaluation', 0): {2: 0.72,  4: 0.77,  5: 0.82,  6: 0.77,  10: 0.72},
            ('mean', 'last_evaluation', 1): {2: 0.69,  4: 0.75,  5: 0.61,  6: 0.52,  10: 0.63},
            ('mean', 'satisfaction_level', 0): {2: 0.7,  4: 0.48,  5: 0.62,  6: 0.59,  10: 0.66},
            ('mean', 'satisfaction_level', 1): {2: 0.65,  4: 0.6,  5: 0.66,  6: 0.62,  10: 0.51},
            ('min', 'last_evaluation', 0): {2: 0.37, 4: 0.36, 5: 0.38, 6: 0.37, 10: 0.37},
            ('min', 'last_evaluation', 1): {2: 0.52, 4: 0.42, 5: 0.37, 6: 0.38, 10: 0.48},
            ('min', 'satisfaction_level', 0): {2: 0.09,  4: 0.09,  5: 0.09,  6: 0.12,  10: 0.14},
            ('min', 'satisfaction_level', 1): {2: 0.29,  4: 0.15,  5: 0.23,  6: 0.48,  10: 0.22}}


class PivotTest(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase(time_limit=15000)]

    def check(self, reply: str, attach):

        reply = reply.strip()

        if len(reply) == 0:
            return CheckResult.wrong("No output was printed")

        if reply.count('{') < 1 or reply.count('}') < 1:
            return CheckResult.wrong('Print output as two dictionaries')

        num_of_answers = len(reply.split('\n'))
        if num_of_answers != 2:
            return CheckResult.wrong(f"Wrong number of answers. Expected 2, found {num_of_answers}.\n"
                                     f"Make sure that each answer is printed on a separate line.")

        reply_1 = reply.split('\n')[0]
        reply_2 = reply.split('\n')[1]


        index_from_1 = reply_1.find('{')
        index_to_1 = reply_1.rfind('}')
        dict_str_1 = reply_1[index_from_1: index_to_1 + 1]

        index_from_2 = reply_2.find('{')
        index_to_2 = reply_2.rfind('}')
        dict_str_2 = reply_2[index_from_2: index_to_2 + 1]
        try:
            user_dict_1 = ast.literal_eval(dict_str_1)
            user_dict_2 = ast.literal_eval(dict_str_2)
        except Exception as e:
            return CheckResult.wrong(f"Seems that output is in wrong format.\n"
                                     f"Make sure you use only the following Python structures in the output: string, int, float, list, dictionary")

        if not isinstance(user_dict_1, dict):
            return CheckResult.wrong('Print the first pivot table as a dictionary')

        if not isinstance(user_dict_2, dict):
            return CheckResult.wrong('Print the second pivot table as a dictionary')

        if len(answer_1.keys()) != len(user_dict_1.keys()):
            return CheckResult.wrong(f'Answer on the 1st line should contain {len(answer_1.keys())} dict elements, found {len(user_dict_1.keys())}')

        for key in answer_1.keys():
            if key not in user_dict_1.keys():
                return CheckResult.wrong(f'Dictionary on the 1st line should contain \"{key}\" as a key')

        if len(answer_2.keys()) != len(user_dict_2.keys()):
            return CheckResult.wrong(f'Answer on the 2nd line should contain {len(answer_2.keys())} dict elements, found {len(user_dict_2.keys())}')

        for key in answer_2.keys():
            if key not in user_dict_2.keys():
                return CheckResult.wrong(f'Dictionary on the 2nd line should contain \"{key}\" as a key')

        for key in user_dict_1.keys():
            curr_user_dict = user_dict_1[key]
            try:
                curr_answer_dict = answer_1[key]
            except KeyError:
                return CheckResult.wrong(f"Looks like the {key} key should not be included in the first dictionary")
            try:
                curr_user_dict.keys()
            except AttributeError:
                return CheckResult.wrong(f'The dictionary on the first line should have dictionaries as values for the keys, appears to be single value of {type(curr_user_dict)} type instead.')


            for key_curr in curr_user_dict.keys():
                if key_curr not in curr_answer_dict.keys():
                    return CheckResult.wrong(f'Output should contain \"{key_curr}\" as a key for department')
                curr_user_val = curr_user_dict[key_curr]

                if not isinstance(curr_user_val, (int, float)):
                    return CheckResult.wrong(f'The following value: {curr_user_val}\ncorresponding to the key: {key}\n'
                                             f'with the following index: {key_curr}\nis neither of type \"int\" or \"float\".\n'
                                             f'Type detected: {type(curr_user_val)}.')

                curr_answer_val = curr_answer_dict[key_curr]
                error = abs(curr_answer_val * 0.02)
                if not curr_user_val - error < curr_answer_val < curr_user_val + error:
                    return CheckResult.wrong(
                        f'Wrong value of element with \"{key}\" key with left status \"{key_curr}\"')

        for key in user_dict_2.keys():
            curr_user_dict = user_dict_2[key]
            try:
                curr_answer_dict = answer_2[key]
            except KeyError:
                return CheckResult.wrong(f"Looks like the {key} key should not be included in the second dictionary")

            try:
                curr_user_dict.keys()
            except AttributeError:
                return CheckResult.wrong(f'The dictionary on the second line should have dictionaries as values for the keys, appears to be single value of {type(curr_user_dict)} type instead.')


            for key_curr in curr_user_dict.keys():
                if key_curr not in curr_answer_dict.keys():
                    return CheckResult.wrong(f'Output should contain \"{key_curr}\" as a key for time spent in company')
                curr_user_val = curr_user_dict[key_curr]

                if not isinstance(curr_user_val, (int, float)):
                    return CheckResult.wrong(f'The following value: {curr_user_val}\ncorresponding to the key: {key}\n'
                                             f'with the following index: {key_curr}\nis neither of type \"int\" or \"float\".\n'
                                             f'Type detected: {type(curr_user_val)}.')

                curr_answer_val = curr_answer_dict[key_curr]
                error = abs(curr_answer_val * 0.02)
                if not curr_user_val - error < curr_answer_val < curr_user_val + error:
                    return CheckResult.wrong(
                        f'Wrong value of element with \"{key}\" key with left status \"{key_curr}\"')

        return CheckResult.correct()


if __name__ == '__main__':
    PivotTest().run_tests()
