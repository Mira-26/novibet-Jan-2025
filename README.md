# novibet-Jan-2025
Assessment project for Novibet - Senior Data Engineer position 


Initial Setup

        git clone <repo_url>
        cd codebase


Install Dependencies

        pip install -r requirements.txt

Project Structure

        src/python/                     : The main directory where all Python scripts are located
        main.py                         : A script to run specific analysis (Question 1, 2, or 3) based on user input
        source_files/football_datasets  : contains the source files
        question1.py                    : computes the Top 5 Scorers per league and season
        question2.py                    : Determines which half has the most goals from corners per league and season
        question3.py                    : Finds the top 3 La Liga Teams based on shots on target
        src/python/output/              : Stores the results in Parquet format        
        access_question1.py             : Loads and displays the stored results for question 1
        access_question2.py             : Loads and displays the stored results for question 2
        access_question3.py             : Loads and displays the stored results for question 3
        requirements.txt                : lists all required dependencies
        README.md                       : Provides setup instructions, project details, and usage guidelines





Program execution

        Each question can be executed independently using main.py and passing the relevant question number:

        python src/python/main.py 1
        python src/python/main.py 2
        python src/python/main.py 3

Access Stored Results

        Each parquet file which derives from each question can be accessed independently with the access_question*.py files:

        python access_question1.py
        python access_question2.py
        python access_question3.py


License

        This project is licensed under the MIT License.