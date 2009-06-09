#Bookletise.py
from __future__ import division # this makes 5/4 give 1.25 rather than 1
from pyPdf import PdfFileWriter, PdfFileReader

inputfile = file("sewtha.pdf", "rb")

inputdoc = PdfFileReader(inputfile)
blankpage = PdfFileReader(file("Blank.pdf", "rb"))
outputbooklet = PdfFileWriter()

num_doc_pages = inputdoc.getNumPages() # find number of pages in the inputdoc

num_paper_sheets_in_booklet = 0
paper_sheets_required = num_doc_pages / 4 # There are 4 pages to an A4 sheet

while num_paper_sheets_in_booklet < paper_sheets_required:
    num_paper_sheets_in_booklet += 1 # need to round up

total_num_pages_in_booklet = num_paper_sheets_in_booklet * 4
bookletsheets = range(num_paper_sheets_in_booklet)

# Create a list of pages in the order that they should be printed. Note that the index starts at 0, so the first page is page(0)
# The algorithm is as follows:
# If there is just one sheet of double-sided paper required (4 pages) then the order of printing is page 1, page 2, page 3, page 0
# If a second double-sided sheet of paper is required then the order of printing is [page 1, page 2], page 5, page 6, page 7, page 4, [page 3, page 0]
# If a third double-sided sheet of paper is required then the order of printing is [page 1, page 2], [page 5, page 6], page 9, page, 10, page 11, page 8, [page 7, page 4], [page 3, page 0]
# etc
# The number of pages in a booklet needs to be a multiple of 4, so extra blank pages are added if required.
orderlist = []

for sheet in bookletsheets:
    orderlist.append(1 + sheet*4)
    orderlist.append(2 + sheet*4)

bookletsheets.reverse()

for sheet in bookletsheets:
    orderlist.append(3 + sheet*4)
    orderlist.append(0 + sheet*4)

# ----------------------------------------------------------------------------------------------------------------------------------------------------
    
for page in range(total_num_pages_in_booklet): # look at each page in the booklet
    inputdocpage = orderlist.index(page) # find which page of the original document to print on current page of the booklet
    print 'Page %d of the booklet is page %d of the original document' % (page, inputdocpage)
    if inputdocpage < num_doc_pages:
        outputbooklet.addPage(inputdoc.getPage(inputdocpage))
    else:
        outputbooklet.addPage(blankpage.getPage(0)) # add a blank page if there are no pages left in the original document.


print 'Number of pages in original document = %d' % num_doc_pages
print 'The booklet is made up of %d double-sided sheets of paper' % num_paper_sheets_in_booklet
if total_num_pages_in_booklet > num_doc_pages:
    print 'Since the booklet has a multiple of 4 pages, %d extra blank pages have been added.' % (total_num_pages_in_booklet - num_doc_pages)
        
outputStream = file("document-output.pdf", "wb")
outputbooklet.write(outputStream)
outputStream.close()