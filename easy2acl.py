#!/usr/bin/env python3

#,----
#| easy2acl.py - Convert data from EasyChair for use with aclpub                
#|                                                                              
#| Author: Nils Blomqvist
#|                                                                              
#| Documentation
#| -------------
#| Full documentation at http://github.com/nblomqvist/easy2acl.    
#|                                                                              
#| Quick reference                                                              
#| ---------------                                                              
#| Before running this script, your file structure should look like this:       
#|                                                                              
#| |-- easy2acl.py                                                              
#| |-- submissions                                                              
#| |-- accepted                                                                 
#| `-- pdf                                                                      
#|     |-- ..._submission_1.pdf                                                 
#|     |-- ..._submission_2.pdf                                                 
#|     `-- ...                                                                  
#|                                                                              
#| Run the script:                                                              
#|                                                                              
#|     $ ./easy2acl.py                                                          
#|                                                                              
#| When the script has finished, you will find the files 'db' and 'final.tar.gz'
#| in the same folder.                                                          
#`----

from shutil import copy, rmtree
from subprocess import Popen
from os import mkdir, path, listdir
from PyPDF2 import PdfFileReader
from unicode_tex import unicode_to_tex

def texify(string):
    """Return a modified version of the argument string where non-ASCII symbols have
    been converted into LaTeX escape codes.

    """
    output = ''
    
    for w in string.split():
        output += unicode_to_tex(w) + ' '
    output = output.strip()
    
    return output

#,----
#| Append each accepted submission, as a tuple, to the 'accepted' list.
#`----
accepted = []             

with open('accepted') as accepted_file:
    for line in accepted_file:
        entry = line.split("\t")

        if entry[-1][0] == "A": # if it's "ACCEPT"
            #print(entry[-1])
            submission_id = entry[0]
            title = entry[1]

        accepted.append((submission_id, title))

#,----
#| Append each submission, as a tuple, to the 'submissions' list.
#`----
submissions = []

with open('submissions') as submissions_file:
    for line in submissions_file:
        entry = line.split("\t")
        submission_id = entry[0]
        authors = entry[1].replace(' and', ',').split(', ')
        title = entry[2]

        authors_clean = []
        for author in authors:
            author_fullname = author.split(' ')
            author_first_name = author_fullname[0]
            author_last_name = ''

            for last in author_fullname[1:]:
                author_last_name += last + ' '
            author_last_name.strip()
                
            authors_clean.append((author_last_name, author_first_name))

        submissions.append((submission_id, title, authors_clean))

#,----
#| Append a tuple of information about each PDFs into list 'pdfs'.
#`----
pdfs = []

for pdf in listdir('pdf'):
    current_path = path.join('pdf', pdf)
    file = PdfFileReader(open(current_path, 'rb'))

    no_of_pages = file.getNumPages()
    submission_id = pdf[:-4].rsplit('_', 1)[1]
    final_path = path.join('final', pdf)

    pdfs.append((submission_id, no_of_pages, current_path, final_path))

#,----
#| Add the submissions whose submission ID is found in the 'accepted' list to a
#| new list 'final_papers'. A match must made for both the submission ID and the
#| title (just in case).
#|                                                                           
#| Copy the PDFs whose submission ID is found in the 'accepted' list to a
#| directory 'final'.
#|                                                                           
#| Finally, compress the 'final' directory into 'final.tar.gz' and remove folder
#| 'final'.
#`----
final_papers = []
mkdir('final')

for a in accepted:
    for s in submissions:
        if s[0] == a[0] and s[1] == a[1]:
            final_papers.append(s)
            break
    for p in pdfs:
        if p[0] == a[0]:
            current_path = p[2]
            final_path = p[3]

            copy(current_path, final_path)
            break

myprocess = Popen(['tar', '-czf', 'final.tar.gz', 'final'])
myprocess.wait()
rmtree('final')

#,----
#| Write the db file.
#|                                                                         
#| Sort papers naturally by key 'first author's last name'.
#`----
final_papers = sorted(final_papers, key=lambda paper: paper[2][0][0])

with open('db', 'w') as db:
    for paper in final_papers:
        id = paper[0]
        title = texify(paper[1])
        authors = paper[2]
        
        db.write('P: ' + id + '\n')
        db.write('T: ' + title + '\n')
        for author in authors:
            lastname = texify(author[0])
            firstname = texify(author[1])
            
            db.write('A: ' + lastname + ', ' + firstname + '\n')

        for pdf in pdfs:
            if paper[0] == pdf[0]:
                path = pdf[3]
                length = str(pdf[1])
                
                db.write('F: ' + path + '\n')
                db.write('L: ' + length + '\n')
                break

        db.write('\n')
