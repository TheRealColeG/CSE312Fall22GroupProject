#Return a html string containing the html of the game that will be sent over websockets
def htmlcreator(properties):

    ret_val = ""
    html = open("cole-code/monopoly.html", 'r')
    for line in html:
        ret_val = ret_val + str(line)
    html.close

    copy = ret_val
    print(copy)

    for i in range(len(ret_val)):
        if ret_val[i] == '[' and ret_val[i+1] == '[':
            index = None
            j = i+2
            if ret_val[index+1] == ']':
                index = int(ret_val[j])
            else:
                index = int(ret_val[j]+ret_val[j+1])
            string = "[["+str(index)+"]]"
            #(property["name"], property["baseCost"], property["currentOwner"])
            property = properties[index]
            if property["name"] == -1:
                copy = copy.replace(string, "")
            elif property["currentOwner"] == -1:
                copy = copy.replace(string, property["name"])
            else:
                copy = copy.replace(string, str(property["name"]+'\n'+property["baseCost"]+'\n'+property["currentOwner"]))

    return copy

htmlcreator(0)