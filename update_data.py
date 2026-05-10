import os
import sys
import json
import codecs
import time

dataDir = "src/data/"
bibFile = "bib/references.bib"
generatedDir = dataDir + "generated/"
bibJsFile = generatedDir + "bib.js"
papersDir = dataDir + "papers_pdf/"
papersImgDir = dataDir + "papers_img/"
availablePdfFile = generatedDir + "available_pdf.js"
availableImgFile = generatedDir + "available_img.js"


def parseBibtex(bibFile):
    parsedData = {}
    lastField = ""
    with codecs.open(bibFile, "r", "utf-8-sig") as fIn:
        currentId = ""
        for line in fIn:
            line = line.strip("\n").strip("\r")
            if line.startswith("@"):
                currentId = line.split("{")[1].rstrip(",\n")
                currentType = line.split("{")[0].strip("@ ")
                parsedData[currentId] = {"type": currentType}
            if currentId != "":
                if "=" in line:
                    field = line.split("=")[0].strip().lower()
                    value = line.split("=")[1].strip("} \n").replace("},", "").strip()
                    if len(value) > 0 and value[0] == "{":
                        value = value[1:]
                    if field in parsedData[currentId]:
                        parsedData[currentId][field] = parsedData[currentId][field] + " " + value
                    else:
                        parsedData[currentId][field] = value
                    lastField = field
                else:
                    if lastField in parsedData[currentId]:
                        value = line.strip()
                        value = value.strip("} \n").replace("},", "").strip()
                        if len(value) > 0:
                            parsedData[currentId][lastField] = parsedData[currentId][lastField] + " " + value
    return parsedData


def writeJSON(parsedData):
    os.makedirs(os.path.dirname(bibJsFile), exist_ok=True)
    with codecs.open(bibJsFile, "w", "utf-8-sig") as fOut:
        fOut.write("define({ entries : ")
        fOut.write(json.dumps(parsedData, sort_keys=True, indent=4, separators=(",", ": ")))
        fOut.write("});")


def listAvailablePdf():
    os.makedirs(papersDir, exist_ok=True)
    fOut = open(availablePdfFile, "w", encoding="utf-8")
    s = "define({availablePdf: ["
    count = 0
    for file in os.listdir(papersDir):
        if file.endswith(".pdf"):
            s += "\"" + file.replace(".pdf", "") + "\","
            count += 1
    if count > 0:
        s = s[: len(s) - 1]
    s += "]});"
    fOut.write(s)
    fOut.close()


def listAvailableImg():
    os.makedirs(papersImgDir, exist_ok=True)
    fOut = open(availableImgFile, "w", encoding="utf-8")
    s = "define({ availableImg: ["
    count = 0
    for file in os.listdir(papersImgDir):
        if file.endswith(".png"):
            s += "\"" + file.replace(".png", "") + "\","
            count += 1
    if count > 0:
        s = s[: len(s) - 1]
    s += "]});"
    fOut.write(s)
    fOut.close()


def update():
    print("convert bib file")
    writeJSON(parseBibtex(bibFile))
    print("list available paper PDF files")
    listAvailablePdf()
    print("list available paper images")
    listAvailableImg()
    print("done")


def watch_loop():
    prevBibTime = 0
    while True:
        currentBibTime = os.stat(bibFile).st_mtime
        if prevBibTime != currentBibTime:
            print("detected change in bib file")
            update()
            prevBibTime = currentBibTime
        else:
            print("waiting for changes in bib file: " + bibFile)
        time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        watch_loop()
    else:
        update()
