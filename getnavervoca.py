# 영어 단어의 뜻을 Naver에서 갖고오기
import sys
import urllib.request
import re

def DealArguments():
	if len(sys.argv) > 1:
		return sys.argv[1]
	else:
		print("please enter your voca file")
		return

def openFile(filename):
	try:
		file = open(filename,"r")
		# save voca to list
		vocalist = file.readlines()

		# delete cr/lf
		for i in range(len(vocalist)):
			vocalist[i]=vocalist[i].replace('\n','')

		# numer of vocalist
		# print("Total voca : %d" % len(vocalist))

		# print vocalist
		# for i in range(len(vocalist)):
			# print(vocalist[i])

        file.close()
        
		return vocalist

	except IOError:
		print("Error : %s open error" % filename)
		return

def removeHTMLTag(str):
    # remove comment
    str1 = re.sub("<!--.*?-->","",str)

    # remove tag
    str2 = re.sub("<.*?>","",str1)

    # print for debug
    # print(str2)

    return str2
    
def findUrlData(voca):
    url = 'http://endic.naver.com/search.nhn?sLn=kr&searchOption=all&query=%s' % voca
    u = urllib.request.urlopen(url)
    data = u.read()
    data = data.decode("utf-8")
    # print(data)

    return data

def findEnglish(data):
    EstartPos = data.find("<span class=\"fnt_e07\">")

    # print("in findenglish method: %s " % EstartPos)
    # error check
    if(EstartPos<0):
        return ""

    # print(EstartPos) 

    EendPos = EstartPos + data[EstartPos:EstartPos+2000].find("</span>")
    # print(EendPos)
    englishExample = data[EstartPos+22:EendPos]

    englishExample = removeHTMLTag(englishExample)

    if not englishExample.endswith('.'):
        englishExample += "."

    return englishExample

def findKorean(data):
    # getting korean example
    # get start Position
    HstartPos = data.find("<span class=\"fnt_k10\">")

    # print("in findKorea method : %s" % HstartPos)
    # error check
    if(HstartPos<0):
        return ""

    # get end Position
    HendPos = HstartPos + data[HstartPos:HstartPos+500].find('</span>')

    # return example
    koreanExample = data[HstartPos:HendPos]

    koreanExample = removeHTMLTag(koreanExample)

    if not koreanExample.endswith('.'):
        koreanExample += "."

    return koreanExample


def findMeaning(data):
    # getting korean example
    # get start Position
    MstartPos = data.find("<span class=\"fnt_k05\">") + 22
    # print("korean example : %s" % MstartPos)
    # error check
    if(MstartPos<0):
        return ""

    # print(data[MstartPos:MstartPos+200])
    # get end Position
    
    MendPos = MstartPos + data[MstartPos:MstartPos+200].find('</span>')
    # return example
    koreanMeaning = data[MstartPos:MendPos]
    # print("meanging")
    # print(koreanMeaning)

    koreanMeaning = removeHTMLTag(koreanMeaning)
    return koreanMeaning


def Main():
	filename = DealArguments()

	if not filename == None:
		vocaList = openFile(filename)

		for k in range(len(vocaList)):
	        # vocaList[k] = vocaList[k].replace('\n','')
			geturldata = findUrlData(vocaList[k])
	        
			englishExample = findEnglish(geturldata)
	        # print(englishExample)
			koreanExample = findKorean(geturldata)
	        # print(koreanExample)
	        # korean example meaning
			koreanMeaning = findMeaning(geturldata)
	        # print(koreanMeaning)

	        # print(koreanMeaning)
	        # setting the print format
			# print("[%d/%d] ==> %s\t%s\t%s\t%s" % (k, len(vocaList), vocaList[k], koreanMeaning,englishExample, koreanExample))

			print("%s\t%s\t%s\t%s" % (vocaList[k], koreanMeaning,englishExample, koreanExample))


##### start position
if __name__ == "__main__":
	Main()
