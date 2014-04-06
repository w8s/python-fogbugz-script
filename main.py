#!/usr/bin/python

from fogbugz import FogBugz
import fb_settings
import argparse

fb = FogBugz(fb_settings.URL, fb_settings.TOKEN)

def listProjectsByUser(arglist):
	user = arglist

	projects = fb.listProjects()

	xmlReturn = "<?xml version=\"1.0\"?>\n<items>\n"

	for project in projects.projects.childGenerator():
		projectName = project.sproject.string.encode('UTF-8')
	 	
		resp = fb.search(q='status:"Active" project:"' + projectName + '" assignedto:"' + user + '"', 
						  cols="ixBug")

		count = int(resp.cases["count"])

		if count > 0:
			
			xmlReturn += "    <item uid=\"project\" arg=\"%s\">\n" % (projectName)
			xmlReturn += "        <title>%s</title>\n" % (projectName)
			xmlReturn += "        <subtitle>View your %s active cases in %s...</subtitle>\n" % (count, projectName)
			xmlReturn += "    </item>\n"

	xmlReturn += "</items>"

	print str(xmlReturn)

def listAllActive(user):
	if user is None:
		user = fb_settings.USER

	resp = fb.search(q='assignedto:"' + user + '" status:"Active"',
					 cols="ixBug,sTitle,sStatus")

	xmlReturn = "<?xml version=\"1.0\"?>\n<items>\n"

	for case in resp.cases.childGenerator():
		xmlReturn += "    <item uid=\"case\" arg=\"%s\">\n" % (case.ixbug.string)
		xmlReturn += "        <title>%s: %s</title>\n" % (case.ixbug.string, case.stitle.string.encode('UTF-8'))
		xmlReturn += "        <subtitle>Start working on and open case %s in a browser...</subtitle>\n" % (case.ixbug.string)
		xmlReturn += "    </item>\n"

	xmlReturn += "</items>"

	print str(xmlReturn)

def listCasesForProject(arglist):
	project = arglist[0]
	if arglist[1] is None:
		user = fb_settings.USER
	else:
		user = arglist[1]

	resp = fb.search(q='status:"Active" project:"' + project + '" assignedto:"' + user + '"', 
						  cols="ixBug,sTitle,sStatus")

	xmlReturn = "<?xml version=\"1.0\"?>\n<items>\n"

	for case in resp.cases.childGenerator():
		xmlReturn += "    <item uid=\"case\" arg=\"%s\">\n" % (case.ixbug.string)
		xmlReturn += "        <title>%s: %s</title>\n" % (case.ixbug.string, case.stitle.string.encode('UTF-8'))
		xmlReturn += "        <subtitle>Start working on and open case %s in a browser...</subtitle>\n" % (case.ixbug.string)
		xmlReturn += "    </item>\n"

	xmlReturn += "</items>"

	print str(xmlReturn)

def workingOn(caseNum):
	try:
		fb.startWork(ixBug=caseNum)

		print "Working on case: %s." % (caseNum)

	except Exception as e:
		print "Oops! %s" % e.message.encode('UTF-8')

def stopWork():
	fb.stopWork()
	print "Stopped Fogbugz Timer"

def estimateOnCase(arglist):
	estimate = arglist[1]
	caseNum = arglist[0]

	fb.edit(ixBug=caseNum, hrsCurrEst=estimate)

	print 'Set estimate on case %s to %s hrs' % (caseNum, estimate)

def timeSpentOnCase(arglist):
	time = arglist[1]
	caseNum = arglist[0]

	fb.edit(ixBug=caseNum, hrsElapsedExtra=time)

	print 'Spent %s non-timesheet hour(s) on case %s' % (time, caseNum)

def addComment(arglist):
	comment = arglist[1]
	caseNum = arglist[0]

	fb.edit(ixBug=caseNum, sEvent=comment)

	print 'Added comment: "%s" to case %s' % (comment, caseNum)

def resolveCase(arglist):
	caseNum = arglist

	fb.resolve(ixBug=caseNum)

	print "Case %s: Resovled. Huzzah!" % (caseNum)

def main():
	parser = argparse.ArgumentParser(description='Interact with FogBugz.')

	parser.add_argument('-s', '--stop', action="store_true", help='Stop working on a case.')
	parser.add_argument('-w', '--working', type=int, help='Start working on case [n]')
	parser.add_argument('-l', '--list', metavar='USER', help='List all active cases by USER.')
	parser.add_argument('-e', '--estimate', nargs=2, metavar='N', help='Set ESTIMATE on a CASE NUMBER.')
	parser.add_argument('-t', '--time', nargs=2, metavar='N', help='Set TIME on CASE NUMBER. !!WARNING!! Overwrites value, does not add!')
	parser.add_argument('-c', '--comment', nargs=2, help='Add a COMMENT on CASE NUMBER.')
	parser.add_argument('-p', '--project', metavar='USER', help='List all projects where USER has active cases.')
	parser.add_argument('-n', '--projectCases', nargs=2, help='List all cases in a PROJECT for a USER.')
	parser.add_argument('-r', '--resolve', metavar='CASE NUMBER', help='Resolve specified case.')

	args = parser.parse_args()

	if args.stop:
		stopWork()

	if args.working:
		workingOn(args.working)

	if args.list:
		listAllActive(args.list)

	if args.estimate:
		estimateOnCase(args.estimate)

	if args.time:
		timeSpentOnCase(args.time)

	if args.comment:
	 	addComment(args.comment)

	if args.project:
		listProjectsByUser(args.project)

	if args.resolve:
		resolveCase(args.resolve)

	if args.projectCases:
		listCasesForProject(args.projectCases)

main()