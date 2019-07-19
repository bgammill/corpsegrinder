import argparse
from git import Repo

class CorpseGrinder:
    def __init__(self):
        # argument parsing
        self.parser = argparse.ArgumentParser(description='Calculate and output the most-used words in a git repo.')
        self.parser.add_argument('--branch', type=str, help='Branch name.', default='master')
        self.parser.add_argument('--max', type=int, help='Maximum number of messages to display.', default=50)
        self.parser.add_argument('--repo', type=str, help='Absolute path to repo.')
        self.args = self.parser.parse_args()
        if self.args.repo is None:
            self.parser.print_help()
            self.parser.exit()

        # properties
        self.branch = self.args.branch
        self.repo = Repo(self.args.repo)
        self.max = self.args.max
        self.commits = list(self.repo.iter_commits(self.args.branch))
        self.words = {}
        self.sorted_words = []

        # initial stuff
        self.populate_words()
        self.sort_words()
        self.print_words()

    def populate_words(self):
        # for each commit in the commits we loaded earlier
        for commit in self.commits:
            # set the commit message to lowercase
            msg = commit.message.lower()
            # if the commit message does not contain "merge branch"
            if not "merge branch" in msg:
                # remove characters we do not want, then split the commit message by space
                #split = msg.replace('\n', '').replace(',', '').replace("'", "").replace("-", "").split(' ')
                split = msg.replace('\n', '').split(' ')
                # for each word in the commit message we split up
                for word in split:
                    # if the word is already in the dictionary
                    if word in self.words:
                        # increase its count
                        self.words[word] += 1
                    # otherwise
                    else:
                        # initialize it with its first value
                        self.words[word] = 1

    def sort_words(self):
        self.sorted_words = sorted(self.words.items(), key=lambda x: x[1], reverse=True)

    def print_words(self):
        if self.max > len(self.sorted_words) - 1:
            # set max_messages to length of sorted_words
            self.max = len(self.sorted_words)

        # loop through numbers 0 through max_messages
        for num in range(0, self.max):
            # print the word and count
            print(self.sorted_words[num][0] + " " + str(self.sorted_words[num][1]))

c = CorpseGrinder()
