import argparse
import subprocess

def run_question1():
    print("Running Question 1")
    subprocess.run(["python", "question1.py"])

def run_question2():
    print("Running Question 2")
    subprocess.run(["python", "question2.py"])

def run_question3():
    print("Running Question 3")
    subprocess.run(["python", "question3.py"])

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run specific question scripts")
    parser.add_argument(
        "question", 
        type=int, 
        choices=[1, 2, 3], 
        help="Specify which question to run: 1, 2, or 3"
    )
    args = parser.parse_args()

    if args.question == 1:
        run_question1()
    elif args.question == 2:
        run_question2()
    elif args.question == 3:
        run_question3()
