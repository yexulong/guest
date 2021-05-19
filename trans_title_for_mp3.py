import os
import eyed3


def trans_title(path):
    files = os.listdir(path)
    for file in files:
        name, suffix = os.path.splitext(file)
        if suffix in ['.mp3']:
            music_file = eyed3.load(file)
            artist, title = map(str.strip, name.split('-'))
            music_file.tag.title = title
            music_file.tag.artist = artist
            
            music_file.save()

    
if __name__ == '__main__':
    trans_title('.')
