thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "year": 2020
}
k = thisdict
k["model"] = "V"
thisdict = k
print(thisdict)
