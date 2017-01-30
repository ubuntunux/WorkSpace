import os
for dirname, dirnames, filenames in os.walk('.'):
  for filename in filenames:
    if os.path.splitext(filename)[1].lower() == '.py':
      f = open(filename, 'r')
      lines = list(f)
      f.close()
      f = open(filename, 'w')
      for line in lines:
        f.writelines(line.replace("\t", "  "))
      f.close()