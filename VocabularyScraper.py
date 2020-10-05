import time
import os
import selenium.webdriver.common.keys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
LOAD_DELAY = 2
email = input("Enter Email:\t")
password = input("Enter Password:\t")
chapter = "Chapter " + input("Book Chapter:\t")
driver = webdriver.Chrome(os.path.abspath("..\\Webdrivers\\chromedriver.exe"))
def signIn():
    driver.get("https://reg.macmillanhighered.com/Account/EmailCheck?nr=True&CourseID=14017971&targetUrl=https%3A%2F%2Fwww.macmillanhighered.com%2Flaunchpad%2Fdiscoveringpsych8e&cancelUrl=https%3A%2F%2Freg.macmillanhighered.com%2FAccount%2FUnauthenticated%3FTargetURL%3Dwww.macmillanhighered.com%2Flaunchpad%2Fdiscoveringpsych8e%2F14017971&baseUrl=www.macmillanhighered.com%2Flaunchpad%2Fdiscoveringpsych8e&siteId=0&EulaAgreement=False&mode=1&AllowNoSelection=False&Platform=PX&Location=0&LMSRequestData=%7B%22courseID%22%3A14017971%2C%22email%22%3Anull%2C%22firstname%22%3Anull%2C%22lastname%22%3Anull%2C%22lmsuserid%22%3A%22854baea37db6fdfc7d1ef2df1d10827a37f359e5%22%2C%22installationid%22%3A12117%2C%22institutionid%22%3A16791%2C%22customcanvasuserid%22%3A343214%2C%22baseURL%22%3A%22www.macmillanhighered.com%2Flaunchpad%2Fdiscoveringpsych8e%22%2C%22TransactionId%22%3A%22ROLE_sysin.lhKBGFAF%22%2C%22associationid%22%3A219594%7D")
    # Enter Email
    driver.find_element_by_id('EMail').send_keys(email)
    # Press Submit
    driver.find_element_by_id('btnRegisterStep1_GO').click()
    # Enter Password
    driver.find_element_by_id("Password").send_keys(password)
    # Press Submit
    driver.find_element_by_id('Bfw_MARS_login_GO').click()
    time.sleep(LOAD_DELAY)
    try:
        # Press Enter Course button
        driver.find_element_by_class_name('EnterCourse').click()
    except:
        pass

def getToBook():
    try:
        chapters = driver.find_elements_by_class_name('tocTitleLink')
        # find correct chapter:
        for ch in chapters:
            if chapter + "." in ch.get_attribute('innerHTML'):
                ch.click()
                break
        # Click on quiz page
        links = driver.find_elements_by_class_name('tocTitleLink')
        for link in links:
            if chapter + " Practice Quiz" in link.get_attribute('innerHTML'):
                link.click()
                break
        time.sleep(LOAD_DELAY)
        # Go to vocab page
        previousPage()
    except:
        signIn()
        getToBook()
    #driver.find_element_by_id('MODULE_bsi__D5591172__4DF8__4CF8__B70E__73C267E2FAAE').click()
    # try:
    #     # Go to chapter 5 quiz page
    #     driver.find_element_by_id('bsi__006A406A__C3E3__4364__91D5__D9AC8B529162_Copy636918188901874431').click()
    #     time.sleep(LOAD_DELAY)
    #     # Go to previous page
    #     previousPage()
    # except:
    #     getToBook()


# def goToPage(number:int):
#     number = str(number)
#     inputs = driver.find_elements_by_tag_name('input')
#     # Find correct input
#     for entry in inputs:
#         if entry.get_attribute('for') == 'pageNumberInput':
#             if(entry.get_attribute('value') != number):
#                 entry.send_keys(number)
#                 entry.send_keys(Keys.ENTER)
#             break
def previousPage():
    time.sleep(LOAD_DELAY)
    driver.find_element_by_class_name('back-label').click()
    time.sleep(LOAD_DELAY)
def nextPage():
    time.sleep(LOAD_DELAY)
    driver.find_element_by_class_name('next-label').click()
    time.sleep(LOAD_DELAY)
def handleLoadError():
    frames = driver.find_elements_by_tag_name('iframe')
    for frame in frames:
        driver.switch_to.frame(frame)
        while(len(driver.find_elements_by_id('main-frame-error')) > 0):
            driver.switch_to_default_content()
            nextPage()
            time.sleep(5)
            previousPage()
def writeToFile(definition:str):
    fileName = chapter + " Vocabulary.txt"
    f = open(fileName, "a+")
    if "<i" in definition:
        definition = definition[0:definition.index("<i")] + definition[definition.index("i>") + 1:]
    f.write(definition)
    f.close()

def copyDefinitions(words):
    for i in range(len(words)):
        try:
            signIn()
            getToBook()
            #handleLoadError(
            time.sleep(LOAD_DELAY)
            findDef(words[i], i) # Leave this breakpoint in to handle page load errors
            time.sleep(LOAD_DELAY)
            definition = copyDef(words[i])
            writeToFile(definition)
        except:
            driver.switch_to_default_content()
            signIn()
            getToBook()
            i = i - 1
            continue
    #/books/9781319243739/epub/OEBPS/xhtml/hoc_9781319136390_ch06_07.xhtml?create=true#cfi=/6/152%5Bhoc_9781319136390_ch06_07%5D!
def copyDef(word:str):
    # Click word and make tooltip appear
    try:
        driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    except:
        pass
    keywords = driver.find_elements_by_class_name('keyword')
    for keyword in keywords:
        if(str.lower(word).replace(' ', '') in str.lower(keyword.get_attribute('innerHTML').replace(' ', ''))):
            keyword.click()
            tooltip = driver.find_element_by_class_name('tooltipText').get_attribute('innerHTML')
            definition = word + ": " + str(tooltip) + "\n"
            driver.switch_to_default_content()
            return definition
    


def findDef(word:str, index:int):
    frames = driver.find_elements_by_tag_name('iframe')
    driver.switch_to.frame(frames[1])
    frames = driver.find_elements_by_tag_name('iframe')
    driver.get(frames[0].get_attribute('src'))
    driver.switch_to.frame(driver.find_element_by_id('epub-content'))
    links = driver.find_elements_by_class_name('crossref')
    if links[index].get_attribute('innerHTML') == word:
        links[index].click()        
    else:
        for link in links:
            if link.get_attribute('innerHTML') == word:
                link.click()
                break
   
        
if __name__ == "__main__":
    words = [' ', '']
    if(chapter == "Chatper 5"):
        words = ["memory", "encoding", "storage", "retrieval", "stage model of memory", "sensory memory", "short-term memory", "long-term memory", "maintenance rehearsal", "chunking", "working memory", "elaborative rehearsal", "procedural memory", "episodic memory", "semantic memory", "explicit memory", "implicit memory", "clustering", "semantic network model", "retrieval", "retrieval cue", "retrieval cue failure", "tip-of-the-tongue (TOT) experience", "recall", "cued recall", "recognition", "serial position effect", "encoding specificity principle", "context effect", "mood congruence", "flashbulb memory", "forgetting", "encoding failure", "prospective memory", "déjà vu experience", "source memory (source monitoring)", "decay theory", "interference theory", "retroactive interference", "proactive interference", "suppression", "repression", "misinformation effect", "schema", "source confusion", "false memory", "imagination inflation", "memory trace (engram)", "long-term potentiation", "amnesia", "retrograde amnesia", "memory consolidation", "anterograde amnesia", "dementia", "Alzheimer’s disease (AD)"]
    elif(chapter == "Chapter 6"):
        words = ["cognition", "thinking", "mental image", "concept", "prototype", "exemplars", "problem solving", "trial and error", "algorithm", "heuristic", "insight", "functional fixedness", "mental set", "availability heuristic", "representativeness heuristic", "language", "confirmation bias", "linguistic relativity hypothesis", "comprehension vocabulary", "production vocabulary", "bilingualism", "animal cognition (comparative cognition)", "intelligence", "mental age", "intelligence quotient (IQ)", "achievement test", "aptitude test", "standardization", "normal curve (normal distribution)", "reliability", "validity", "g factor (general intelligence)", "triarchic theory of intelligence", "intellectual disability", "intellectual giftedness", "heritability", "stereotype threat", "creativity"]
    copyDefinitions(words)
    
