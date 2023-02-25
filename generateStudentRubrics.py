import ssl
from shutil import copy2
from urllib.request import urlopen, urlretrieve
from os import mkdir, chdir, remove, system, name

def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")

def header():
    clear()
    print("Welcome to Jimmy's Student Rubric Generator!")

def choice(values):
    x = -1
    while x < 0 or x >= len(values):
        header()
        i = 1
        for value in values:
            print(str(i) + ": " + value)
            i += 1
        try:
            x = int(input("Number: ")) - 1
        except:
            pass
    return values[x]

def namelist():
    # http://gradersections.ducta.net/
    data = urlopen("https://docs.google.com/spreadsheets/d/17PrxZS_BnBqAsFfVVP6oL08TvymFIFqbIXijq63r9LI/gviz/tq?tqx=out:csv&sheet=Student-Grader-GraderSection")
    sections = {}
    for info in data:
        info = info.decode("utf-8").replace("\n", "").split(",")
        if info[0].find("Grader SECTION") == 1 and len(info[0]) == 19:
            grader = info[1].replace("\"", "")
            info[4] = [i.capitalize() for i in info[4].replace("\"", "").replace("-", "").split()]
            info[5] = [i.capitalize() for i in info[5].replace("\"", "").replace("-", "").split()]
            student = "".join(info[5]) + "".join(info[4])
            if student:
                students = sections.get(grader)
                if (students):
                    sections[grader].append(student)
                else:
                    sections[grader] = [student]
    data.close()
    return sections[choice([i for i in sections.keys()])]


def assignments():
    data = urlopen("https://jpweb.ml/grader-rubrics/rubrics.txt")
    rubrics = []
    for info in data:
        rubrics.append(info.decode("utf-8").replace("\n", ""))
    data.close()
    return choice(rubrics)
                
def generate(assignment, names):
    folder = assignment[:-5] + "s"
    mkdir(folder)
    chdir(folder)
    urlretrieve("https://jpweb.ml/grader-rubrics/" + assignment, assignment)
    for sname in names:
        copy2(assignment, sname + "-" + assignment)
    remove(assignment)

if name != "nt":
    ssl._create_default_https_context = ssl._create_unverified_context
a = assignments()
n = namelist()
generate(a, n)
clear()
print("Rubrics generated!")
input("Press enter to close...")