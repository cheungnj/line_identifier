#!/usr/bin/env python
import argparse
import csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='csv file containing 2D points')
    args = parser.parse_args()
    points = parse_points(args.file)
    identify_lines(points)


def parse_points(filename):
    points = []
    with open(filename, 'rU') as f:
        reader = csv.reader(f)
        # assumes each point is a comma separated entry in column A of the spreadsheet
        # ex. 1A = 0.0,0.0
        for line in reader:
            point = [float(coord) for coord in line[0].split(',')]
            points.append(tuple(point))
    return points


def identify_lines(points):
    slopes = {}
    for i in range(len(points)):
        p1 = points[i]
        for j in range(i + 1, len(points)):
            p2 = points[j]
            # slope = (y2 - y1) / (x2 - x1)
            numerator = p2[1] - p1[1]
            denominator = p2[0] - p1[0]

            if denominator == 0:
                # vertical line has undefined slope and the x coordinate is used to mark this line as unique
                # because there could be multiple vertical lines
                slope = 'undefined-{}'.format(p2[0])
            else:
                # https://docs.python.org/2/tutorial/floatingpoint.html#representation-error
                # floats are represented by python weirdly so we use string formatting to 15 decimals
                # 15 decimals because 16 and 17 weren't working as I expected
                slope = format(numerator / denominator, '.15f')
            # use a set so we don't have duplicate points
            line_points = slopes.get(slope, set())
            line_points.add(points[i])
            line_points.add(points[j])
            slopes[slope] = line_points

    # convert the set to a list because writerows expects a sequence not a set
    lines = [list(v) for v in slopes.values() if len(v) >= 3]
    with open('result.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(lines)


if __name__ == '__main__':
    main()
