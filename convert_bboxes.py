import os
import json
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('split_name', type=str)
    return parser.parse_args()


def convert_bbox(bbox: list[float]):
    return [
        bbox[0] + bbox[2] / 2,
        bbox[1] + bbox[3] / 2,
        bbox[2],
        bbox[3]
    ]


def copy_img(src_img_dir: str, dst_img_dir: str, filename: str):
    os.system(f'cp -u {src_img_dir}/{filename} {dst_img_dir}/{filename}')


def main():
    args = parse_args()
    if args.split_name == 'evaluation':
        annotation_file = open('raw_data/sample_submission/bbox.json', 'r')
    elif args.split_name == 'train':
        annotation_file = open('raw_data/train_bbox_annotations.json', 'r')
    else:
        raise ValueError('No such type of split')

    annotations = json.load(annotation_file)

    src_img_dir = f'raw_data/{args.split_name}_bbox_images'
    yolo_split_name = 'train' if args.split_name == 'train' else 'val'
    dst_img_dir = f'yolo_data/{yolo_split_name}/images'
    dst_labels_dir = f'yolo_data/{yolo_split_name}/labels'

    for image_annotation in annotations['images']:
        copy_img(src_img_dir, dst_img_dir, image_annotation['file_name'])
        label_file = open(f"{dst_labels_dir}/{image_annotation['file_name'].replace('.tif', '.txt')}", 'wt')
        for bbox_annotation in image_annotation['annotations']:
            yolo_bbox = convert_bbox(bbox_annotation['bbox'])
            label_file.write(f"0 {' '.join(str(x) for x in yolo_bbox)}\n")


if __name__ == '__main__':
    main()
