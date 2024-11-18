import random
import string

def generate_pin_token():
  part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
  part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
  return f"{part1}-{part2}"