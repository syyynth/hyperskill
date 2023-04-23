import difflib

import git
from git import InvalidGitRepositoryError, NoSuchPathError
from hstest import CheckResult, StageTest, dynamic_test

repo_path = "./repository"
commit_message = "Greet user by the name"
commit_count = 3
branch_name = "main"
remote_name = "origin/master"
test_list = ['def main() -> None:',
             '    name = input("What\'s your name? ")',
             '    print(f"Hello, {name}!")',
             '    print("Nice to meet you!")',
             '',
             '',
             'if __name__ == "__main__":',
             '    print("Hello, world!")',
             '    main()'
             ]
file_name = "main.py"
branches_list = ['develop', 'hotfix/no-more-typos', 'main']


class GitTest(StageTest):

    def __init__(self):
        super().__init__()
        self.r = None


    @staticmethod
    def file_content_test(test_file, output_file):
        """Tests the contents of files line by line"""
        try:
            # removing blank spaces, newlines and adding a new line for each line
            test_file_data = [f"{line.strip()}\n" for line in test_file]
            output_file_data = [f"{line.strip()}\n" for line in output_file]

            # Converting generator object to list
            wrong_lines = [line for line in difflib.unified_diff(
                test_file_data, output_file_data, fromfile="test-file",
                tofile="output-file", lineterm='\n')]
        except:
            return CheckResult.wrong("Error while comparing test and output file!")

        if not wrong_lines:
            return CheckResult.correct()

        return CheckResult.wrong(
            f"Wrong line(s) found in the output file\n"
            f"{''.join(wrong_lines)}"
        )


    # Test if path is a valid git repository
    @dynamic_test()
    def test1(self):
        try:
            self.r = git.Repo(repo_path)
        except NoSuchPathError as e:
            return CheckResult.wrong(f"The path '{repo_path}' does not exist!")
        except InvalidGitRepositoryError as e:
            return CheckResult.wrong(f"'{repo_path}' is not a valid git repository!")
        except Exception as err:
            return CheckResult.wrong(f"{err} error occurred while creating the Git instance!")

        return CheckResult.correct()

    # Test active branch
    @dynamic_test
    def test2(self):
        try:
            is_valid_branch = self.r.active_branch.is_valid()
            current_branch_name = self.r.active_branch.name
        except TypeError:
            return CheckResult.wrong("Head might be detached!")
        except AssertionError:
            return CheckResult.wrong("Failed to read branch name!")
        except Exception as err:
            return CheckResult.wrong(f"{err} error occurred while reading branch name!")
        if not is_valid_branch:
            return CheckResult.wrong(f"Active branch is not valid!")
        if current_branch_name != branch_name:
            return CheckResult.wrong(f"Active branch is not '{branch_name}'!")

        return CheckResult.correct()

    # Test commit message
    @dynamic_test
    def test3(self):
        if self.r.commit().message.strip() == commit_message:
            return CheckResult.correct()
        return CheckResult.wrong(f"Commit message should be '{commit_message}'!")

    # Test commit count
    @dynamic_test
    def test4(self):
        if self.r.commit().count() == commit_count:
            return CheckResult.correct()
        return CheckResult.wrong(f"Commit count should be '{commit_count}'!")

    # Test the file and the content
    @dynamic_test
    def test5(self):
        h = self.r.commit().binsha.hex()
        try:
            b = self.r.blame(h, file_name)
        except:
            return CheckResult.wrong(f"'{file_name}' not found in the commit!")

        # Adding unchanged and changed lines to the list
        commit_content = []
        for item in b:
            for line in item[-1]:
                commit_content.append(line)
        # print(commit_content)
        return GitTest.file_content_test(test_list, commit_content)

    # Test existence of branches
    @dynamic_test
    def test6(self):
        branches = [b.name for b in self.r.branches]
        for b in branches_list:
            if b not in branches:
                return CheckResult.wrong(f"Branch '{b}' not found!")
        return CheckResult.correct()

    # Test existence of remote branch definition
    @dynamic_test
    def test7(self):
        try:
            if self.r.remotes:
                return CheckResult.correct()
            return CheckResult.wrong("\nRemote branch settings does not found!")
        except:
            return CheckResult.wrong("\nDirectory not found or failure during executing git command!")


if __name__ == '__main__':
    GitTest().run_tests()
