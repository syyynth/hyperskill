from hstest import StageTest, CheckResult, dynamic_test, TestedProgram
from random import randint


class XMassTreeTest4(StageTest):

    @staticmethod
    def output_len_stage1(out, high):
        out_len = len(out.splitlines())
        if out_len != int(high) + 2:
            return f"Wrong tree high. Expected {high}, founded {out_len}."
        return

    @staticmethod
    def output_ext_stage2(out, high):
        out = out.splitlines()
        ext = [("X", 0, 0), ("^", 1, 0), ("| |", len(out) - 1, -1)]
        for item, i, correction in ext:
            out_pos = [out[i].index(item) if item in out[i] else None,
                       out[i].count(item),
                       len(out[i].strip())]
            exp_pos = [int(high - 1) + correction, 1, len(item)]
            if out_pos[0] != exp_pos[0]:
                return f"Wrong position of {item} in line {i}. Expected {exp_pos[0]}, founded {out_pos[0]}."
            if out_pos[1] != exp_pos[1]:
                return f"Wrong number of {item} in line {i}. Expected {exp_pos[1]}, founded {out_pos[1]}."
            if out_pos[2] != exp_pos[2]:
                return f"Wrong width of the tree in line {i}. " \
                       f"Expected {exp_pos[2]} chars, founded {out_pos[2]} chars."
        return

    @staticmethod
    def output_pos_stage3(out, high, inter):
        out = out.splitlines()[2:-1]
        #  extra condition "ZONK" for empty line to return None
        out_pos = [[n.index(n.strip()) if (n.strip() or "ZONK") in n else None, n.count("*"), len(n.strip()), n.strip()] for n in out]
        exp_pos = [[int(high - n - 1), 2 * n + 1 - 2, 2 * n + 1] for n in range(1, high)]
        for i, value in enumerate(out_pos):
            if value[0] != exp_pos[i][0]:
                return f"Wrong position of line {i + 3}. Expected {exp_pos[i][0]}, founded {value[0]}."
            if value[2] != exp_pos[i][2]:
                return f"Wrong width of the tree in line {i + 3}. Expected {exp_pos[i][2]} chars, founded {value[2]} chars."
            if not value[3].endswith("\\"):
                return f"Tree in line {i + 3} doesn't ends with '\\'. Expected '\\', founded {value[3][-1]}."
            if not value[3].startswith("/"):
                return f"Tree in line {i + 3} doesn't starts with '/'. Expected '/', founded {value[3][0]}."

        #  checking Christmas balls
        star_line = [[(o.strip().strip("/")).strip("\\")[:-1], (o.strip().strip("/")).strip("\\")[-1]] for o in out[1:]]
        balls_line = ''.join(n[0] for n in star_line)
        max_balls = sum(range(1, len(star_line) + 1))
        nr_balls = ((max_balls - 1) // inter) + 1
        if balls_line.count("O") != nr_balls:
            return f"Wrong number of Christmas balls 'O'. Expected {nr_balls}, founded {balls_line.count('O')}."
        balls_pos = [2 * n + 1 for n in range(0, max_balls, inter)]
        for i in balls_pos:
            if balls_line[i] != "O":
                return f"The ball #{i} is not on correct position."

        #  checking nr of stars
        right_line = ''.join(n[1] for n in star_line)
        stars_max = len(balls_line) + len(right_line) - nr_balls
        nr_stars = right_line.count("*") + balls_line.count("*")
        if stars_max != nr_stars:
            return f"Wrong number of stars '*'. Expected {stars_max}, founded {nr_stars}."

        return

    @staticmethod
    def check_card(out, high, width):
        out = out.splitlines()
        lines_width = [len(n) == width for n in out]
        if len(out) != high:
            return f"Wrong card size. Expected high {high}, founded {len(out)}"
        if not all(lines_width):
            print([len(n) for n in out])
            return f"Wrong card size. At least one of the lines has not {width} width.\n" \
                   f"Check line(s): {[i + 1 for i, n in enumerate(lines_width) if not n]}"
        if out[0].count("-") != width or out[-1].count("-") != width:
            return f"{'First' if out[0].count('-') != width else 'Last'} line doesn't contain only '-'."
        for i, o in enumerate(out[1:-1]):
            if not o.startswith("|"):
                return f"Line {i + 2} doesn't starts with '|'"
            if not o.endswith("|"):
                return f"Line {i + 2} doesn't ends with '|'"
        return

    @staticmethod
    def check_sentence(out, high, width):
        out = out.splitlines()
        out = out[high - 3]
        text = "Merry Xmas"
        if out.strip("|").strip() != text:
            return f"Line {high - 2} doesn't contains the sentence '{text}'"
        if out.index(text) != (width / 2) - len(text) / 2:
            return f"The sentence '{text}' is not in the middle of the card."
        return

    @staticmethod
    def check_tops(out, tops):
        out = out.splitlines()
        text = "X"
        tops = tops.split(" ")
        tops = list(map(int, tops))
        tops = list(zip(tops[2::4], tops[3::4]))
        for top in tops:
            if out[top[0]][top[1]] != text:
                return f"The top {top} is not in correct place."
        return

    @staticmethod
    def check_hash(out, org_hash):
        out = ''.join([o[1:-1] for o in out.splitlines()[1:-1]])
        hashs = 5381
        for x in out:
            # ord(x) simply returns the unicode rep of the
            # character x
            hashs = ((hashs << 5) + hashs) + ord(x)
        # Note to clamp the value so that the hash is
        # related to the power of 2
        # print(hashs & 0xFFFFFFFF)
        if hashs & 0xFFFFFFFF != org_hash:
            return (f"The hash function for trees returned wrong value. \n"
                    f"Tops of trees are correct, the sentence and the border lines too.")
        return


    @dynamic_test
    def test1(self):
        for _ in range(3):
            main = TestedProgram()
            main.start()
            high = str(randint(3, 30))
            interval = str(randint(1, 9))
            output = main.execute(f"{high} {interval}")
            func = [self.output_len_stage1(output, high),
                    self.output_ext_stage2(output, int(high)),
                    self.output_pos_stage3(output, int(high), int(interval))]
            for f in func:
                check = f
                if check:
                    return CheckResult.wrong(check)
        return CheckResult.correct()


    @dynamic_test
    def test2(self):
        test_cases = [["7 3 7 37 4 2 10 25 11 1 5 14 10 4 9 30 5 4 16 19", 3875571371],
                      ["5 1 4 10 5 2 4 37 5 3 4 17 5 4 4 30 5 5 4 24 5 3 12 24 5 2 12 17 5 1 12 30", 1026703363]]
        for _ in range(2):
            pass
        for case in test_cases:
            main = TestedProgram()
            main.start()
            output = main.execute(case[0])
            func = [self.check_card(output, 30, 50),
                    self.check_sentence(output, 30, 50),
                    self.check_tops(output, case[0]),
                    self.check_hash(output, case[1])]
            for f in func:
                check = f
                if check:
                    return CheckResult.wrong(check)
        return CheckResult.correct()
