# easy2acl.py

This short script is useful in the scenario where peer-reviewing is done using EasyChair but proceedings are to be produced with aclpub. The user must retrieve information from EasyChair before running the script.
 
easy2acl.py produces two files for use with aclpub; the `db` file, and an archive `final.tar.gz` containing a folder `final`, which in turn contains the PDF files of the accepted submissions. You should make yourself familiar with the db file, which you can read more about in the aclpub documentation.

Please report bugs and suggest improvements.

## Prerequisites

The Python 3 packages PyPDF2 and unicode_tex are needed and can be installed using pip. The tar command is also needed (and should be available at PATH).

## How to run 

Create the files `accepted` and `submissions` and the folder `pdf` as shown in [Getting data from EasyChair](#getting-data-from-easychair). Before running this script, your file structure should look like this: 

    |-- easy2acl.py 
    |-- submissions 
    |-- accepted 
    `-- pdf 
        |-- ..._submission_1.pdf 
        |-- ..._submission_2.pdf 
        `-- ...

Run the script:

    $ python3 easy2acl.py
 
When the script has finished, you will find the files `db` and `final.tar.gz` in the same folder.  Place these files in your `proceedings` folder as suggested by the aclpub documentation, and proceed as you usually would with aclpub.

## Additional information

It is your responsibility to make sure that the `db` file is correct. The author(s) of this script make no claims that this script works as intended. Below are some things to look out for regarding the data you get from EasyChair, and the assumptions made by the script.

* **Title of submission in EasyChair does not match title in the submitted PDF.** In case of a substantial change to the title, and depending on the policy of your conference, you might want to contact the Program Chair.  You might want to do so anyways in case the title is used anywhere else, for example in the conference program.
	
* **Order of authors of submission in EasyChair does not match the order in the submitted PDF.**

* **Order of author name internally, as in `<first> <last>`, in EasyChair is incorrect.** This can cause problems with the order of the papers since they are written to the `db` file in alphabetical order according to the first author's last name.

* **Author has multiple names before the last name, e.g. `<first> <middle> <last>`.** This can cause problems with the order of the papers since they are written in alphabetical order according to the first author's last name. The script assumes the format `<first> <last> [<last>] [<last>] ...`.
    
* **Some diacritics and special characters in names are not converted by the script.** Certain characters that you expected to be translated into LaTeX escape codes, but were not, might be because they are not handled in the unicode_tex package. Make sure that the name was properly written in EasyChair; it might be that the person who entered the name forgot to add diacritics. If you want to be nice, you can check the names in your resulting `db` file against the names of the actual submissions and make the appropriate changes to the `db` file.

## Getting data from EasyChair

Start by downloading the actual submissions: In EasyChair, go to the page _Submissions_ and click the link _Download submissions_ found in the upper right hand side. Extract the PDF files to a folder `pdf`. See [How to run](#how-to-run) for the file structure.

### Information about all submissions

On the same page _Submissions_: In the table, starting with the first submission entry (excluding the first row/header starting with `#`), select and copy the entire table. Copy and paste this into a proper text editor of your choice and save the file as `submissions`. Remember to not force any linebreaks. Each row in the table should correspond to one line in the resulting file. A sample `submissions` file is available [here](example-files/submissions).

We now have information about all the submissions but not whether they are accepted or not. Of course we do not want to include the rejected submissions. We need to get one more piece of information.

### A list of the accepted submissions

Go to _Status -> All papers_. Here we find the information on what submissions are accepted. Copy the content of this table as you did with the previous one. Save the content as `accepted`, and make sure that each row in the table corresponds to one line in the resulting file. A sample `accepted` file is available [here](example-files/accepted).

### A short explanation of the steps above

Neither of the two pages we saved data from alone contain all the information we need to create the `db` file – the _Submissions_ page does not say which ones are accepted, and the _Status page_ does not tell us the author names of the papers. By taking the intersection of the submission IDs of the two lists that we saved, we get the information we need about the accepted submissions.

Copying the table contents directly from the web browser results in a nice tab separated list when pasting into a text editor. This makes it easy to work with, and if the table format should change in EasyChair it is simple to adapt the script.
