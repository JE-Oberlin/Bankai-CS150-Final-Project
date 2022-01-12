class ScriptParser:
  def __init__(self, fn: str):
    f = open(fn)
    self.masterScript = []
    self.position = -1
    for line in f:
      print(line)
      if line[0] == "#" or line[0] == "\n":
        pass
      else:
        l = line.strip("\n")
        l = l.split("|")
        print(l)
        self.masterScript.append(l)

    print(self.masterScript)

    f.close()

  def next(self):
    self.position += 1

  def currentLine(self):
    return self.masterScript[self.position]
