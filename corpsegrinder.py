import argparse
import json
import os
import re
from git import Repo

# arguments
parser = argparse.ArgumentParser(description='Calculate and output the most-used words in a git repo.')
parser.add_argument('--branch', type=str, help='Branch name.', default='master')
parser.add_argument('--max', type=int, help='Maximum number of messages to display.', default=50)
parser.add_argument('--repo', type=str, help='Absolute path to repo.')
args = parser.parse_args()
if args.repo is None:
    parser.print_help()
    parser.exit()

# load repo from directory
repo = Repo(args.repo)

# get all commits from 'Launch' branch
commits = list(repo.iter_commits(args.branch))

# create a dictionary to hold words and count
words = {}

# for each commit in the commits we loaded earlier
for commit in commits:
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
            if word in words:
                # increase its count
                words[word] += 1
            # otherwise
            else:
                # initialize it with its first value
                words[word] = 1

# sort the dictionary by the count (number of times word has occurred)
sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)

# create a variable to hold user input (number of commit messages)
max_messages = args.max
# if max_messages is greater than the length of sorted_words minus 1 to
# account for range starting at 0
if max_messages > len(sorted_words) - 1:
    # set max_messages to length of sorted_words
    max_messages = len(sorted_words)

# loop through numbers 0 through max_messages
for num in range(0, max_messages):
    # print the word and count
    print(sorted_words[num][0] + " " + str(sorted_words[num][1]))
