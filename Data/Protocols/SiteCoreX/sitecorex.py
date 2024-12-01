from terminaltables import SingleTable
from Wappalyzer import Wappalyzer, WebPage

#sitename = input("url:")


def sitecorex(sitename):
    data = [['Software', 'Versions', 'Categories']]
    wappalyzer = Wappalyzer.latest()
    website = WebPage.new_from_url(sitename)
    results = wappalyzer.analyze_with_versions_and_categories(website)
    #sitedata = ("URL", sitename)
    #data.append(sitedata)
    for software, details in results.items():
        versions = ', '.join(details['versions'])
        categories = ', '.join(details['categories'])
        data.append([software, versions, categories])
        data.append(['', '', ''])

    if data[-1] == ['', '', '']:
        data.pop()

    table = SingleTable(data, sitename)
    print("\n" + table.table)
    #print(f"\n{results}")


#if __name__ == '__main__':
    #sitecorex(sitename)
