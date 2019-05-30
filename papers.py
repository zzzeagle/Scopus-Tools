import csv, requests, json

#Your Scopus API key
apiKey = ""

#Open list of Scopus Author IDs. Use a CSV UTF-8 file with no header
csvReader = csv.reader(open('ids.csv', 'r', encoding="utf-8"), delimiter=' ', skipinitialspace=True)
authors = []
for row in csvReader:
	row = "".join(row)
	authors.append(row)

#Open a CSV file to write results to
paper_data = open('papers.csv', 'w', newline='', encoding="utf-8")
csvwriter = csv.writer(paper_data)

for author in authors:
	print(author)
	#Author Data API URL
	authorUrl = "https://api.elsevier.com/content/search/author?query=AU-ID("+author+")&apiKey="+apiKey+"&xml-decode=true&httpAccept=application%2Fjson"
	authorDetails = requests.get(authorUrl).json()
	
	#Get Author Name
	authorSurname = authorDetails['search-results']['entry'][0]['preferred-name']['surname']
	authorGivenName = authorDetails['search-results']['entry'][0]['preferred-name']['given-name']
	
	#Authors papers API URL
	papersUrl = "https://api.elsevier.com/content/search/scopus?query=AU-ID("+author+")&sort=-coverDate&apiKey="+apiKey+"&xml-decode=true&httpAccept=application%2Fjson&view=Complete&count=20"
	authorPapers = requests.get(papersUrl).json()

	entries = authorPapers['search-results']['entry']

	#For each paper in the search results add the requested field to a list. Output list to CSV file.
	for entry in entries:
		paper = []
		paper.append(authorSurname)
		paper.append(authorGivenName)
		paper.append(entry.get('eid'))
		paper.append(entry.get('prism:publicationName'))
		paper.append(entry.get('dc:title'))
		paper.append(entry.get('prism:coverDate'))
		paper.append(entry.get('prism:pageRange'))
		
		#Author stores a lot of extraneous data. Loop to get just the names.
		authors = entry.get('author')
		authorList = []
		for aut in authors:
			authorList.append(aut.get('authname'))
		paper.append(authorList)
		
		#Write results
		csvwriter.writerow(paper)

paper_data.close()
