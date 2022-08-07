import sys
import platform
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from tkinter import Tk
from itertools import permutations

from fileOperations import FileOperations
from twitterOperations import TwitterOperations
from charProp import CharProp

global configData
alphabetDict = {}
absentChars = []
presentChars = []
possibleChars = [x for x in 'EARIOTNSLCUDPMHGBFYWKVXZJQ']
buildWord = ['0', '0', '0', '0', '0']


def initConfigFile():
    global configData
    configFilePath = FileOperations.parseFileName('configs', 'config.json')
    args = sys.argv
    if len(args) > 1:
        configFilePath = FileOperations.parseFileName(args[1], args[2])
    configData = FileOperations.initJsonFile(configFilePath)
    global website

    website = configData["website"]


def initDriver(website):

    if platform.system() == 'Linux':
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800, 800))
        display.start()
        print("Display Started!")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get(website)
        time.sleep(2)
        driver.maximize_window()
        time.sleep(2)
    except:
        print("No website found")
    return driver


def initValues():
    global nonListedWords
    global storedWords
    global wordledWords
    global permutatedWords
    global savedWords

    global configData

    global storedWordsFile
    global wordledWordsFile
    global nonListedWordsFile
    global permutatedWordsFile
    global nonChanceWords

    csvFilesLocation = configData["csvFilesLocation"]
    permutatedWordsFile = FileOperations.parseFileName(
        csvFilesLocation, configData["permutatedWordsFile"])
    nonListedWordsFile = FileOperations.parseFileName(
        csvFilesLocation, configData["nonListedWordsFile"])
    storedWordsFile = FileOperations.parseFileName(
        csvFilesLocation, configData["storedWordsFile"])
    wordledWordsFile = FileOperations.parseFileName(
        csvFilesLocation, configData["wordledWordsFile"])

    permutatedWords = FileOperations.readCsvFile(permutatedWordsFile)
    nonListedWords = FileOperations.readCsvFile(nonListedWordsFile)
    storedWords = FileOperations.readCsvFile(storedWordsFile)
    wordledWords = FileOperations.readCsvFile(wordledWordsFile)

    nonChanceWords = nonListedWords+wordledWords

    savedWords = storedWords + permutatedWords
    for word in nonChanceWords:
        if word in savedWords:
            savedWords.remove(word)


def closePopUp(driver):
    initialPopUpClosureClass = configData["initialPopUpClosureClass"]
    try:
        closePopUpBox = driver.find_element(
            By.CLASS_NAME, initialPopUpClosureClass)
        if closePopUpBox is not None:
            closePopUpBox.click()
    except:
        print("Element Not found")
    time.sleep(2)


def findWord():
    global driver
    rows = driver.find_elements(By.CLASS_NAME, configData["wordleRowClass"])
    rowCount = 0
    for row in rows:
        isFilled, word, resultFound, correctWord = fillRow(row, rowCount)

        while isFilled is False and word != None:
            isFilled, word, resultFound, correctWord = fillRow(row, rowCount)
        if isFilled and not resultFound:
            checkPresentChars(word)

        if resultFound:
            twitterEnabled = configData["twitterEnabled"]
            if twitterEnabled == "Y":
                shareInTwitter()
            driver.close()
            if word not in storedWords:
                FileOperations.writeWordToCsv(storedWordsFile, word)
            if word not in wordledWords:
                if correctWord:
                    FileOperations.writeWordToCsv(wordledWordsFile, word)
            break

        rowCount += 1


def fillRow(row, rowCount):
    resultFound = False
    correctWord = False
    word, isOptWord = fetchWord()
    if word is None or isOptWord is False:
        word, isFilled, resultFound, correctWord = formWord(row, rowCount)
    else:
        isFilled, resultFound, correctWord = enterWord(word, row, rowCount)

    return isFilled, word, resultFound, correctWord


def shareInTwitter():
    tweet = Tk().clipboard_get()
    consumer_key = configData["consumerKey"]
    consumer_secret = configData["consumerSecretKey"]
    access_token = configData["accessToken"]
    access_token_secret = configData["accessSecretToken"]

    twitterOperations = TwitterOperations(
        consumer_key, consumer_secret, access_token, access_token_secret)
    twitterOperations.postTweet(tweet)


def checkPresentChars(enteredWord):
    global presentChars
    global tiles
    presentChars = []
    i = 0
    for ch in enteredWord:
        global savedWords
        btnElement = driver.find_element(
            By.XPATH, '//button[@data-key="'+ch.lower()+'"]')
        dataState = btnElement.get_attribute('data-state')
        if alphabetDict == {}:
            alphabetDict[ch] = CharProp(ch, dataState, None, None, btnElement)
        else:
            if ch not in alphabetDict.keys():
                alphabetDict[ch] = CharProp(
                    ch, dataState, None, None, btnElement)

        if dataState == 'absent':
            absentChars.append(ch)
            if ch in possibleChars:
                possibleChars.remove(ch)
            savedWords = [wrd for wrd in savedWords if ch not in wrd]
        else:
            tile = tiles[i]
            tileDataState = tile.get_attribute('data-state')

            if tileDataState == 'correct':
                wrdLst = []
                buildWord[i] = ch
                for wrd in savedWords:
                    if ch in wrd:
                        if wrd[i] == ch:
                           wrdLst.append(wrd)
                savedWords = wrdLst
                if alphabetDict[ch]:
                    if alphabetDict[ch].slot_chances:
                        if i not in alphabetDict[ch].slot_chances:
                            alphabetDict[ch].setSlotChance(i)
                            alphabetDict[ch].setDataState(tileDataState)
                    else:
                        alphabetDict[ch].setSlotChance(i)
                        alphabetDict[ch].setDataState(tileDataState)
            else:
                alphabetDict[ch].setNonSlotChance(i)
                wrdLst = []
                for wrd in savedWords:
                    if ch in wrd:
                        if not wrd[i] == ch:
                           wrdLst.append(wrd)
                savedWords = wrdLst
                if tileDataState == 'present':
                    presentChars.append(ch)

        i += 1


def fetchWord():
    global savedWords
    word = None
    isOptWord = False
    word, isOptWord = fetchWordFromList(savedWords)
    return word, isOptWord


def formWord(row, rowCount):
    isFilled = False
    resultFound = False
    correctWord = False
    tempWord = buildWord.copy()
    for ch in presentChars:
        alphabet = alphabetDict[ch]
        non_slot_chances = alphabet.non_chances_slots
        idx = 0
        for c in buildWord:
            if c == '0' and idx not in non_slot_chances:
                tempWord[idx] = ch
                break
            idx += 1

    correctChars = [i for i in tempWord if i != '0']
    mergedList = possibleChars+correctChars+presentChars
    if len(mergedList) <= 16:
        mergedList = mergedList+mergedList
    permutationLength = 5 - len(correctChars)
    while not isFilled:
        word, isFilled, resultFound, correctWord = permuteAndEnterWord(
            row, tempWord, mergedList, permutationLength, rowCount)
        if not isFilled:
            tempWord = buildWord.copy()
            mergedList += mergedList
            correctChars = [i for i in tempWord if i != '0']
            permutationLength = 5 - len(correctChars)

    return word, isFilled, resultFound, correctWord


def enterWord(word, row, rowCount):
    correctWord = True
    isFilled = False
    resultFound = False
    for alphabet in word:
        if not alphabetDict == {} and alphabet in alphabetDict.keys():
            alphabetDict[alphabet].webElement.click()
        else:
            key_path = '//button[@class="Key-module_key__Rv-Vp" and @data-key="' + \
                alphabet.lower()+'"]'
            driver.find_element(By.XPATH, key_path).click()

    driver.find_element(
        By.XPATH, '//button[@class="Key-module_key__Rv-Vp Key-module_oneAndAHalf__K6JBY" and @data-key="↵"]').click()
    time.sleep(10)

    print(f"Entered Word {word}")

    #Modal-module_closeIcon__b4z74
    global tiles
    if checkElementExist('Modal-module_content__s8qUZ'):
        isFilled = True
        rsltCopyBtn = driver.find_element(
            By.CLASS_NAME, 'AuthCTA-module_shareButton__SsNA6')
        rsltCopyBtn.click()
        resultFound = True
        if rowCount == 5:

            closeBtn = driver.find_element(
                By.CLASS_NAME, 'Modal-module_closeIcon__b4z74')
            closeBtn.click()
            tiles = row.find_elements(By.CLASS_NAME, 'Tile-module_tile__3ayIZ')
            for i in range(0, 5):
                dataState = tiles[i].get_attribute('data-state')
                if dataState != 'correct':
                    correctWord = False
                    break

        print("Stastics Element Exists")
    else:
        tiles = row.find_elements(By.CLASS_NAME, 'Tile-module_tile__3ayIZ')
        dataState = tiles[1].get_attribute('data-state')
        if dataState == 'tbd':
            FileOperations.writeWordToCsv(nonListedWordsFile, word)
            hitBackSpace(5)
            nonChanceWords.append(word)
        else:
            if word not in storedWords:
                FileOperations.writeWordToCsv(storedWordsFile, word)

            isFilled = True
            nonChanceWords.append(word)

    return isFilled, resultFound, correctWord


def fetchWordFromList(listedWord):
    word = None
    isOptWord = False
    for word in listedWord:
        isOptWord = checkOptWord(word)
        if isOptWord:
            break
    return word, isOptWord


def permuteAndEnterWord(row, tempWord, mergedList, permutationLength, rowCount):
    isFilled = False
    resultFound = False
    for y in list(permutations(mergedList, permutationLength)):
        newWord = tempWord.copy()
        for c in y:
            for idx in range(5):
                if newWord[idx] == '0':
                    newWord[idx] = c
                    break

        word = "".join(newWord)
        if len(word) == 5:
            if word not in permutatedWords:
                isOptWord = checkOptWord(word)
                if isOptWord:
                    isFilled, resultFound, correctWord = enterWord(
                        word, row, rowCount)
                if isFilled:
                    break
                print(word)
                permutatedWords.append(word)
                FileOperations.writeWordToCsv(permutatedWordsFile, word)
    return word, isFilled, resultFound, correctWord


def checkElementExist(className):
    try:
        driver.find_element(By.CLASS_NAME, className)
    except NoSuchElementException:
        return False
    return True


def hitBackSpace(times):
    for i in range(0, times):
        driver.find_element(
            By.XPATH, '//button[@class="Key-module_key__Rv-Vp Key-module_oneAndAHalf__K6JBY" and @data-key="←"]').click()
    time.sleep(1)


def checkOptWord(word):
    isWord = aChancefulWord(word)
    isCharsAbsent = isAbsentCharsInWord(word)
    isCharsPresent = isPresentCharsInWord(word)
    isNotInNonSlots = isCharNotInNonSlots(word)
    isInSlots = isCharsInSlots(word)
    if isWord and isCharsAbsent and isCharsPresent and isNotInNonSlots and isInSlots:
        return True

    return False


def aChancefulWord(word):
    if nonChanceWords:
        if word in nonChanceWords:
            return False
    return True


def isAbsentCharsInWord(word):
    if absentChars:
        for char in absentChars:
            if char in word:
                return False
    return True


def isPresentCharsInWord(word):
    isPresentCharsinWord = True
    if presentChars:
        i = 0
        for ch in presentChars:
            if not ch in word:
                isPresentCharsinWord = False
                break
            if not alphabetDict == {}:
                alphabet = alphabetDict[ch]
                for chance in alphabet.non_chances_slots:
                    wordIndices = [
                        i for i, ltr in enumerate(word) if ltr == ch]
                    if chance in wordIndices:
                        isPresentCharsinWord = False
                        break
                if alphabet.dataState == 'correct':
                    if buildWord[i] != ch or word[i] != ch:
                        isPresentCharsinWord = False

                    # for chance in alphabet.slot_chances:
                    #     if word[chance] != ch:
                    #         isPresentCharsinWord = False

            i += 1
    return isPresentCharsinWord


def isCharNotInNonSlots(word):
    idx = 0
    for ch in word:
        if not alphabetDict == {}:
            if ch in alphabetDict.keys():
                alphabet = alphabetDict[ch]
                non_chances_slot = alphabet.non_chances_slots
                if non_chances_slot:
                    if word[idx] == ch and idx in non_chances_slot:
                        return False
        idx += 1
    return True


def isCharsInSlots(word):
    idx = 0
    correctChars = [ch for ch in buildWord if ch != '0']
    if correctChars != []:
        for ch in buildWord:
            if ch != '0':
                if word[idx] != buildWord[idx]:
                    return False
            idx += 1
    return True


def main():
    global driver
    initConfigFile()
    driver = initDriver(website)
    initValues()
    closePopUp(driver)
    findWord()
    time.sleep(5)


if __name__ == "__main__":
    main()
