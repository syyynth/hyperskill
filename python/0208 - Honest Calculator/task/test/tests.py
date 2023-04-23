from hstest import StageTest, CheckResult, WrongAnswer, dynamic_test, TestedProgram

msg = ["Enter an equation",
       "Do you even know what numbers are? Stay focused!",
       "Yes ... an interesting math operation. You've slept through all classes, haven't you?",
       "Yeah... division by zero. Smart move...",
       "Do you want to store the result? (y / n):",
       "Do you want to continue calculations? (y / n):",
       " ... lazy",
       " ... very lazy",
       " ... very, very lazy",
       "You are",
       "Are you sure? It is only one digit! (y / n)",
       "Don't be silly! It's just one number! Add to the memory? (y / n)",
       "Last chance! Do you really want to embarrass yourself? (y / n)"
]


def add_enter(txt):
    return "\n".join([txt, msg[0]])


def add_memory(txt):
    return "\n".join([txt, msg[4]])


data = [(("4 * 5.0", "\n".join([msg[9] + msg[6], add_memory("20.0")])), ("n", msg[5]), ("n", "")),
        (("2 + 5.5", add_memory("7.5")), ("y", msg[5]), ("y", msg[0]), ("M - 9", add_memory("-1.5")), ("n", msg[5]), ("n", "")),
        (("225 / 15", add_memory("15.0")), ("y", msg[5]), ("y",msg[0]),
         ("1 * 5", "\n".join([msg[9] + msg[6] + msg[7], add_memory("5.0")])), ("y", msg[10]), ("y", msg[11]), ("n", msg[5]), ("y", msg[0]),
        ("M - 10", add_memory("5.0")), ("y", msg[10]), ("y", msg[11]), ("y", msg[12]), ("y", msg[5]), ("y", msg[0]),
         ("M / M",  "\n".join([msg[9] + msg[6], add_memory("1.0")])), ("n", msg[5]), ("n", "")),
       ]  # (input data, msg sentence])


class HonestCalc(StageTest):
    @dynamic_test(data=data)
    def test(self, *items):
        pr = TestedProgram()
        output = pr.start()
        if msg[0] not in output:
            return CheckResult.wrong(f"Expected: ({msg[0]});\nFound:    ({output.strip()})")
        for item in items:
            output = pr.execute(item[0])
            if item[1] != output.strip():
                return CheckResult.wrong(f"Expected:\n{item[1]}\nFound:\n{output.strip()}")
        if not pr.is_finished():
            return CheckResult.wrong("Your program unnecessarily waiting for input.")
        return CheckResult.correct()


if __name__ == '__main__':
    HonestCalc().run_tests()
