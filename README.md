# CED-Tesseract
This could have been very simple.  The only reason it was never truly implemented was due to the inconsistency of our printer - a 20 year old dot matrix.


Implemented in python, running on Cygwin.  Several times the python script outputs bash scripts to run via the cygwin shell, to feed things back into the python script, and just in general uses bash calls more than python calls for the same thing.

##The Process:
1.  Split all files in the Incoming directory into individual pages
2.  Convert all of those pages to 600ppi Jpegs.
3.  Take each image, determine if it's right-side-up, and crop out an area around the register number field, and apply a few filters to aid in OCR
4.  Build a bash script to OCR the cropped images, and output the results to a text file with the same name as the page that it came from.
5.  Determine if a valid six-digit string is in the OCR'd text.  
    1. If so, move the appropriate pdf page file into the Outgoing directory.  
    2. If there is already a file that shares a name with the page, we assume that this image is another page of the same invoice.
    3. If no valid string is found, move it to Outgoing/Unread and name it numerically
6. Clean up all of the considerable waste that is generated from running so many freakin scripts 
7.  Since this was meant to run as a sort of daemon,  loop back and wait for more files to arrive

This could probably be engineered to work for documents that AREN'T printed on a crappy dot matrix printer, as long as the form is consistent.
