import argparse
import itertools
import math
import sys

from PIL import Image

def get_state(pixel, mode):
  """
  Determines whether a given pixel is considered "on" or "off".
  """
  off_threshold = 80
  on_threshold = 180

  if pixel >= on_threshold:
    return True
  elif pixel <= off_threshold:
    return False
  else:
    raise Exception('Unclear state of pixel ' + str(pixel))

def process_image(image_path, height, width):
  """
  Takes an image path and converts it into the k value that will produce that image.
  """
  im = Image.open(image_path).convert('L')
  pic = im.load()
  assert im.size == (width, height)
  bin_str = ''
  for x in xrange(width):
    for y in xrange(height - 1, -1, -1):
      bin_str += '1' if get_state(pic[x, y], im.mode) else '0'
  return long(bin_str, 2) * height

def evaluate_formula(x, y, height):
  """
  Evaluates Tupper's self-referential formula for given integers x and y.
  """
  c = height
  d = (-c * x) - (y % c)
  e = 1
  for _ in xrange(-d):
    e *= 2
  f = (y / c) / e
  g = f % 2
  return 0.5 < g

def process_value(k, height, width):
  """
  Given a k-value, create print out what the graph looks like between k and k + height
  """
  for y in itertools.count(k):
    if y >= k + height:
      break
    for x in xrange(width - 1, -1, -1):
      pixel = evaluate_formula(x, y, height)
      if pixel:
        print '*',
      else:
        print ' ',
    print

def main(argv=sys.argv):
  p = argparse.ArgumentParser()
  group = p.add_mutually_exclusive_group(required=True)
  group.add_argument('--image', help='Image file to extract the k-value from')
  group.add_argument('--value', help='k-value to plot')
  p.add_argument('--height', default=17, type=int, help='adjustable height of resulting image')
  cfg = p.parse_args(argv[1:])

  # TODO: figure out how width comes into play in the formula
  width = 106

  if cfg.image:
    k = process_image(cfg.image, cfg.height, width)
    print 'k = ' + str(k)
  elif cfg.value:
    k = long(cfg.value)
  result = process_value(k, cfg.height, width)

if __name__ == '__main__':
  main(sys.argv)
