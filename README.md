# KNU 2023 Software Design Final Exam: Detecting all types of each member variable

Your submission must satisfy the following requirements:

* R1. Shall initialize your assignment repository from the url of GitHub Classroom.
* R2. Write your `analyzer.py` in the repository.
* R3. Test your `analyzer.py` by using `pytest`.
* R4. You need to let your TA know your repository URL and your student ID together via Slack.
* R5. Check out `test_analyzer1.py` to figure out the output format.
* R6. Assume that there are "NO" nested classes/methods, overloaded methods, and anonymous classes.
* R7. Assume that there are nested directories in the input path.
* R8. The function `collect_uninvoked_methods(...)` takes a path of a directory containing multiple Python source code files together with a target class name (e.g., `Session`), and produces a map of member variables of the target classes. The keys of the map are member variables of the target classes, and the values are a set of all types ever assigned to each member variable. If there is no value, the value should be an empty set (`set()`).


## Note:

* N1. `pytest` (based on `test_analyzer1.py`) is just for validating your program. The final grading will be made by other test cases.
* N2. Submissions via GitHub Classroom will only be accepted. Submissions via LMS or any other means are not accepted.
* N3. DO NOT change files in this repository except for `invoke_analyzer.py`. Adding new files are allowed.
* N4. Late submissions after 2:45pm are *NOT* allowed.
