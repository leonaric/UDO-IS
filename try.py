with open("active.db", "r") as r:
    reeed = r.read()
    reeed = reeed.replace("\nimport", " ")
    reeed = reeed.replace("\nfrom", " ")
    reeed = reeed.replace("import", "")

with open("active.db", "w") as w:
    w.write(reeed)