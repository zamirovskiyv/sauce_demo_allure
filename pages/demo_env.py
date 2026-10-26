import os

print(os.getenv("USERNAME"))
print(os.getenv("CI"))
print(os.getenv("CI", "false"))

CI = True