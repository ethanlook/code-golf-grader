from functools import total_ordering
import os
import subprocess
import json
from datetime import datetime
from uuid import uuid4
import random

SUBMISSIONS_FILENAME = './submissions.txt'
SOLUTIONS_DIRNAME = './solutions'
RESULTS_DIRNAME = './results'
NUMBER_OF_WINNERS = 3
NUM_PROBLEMS = 6


def shell_exec(string_of_args):
    return subprocess.call([s.strip() for s in string_of_args.split(' ')])

class Contest():

    def __init__(self, solutions={}):
        self.contestants = []
        self.solutions = solutions

    def add_contestant(self, contestant):
        self.contestants.append(contestant)

    def get_top_n_names(self, n):
        return reversed(sorted(self.contestants[:n]))

    def dump_all_results(self):
        results_id = uuid4().hex
        shell_exec('touch {}/{}.txt'.format(RESULTS_DIRNAME, results_id))
        with open('{}/{}.txt'.format(RESULTS_DIRNAME, results_id), 'wr') as results_file:
            for i, contestant in enumerate(reversed(sorted(self.contestants))):
                results_file.write('\n{}.\n{}'.format(i+1, contestant))
            results_file.write('\n')
        return results_id


@total_ordering
class Contestant():

    def __init__(self, name):
        self.name = name
        self.scores = []
        for i in range(NUM_PROBLEMS):
            self.scores.append(0)

    def add_result(self, problem, score):
        self.scores[int(problem) - 1] = score

    def get_total_score(self):
        return sum(self.scores)

    def __eq__(self, other):
        return self.name == other.name and self.get_total_score() == other.get_total_sccore()

    def __gt__(self, other):
        return self.get_total_score() < other.get_total_score()

    def __repr__(self):
        s = '\n---------{}--------\n'.format(self.name)
        for i, score in enumerate(self.scores):
            s += '\tproblem {}: {}\n'.format(i+1, score)
        s += '\ttotal: {}'.format(self.get_total_score())
        return s

def extract_problem_number(filename):
    for char in filename:
        if char.isdigit():
            return char
    return False

def load_solutions():
    solns = [(extract_problem_number(solution), open('{}/{}'.format(SOLUTIONS_DIRNAME, solution), 'r')) for solution in os.listdir(SOLUTIONS_DIRNAME)]
    soln_map = {}
    for problem_number, soln_file in solns:
        soln_map[problem_number] = soln_file
    return soln_map

def full_fp(github_dir):
    return '{}/github_dirs/{}/'.format(os.getcwd(), github_dir)

def file_lines_to_list(filename):
    return open(filename, 'r').readlines()

def list_open_files(directory):
    return [open(fname, 'r') for fname in os.listdir(full_fp(directory))]

def extract_username(repo_url):
    splitted = repo_url.split('/')
    return splitted[splitted.index('github.com') + 1]

def clone_github_repo(repo):
    shell_exec('git clone {} ./github_dirs/{}-{}/'
               .format(repo, extract_username(repo), random.randint(0, 10000)))


def file_size(fname):
    return os.path.getsize(fname)

def evaluate_correctness(soln_map, submitted):
    solution = soln_map[extract_problem_number(submitted)].readlines()
    with open('{}/{}'.format(SOLUTIONS_DIRNAME, submitted), 'r') as submission:
        submission_lines = submission.readlines()
        for i, line in enumerate(submission_lines):
            if line.lower().strip() != solution[i].lower().strip():
                return False
    return True

def build_submission_dir():
    githubs_list = file_lines_to_list(SUBMISSIONS_FILENAME)
    for repo_url in githubs_list:
        clone_github_repo(repo_url)

def is_txt(fname):
    return fname.split('.')[-1] == 'txt'

def get_source_for_problem(problem_number, submission_dir):
    for fname in submission_dir:
        num = extract_problem_number(fname)
        if num == problem_number:
            if not is_txt(fname):
                return fname
    return False

def get_output_for_problem(problem_number, submission_dir):
    for fname in submission_dir:
        num = extract_problem_number(fname)
        if num == problem_number:
            if is_txt(fname):
                return fname
    return False

def is_file_of_interest(fname):
    return fname[0] != '.' and fname.split('.')[-1] != 'git' and fname.split('.')[-1] != 'txt'

def run():
    shell_exec('rm -rf github_dirs')
    shell_exec('mkdir github_dirs')
    build_submission_dir()
    contest = Contest(load_solutions())
    print 'scoring...'
    for contestant in os.listdir('./github_dirs'):
        print 'evaluating contestant {}'.format(contestant)
        new_contestant_obj = Contestant(contestant)
        contest.add_contestant(new_contestant_obj)
        submission_dir = os.listdir('./github_dirs/{}'.format(contestant))
        for submission in submission_dir:
            if not is_file_of_interest(submission):
                continue
            print 'evlauating submission {}'.format(submission)
            problem_num = extract_problem_number(submission)

            source = submission
            #output = get_output_for_problem(problem_num, submission_dir)

            fsize = file_size('{}/{}/{}'.format('./github_dirs', contestant, source))
            #correct = evaluate_correctness(contest.solutions, output)
            new_contestant_obj.add_result(problem_num, fsize)


    result_name = contest.dump_all_results()
    for winner in reversed(sorted(contest.contestants[:NUMBER_OF_WINNERS])):
        print winner
    print 'result file: {}.txt'.format(result_name)

run()
