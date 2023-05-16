#writing a strict to a file?
# Writing to a file in Python
# This was tested on Python 2.7.

# path - is a string to desired path location. The file does
#         not have to exist.
# content - is a string with the file content.
def writeToFile(path, content):
  file = open(path, "w")
  for i in range(500000):
    file.write(f"{i} ")
  file.close()
  
  
PATH_TO_MY_FILE = 'temp.txt'
CONTENT_FOR_MY_FILE = 'Once upon a time in a small village nestled in the heart of a dense forest there lived a young girl named Maya She was known throughout the village for her beauty her intelligence and her kind heart Maya spent her days tending to the animals on her familys farm reading books and exploring the woods One day while wandering through the forest Maya stumbled upon a hidden clearing In the center of the clearing stood a magnificent tree its trunk as wide as a house and its branches stretching up to the sky Maya approached the tree marveling at its size and beauty As she reached out to touch one of the branches she heard a voice Greetings Maya the voice said I am the guardian of this forest What brings you here Startled Maya looked around trying to locate the source of the voice Who are you she asked I am the spirit of the forest the voice replied And you Maya have been chosen to undertake a great quest Will you accept Maya was hesitant She had never been one for adventure or danger But something about the tree and the voice called out to her stirring a sense of curiosity and excitement within her What kind of quest she asked You must travel to the other side of the forest to a place known as the Dark Mountains the voice explained There you will find a rare flower that can cure any illness or ailment Bring it back to me and I will grant you a great reward Maya considered the offer The idea of traveling to a faroff land and facing unknown dangers was daunting but the promise of a great reward was tempting She made up her mind I accept the quest she said But how will I know where to find the flower The forest will guide you the voice replied Trust in your instincts and you will find your way With that the voice faded away and Maya was left standing alone in the clearing She looked up at the tree feeling a sense of reverence and awe Then she set out on her journey For days Maya traveled through the forest following the guidance of the trees and the animals She encountered all manner of creatures from playful squirrels to fearsome wolves She slept under the stars and foraged for food in the wild Finally after many days of travel Maya arrived at the foot of the Dark Mountains The mountains were shrouded in mist and shadow and Maya could feel a sense of foreboding creeping over her She climbed the steep slopes of the mountains her heart pounding with fear and anticipation She had no idea what lay ahead but she was determined to find the flower and complete her quest As she climbed higher the air grew colder and the wind began to howl Maya pulled her cloak tighter around her and pressed on At last she reached the summit of the mountains There nestled in a small crevice between two boulders she found the flower It was a delicate blossom with petals as white as snow and a sweet fragrance that filled the air Maya carefully plucked the flower from its stem and cradled it in her hands She felt a surge of triumph and relief She had completed her quest But as she turned to make her way back down the mountains she heard a sound A low rumbling growl like that of a hungry beast She spun around her heart racing What she saw made her blood run cold Standing before her was a fearsome dragon its scales gleaming in the moonlight Its eyes glowed with a fierce red light and smoke poured from its'

writeToFile(PATH_TO_MY_FILE, CONTENT_FOR_MY_FILE)

# Run in terminal using:
# python write-to-file.py
#
# It will create a file called `example.txt` and the contents will look like (minus the number signs):
# Example
# This is on line 2 of a text file.
# 
# The end.