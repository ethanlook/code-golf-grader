from functools import total_ordering
import os
import subprocess
import json
from datetime import datetime
from uuid import uuid4

SUBMISSIONS_FILENAME = './submissions.txt'
SOLUTIONS_DIRNAME = './solutions'
RESULTS_DIRNAME = './results'
NUMBER_OF_WINNERS = 3


def shell_exec(string_of_args):
    return subprocess.call(string_of_args.split(' '))

class Contest():

    def __init__(self, solutions={}):
        self.contestants = []
        self.solutions = solutions

    def add_contestant(self, contestant):
        self.contestants.append(contestant)

    def get_top_n_names(self, n):
        return sorted(self.contestants[:n])

    def dump_n_winners_results(self, n):
        results_id = uuid4().hex
        shell_exec('touch {}/{}.txt'.format(RESULTS_DIRNAME, results_id))
        with open('{}/{}.txt'.format(RESULTS_DIRNAME, results_id), 'wr') as results_file:
            for winner in self.get_top_n_names(n):
                dump = '\n{}\n---------------------------\n'.format(winner.name)
                for problem in winner.scores:
                    result = winner.scores[problem]
                    dump += '\t{}: file size: {}, correct? {}, score: {}\n'.format(problem, result[0], result[1], result[2])
                dump += '\n\tTotal score: {}\n'.format(winner.get_total_score())
                results_file.write(dump)
        return results_id
        

def grade(fsize, correctness):
    ''' This is the criterion for score
    '''
    return float((correctness + 0.5)) / fsize


@total_ordering
class Contestant():
    
    def __init__(self, name):
        self.name = name
        self.scores = {}
        self.grading_criteria = grade

    def add_result(self, problem, score):
        self.scores[problem] = score

    def get_total_score(self):
        running_total = 0
        for prob_num in self.scores:
            fsize = self.scores[prob_num][0]
            correctness = self.scores[prob_num][1]
            running_total += self.grading_criteria(fsize, correctness)
        return running_total

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.get_total_score() > other.get_total_score()
    

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
    return splitted[splitted.find('github.com') + 1]

def clone_github_repo(repo):
    shell_exec('git clone {} ./github_dirs/{}'
               .format(repo, extract_username(repo)))

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
            output = get_output_for_problem(problem_num, submission_dir)

            fsize = file_size('{}/{}/{}'.format('./github_dirs', contestant, source))
            correct = evaluate_correctness(contest.solutions, output)
            new_contestant_obj.add_result(problem_num, (fsize, correct, grade(fsize, correct)))
    
    result_name = contest.dump_n_winners_results(NUMBER_OF_WINNERS)
    shell_exec('cat {}/{}.txt'.format(RESULTS_DIRNAME, result_name))

run()














    # ingest github directories from text file
    # for each github directory
        # print "scoring person..."
        # clone directory
        # for each submitted-problem in directory
            # print "scoring problem...", sleep(1)
            # get size of file
            # check for correctness
            # add (problem_id, size_of_file, correctness) to records under person's github name
            # print "score: {}'

# print "finding top 3.."
# find top 3
# print "number 3:...", sleep(1), "name!"
# print "number 2:...", sleep(1), "name!"
# print "number 1:...", sleep(1), "name!"
# return winners

