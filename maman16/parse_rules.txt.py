text =open('rules.txt').read().replace("\n","").replace("epsilon","").replace("'","\"")
''
rules= text.split("1")
for rule in rules:
  if  rule=="":
    continue
  arr  =rule.split("->")
  if len(arr)!=2:
    raise Exception(f"[{rule}]")
  name=arr[0].strip()
  bodies=arr[1].split("|")
  for body in bodies:
    print(f"""
  @_('{body.strip()}')
  def {name}(self, p):
    return []""")
