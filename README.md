# Read Me
## _Usage_ - The least imaginative COUNTER reporting and SUSHI client tool name, ever

_(26Mar2021)_

For years, librarians have wanted tools to extract usage information from our electronic database, journal, and ebook providers. The [COUNTER Project](https://counterproject.org/) lays out a standard set of reports and and report formats for vendors to provide to librarians, in the hope of standardizing how the information librarians want can be extracted from our vendors.

The [National Information Standards Organization](https://niso.org) has created a protocol called SUSHI to make automated collection of the COUNTER reports possible.

The _Usage_ tool uses SUSHI to gather specified COUNTER reports together for any number of vendors. It also accepts individual COUNTER report files as input.

## Technology stack

* Anaconda Python
* Python version 3.8
* PyQt6, a python library for using Qt6 for the user interface
* PeeWee ORM for data storage
* pyCOUNTER for SUSHI and COUNTER handling