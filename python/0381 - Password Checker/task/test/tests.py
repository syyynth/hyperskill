from hstest import CheckResult, StageTest, dynamic_test, TestedProgram
import hashlib
import requests


class StageTest6(StageTest):
    valid_pwds = ["mypassword123", "youcantguessme"]
    pwned_pwds = ["12345678", "password", "mypassword"]
    exit_cmd = ["exit"]

    @dynamic_test
    def test_continuous_prompt(self):
        main = TestedProgram()
        output = main.start().lower()

        if "enter your password" not in output:
            return CheckResult.wrong("The program did not prompt for the password initially.")

        output = main.execute("test_password").lower()
        if "enter your password" not in output:
            return CheckResult.wrong("The program did not prompt for the password again.")

        return CheckResult.correct()

    @dynamic_test(data=valid_pwds)
    def test_output_hash(self, x):
        main = TestedProgram()
        main.start().lower()
        output = main.execute(x).lower()

        sha1_hash = hashlib.sha1(x.encode()).hexdigest().lower()

        if sha1_hash in output:
            return CheckResult.wrong(f"The program should NOT display the hashed password, " +
                                     "if --show-hash was not given.")

        return CheckResult.correct()

    @dynamic_test(data=pwned_pwds)
    def test_pwned_pwd(self, x):
        main = TestedProgram()
        main.start().lower()
        output = main.execute(x)

        sha1_hash = hashlib.sha1(x.encode()).hexdigest().lower()

        response = requests.get("https://api.pwnedpasswords.com/range/" + sha1_hash[0:5],
                                headers={"Add-Padding": "true"})
        results = response.text.split("\n")
        found = False
        for result in results:
            hash_suffix, count = result.lower().strip().split(":")
            if hash_suffix == sha1_hash[5:]:
                found = True
                if str(count) not in output:
                    return CheckResult.wrong(
                        "This password has been pwned " + count + " times, but your output is: \n" + output)
                else:
                    return CheckResult.correct()

    @dynamic_test(data=exit_cmd)
    def test_exit_option(self, x):
        main = TestedProgram()
        main.start()
        output = main.execute(x).lower()
        if "goodbye" not in output:
            return CheckResult.wrong("The program did not exit when the 'exit' command was entered.")
        return CheckResult.correct()

    @dynamic_test(data=valid_pwds)
    def test_show_hash_argument(self, x):
        main = TestedProgram()
        main.start("--show-hash")
        output = main.execute(x).lower()
        sha1_hash = hashlib.sha1(x.encode()).hexdigest().lower()

        if sha1_hash not in output:
            return CheckResult.wrong("The hashed password should be displayed when --show-hash is used.")

        return CheckResult.correct()


if __name__ == '__main__':
    StageTest6().run_tests()
