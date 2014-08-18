__author__ = 'toddwaits'

from fogbugz import FogBugz
import fb_settings
import argparse
import os

fb = FogBugz(fb_settings.URL, fb_settings.TOKEN)


def write_srs(markdown, project):

    # Grab the current working dir
    curdir = os.getcwd()

    filepath = os.path.join(curdir + "/%s-reqs.md" % project)

    print "Writing File: " + filepath

    srs_file = open(filepath, "w")
    srs_file.write(markdown)
    srs_file.close()


def get_requirements_cases(project_name):

    print "Requesting Data"

    resp = fb.search(q='category:"Requirement" orderby:"ixBug" project:"' + project_name + '"', cols="sTitle,sArea,ixBug,latestEvent,sFixFor,sStatus")

    return resp


def translate_xml_to_markdown(fb_xml, project_name):

    output = "# Requirements for " + project_name + "\n\n"

    print "Translating XML to Markdown"

    for case in fb_xml.cases.childGenerator():
        output += "## %s\n\nID: [%s](%s/default.asp?%s)\n\n" % (case.stitle.string.encode('UTF-8'), case.ixbug.string.encode('UTF-8'), fb_settings.URL, case.ixbug.string.encode('UTF-8'))

        output += "**Status:** %s\n\n" % (case.sstatus.string.encode('UTF-8'))

        ## Get Text from Event
        if (not case.events) or (len(case.events) != 0) :
            for event in case.events.childGenerator():
                if (not event.s) or (len(event.s) != 0) :
                    # print event.s
                    output += "%s\n\n" % (event.s.string.encode('UTF-8'))

        output += "**Area:** %s\n\n" % (case.sarea.string.encode('UTF-8'))

    return output


def main():

    # Set up script arguments

    parser = argparse.ArgumentParser(description='Create SRS from cases marked as "Requirement" in FogBugz.')
    parser.add_argument('-p', '--project', help='Grab all requirement cases from a given PROJECT.')
    
    args = parser.parse_args()
    
    print args

    if args.project:
        project = args.project

        if project:
            print project

            response = get_requirements_cases(project)

            output = translate_xml_to_markdown(response, project)

            write_srs(output, project)

        else:
            print "No Project specified."


main()