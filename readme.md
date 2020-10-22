# Grade by MAIL
***
A script for marking files made for the Mun AI Lab.

## Setup
The grader assumes you have a main 'assignment' directory where all assignments will be placed.
For 4300 and 4303 an example directory structure is as follows:
```
Assignments
├── A1
│   ├── bin
│   ├── src
│   ├── A1_MARKS.txt
│   └── submissions
├── A2
│   ├── bin
│   ├── src
│   ├── A2_MARKS.txt
│   └── submissions
```

The 'submissions' directory was not part of the assignment as downloaded, and instead is the output of the zip file of the batch download from d2l.
This is important, as d2l names files using a specific convention that the grader uses to parse files.
The assignment root folder, as well as the destination source folder must be set in `config.ini`.

## Usage
The first step is to run ```grader.py -i [assignment name]``` which will initialize the project.
This step goes through the submissions directory, and renames every file from its d2l convention to simply `sid filename.ext`
Where SID is the student id, followed by the name of the file as submitted.
In cases of duplicate submissions, the d2l filename includes the time of submission, and the initialization step will delete the older of any duplicate files.
Afterwards, any files whose names did not meet the convention will be shown, with the option to delete. It is not nessecary to delete them, as the initialization step will keep all the valid filename stored in the local grades JSON.

The Initializer will create 2 files in the local `/data` directory. A `marking_template.json` and `grades.json`. 
The grades file is a JSON directory that stores all the students submissions by ID as well as their grade, based on the marking template.
If the flag `-t` is used when initializing, the program will look for any file with the word "mark" in it, and will attempt to parse a marking template from it.
It uses a very simple regex where it looks for lines in the format `[REQUIREMENT]   nn/nn` so for example `file reading: 10/100`.
If this is the case, the grades file will track each requirement. If none is found or provided, then a simple `total/100` will be used.

After initialization, you can use the `-l` or `--load` flag to copy all files from a given student ID to the source directory.
For example `grader.py A1 -l g95rwb` will copy all files prepended with 'g95rwb' to the source directory, overwriting the files there.

To speed up this process, you can use the `-m` flag to enter marking mode. This will present a command line interface for marking all the files in the directory,
or if PySide2 is installed, then you may use `-m -g` to mark with a QT gui.

Finally, use the `-w [assignment name]` to write a text output file of all the grades. This will create a text file output of the grades as saved, ready to copy-paste into assignment feedback.
***
Obviously this is a somewhat hacky work in progress, but feel free to submit requests to improve the project. It is my hope that we can make the tool robust enough to help future graders for these classes.