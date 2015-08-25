import urllib2, re

# program to see if the COS undergrad lab TA/grader app is updated
source = urllib2.urlopen('http://tas.cs.princeton.edu/apply.php')
content = source.read()
check1 = re.search('reviewing the Spring 2015 grader applicants', content)
check2 = re.search('January 16', content)
if check1 and check2:
	print 'grader app has not been updated'
else:
	print 'grader app was updated, visit website now'
	deadline = re.search('deadline.{25}', content)
	if deadline:
		print deadline.group(0)