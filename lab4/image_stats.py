#!/usr/bin/env python
import os
import argparse

import PIL.Image
import PIL.ExifTags


def get_image_paths(path):
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                yield os.path.join(dirpath, filename)
    else:
        yield path


def get_image_metadata(image):
    metadata = image.info.copy()

    metadata['size'] = image.size
    metadata['format'] = image.format.lower()
    metadata['color_mode'] = image.mode

    try:
        metadata.update({
            PIL.ExifTags.TAGS[k]: v
            for k, v in image._getexif().items()
            if k in PIL.ExifTags.TAGS
        })
    except AttributeError:
        pass

    if 'XResolution' in metadata and 'YResolution' in metadata and 'dpi' not in metadata:
        metadata['dpi'] = (metadata['XResolution'][0], metadata['YResolution'][0])

    for name in ['exif', 'icc_profile', 'MakerNote', 'UserComment']:
        if name in metadata:
            del metadata[name]

    return metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('images_path', type=str, help='Path to an image or a folder with images')
    args = parser.parse_args()

    image_paths = get_image_paths(args.images_path)
    for image_path in image_paths:
        try:
            image = PIL.Image.open(image_path)
            print(image_path)
            for key, value in sorted(get_image_metadata(image).items()):
                print('%s: %s' % (key, value))
            print()
            image.close()
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()
