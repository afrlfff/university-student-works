from PIL import Image # "pip install pillow" may be needed
import os
import time
from pathlib import Path
from matplotlib import pyplot as plt

from QTCimage import QTCimage

# constants
WORKSPACE_FOLDER = os.getcwd()
INPUT_IMG_FOLDER = os.path.join(WORKSPACE_FOLDER, "img")

OUTPUT_FOLDER = os.path.join(WORKSPACE_FOLDER, "results")
OUTPUT_IMG_FOLDER = os.path.join(OUTPUT_FOLDER, "img")

GRAPHICS_FOLDER = os.path.join(OUTPUT_FOLDER, "graphics")
GRAPHICS_SIZES_FOLDER = os.path.join(GRAPHICS_FOLDER, "sizes")
GRAPHICS_TIME_FOLDER = os.path.join(GRAPHICS_FOLDER, "time")
GRAPHICS_COUNT_OF_NODES_FOLDER = os.path.join(GRAPHICS_FOLDER, "count_of_nodes")

THRESHOLDS = [i for i in range(0, 700 + 1, 50)]
RED_COLORS = []
step = (0.5 / (len(THRESHOLDS) - 1))
for i in range(len(THRESHOLDS)):
    RED_COLORS.append((float(1 - i * step), 0, 0)) 

def filename_without_ext(filename):
    return filename.split('.')[0]
def filename_ext(filename):
    return filename.split('.')[1]

# count of nodes for each image with different thresholds
count_of_nodes = []
# text formatting
START_BOLD = r"$\bf{"
END_BOLD = "}$"

# options
MEASURE_INPUT_IMG_SIZES = False
MEASURE_TIME = False
MEASURE_COUNT_OF_NODES = True
MEASURE_OUTPUT_IMG_SIZES = False

PLOT_TIME = False
PLOT_IMG_SIZES = False
PLOT_COUNT_OF_NODES = True
SINGLE_PLOT = False
SHOW_GRAPHICS = True


# Main

if MEASURE_INPUT_IMG_SIZES:
    # SETTING INPUT_IMG_FILENAMES
    INPUT_IMG_FILENAMES = []
    for filename in os.listdir(INPUT_IMG_FOLDER):
        if os.path.isfile(os.path.join(INPUT_IMG_FOLDER, filename)):
            INPUT_IMG_FILENAMES.append(filename)
    
    file = open(os.path.join(OUTPUT_FOLDER, "input_sizes.txt"), "w")
    file.write("Filename | Size (Kbytes)\n\n")

    # MEASURING
    for filename in INPUT_IMG_FILENAMES:
        file_path = Path(os.path.join(INPUT_IMG_FOLDER, filename))
        file_size = file_path.stat().st_size
        file_size /= 1024 # to get Kbytes

        file_size_str = str(f"%.3f" % file_size)

        print(filename + " | " + file_size_str)
        file.write(filename + " | " + file_size_str + '\n')

if (MEASURE_TIME) or (MEASURE_COUNT_OF_NODES):
    INPUT_IMG_FILENAMES = []
    for filename in os.listdir(INPUT_IMG_FOLDER):
        if os.path.isfile(os.path.join(INPUT_IMG_FOLDER, filename)):
            INPUT_IMG_FILENAMES.append(filename)

    if MEASURE_TIME and MEASURE_COUNT_OF_NODES:
        timeKeeper = 0.0
        file_time = open(os.path.join(OUTPUT_FOLDER, "times.txt"), "w")
        file_time.write("Filename | Threshold | TimeToBuildTree(seconds) | TimeToGetImage(seconds)\n\n")
        file_count = open(os.path.join(OUTPUT_FOLDER, "count_of_nodes.txt"), "w")
        file_count.write("Filename | Threshold | CountOfNodes\n\n")

        for filename in INPUT_IMG_FILENAMES:
            for threshold in THRESHOLDS:
                image = Image.open(os.path.join(INPUT_IMG_FOLDER, filename))
                
                start_time = time.perf_counter()
                new_image = QTCimage(image, threshold)
                end_time = time.perf_counter()
                timeKeeper = (end_time - start_time)
                print("File: " + filename + \
                      " | Threshold = " + str(threshold) + \
                      " | Time to build tree: "+ str(f"%.3f" % timeKeeper) + " seconds")
                file_time.write(filename + " | " + str(threshold) + " | " + str(f"%.3f" % timeKeeper) + " | ")
                print("File: " + filename + \
                      " | Threshold = " + str(threshold) + \
                      " | Count of nodes = " +  str(new_image.count_of_nodes))
                file_count.write(filename + " | " + str(threshold) + " | " + str(new_image.count_of_nodes) + '\n')
                
                start_time = time.perf_counter()
                new_image.save(os.path.join(OUTPUT_IMG_FOLDER, filename_without_ext(filename) + "_" + str(threshold) + ".jpg"))
                end_time = time.perf_counter()
                timeKeeper = (end_time - start_time)
                print("File: " + filename + \
                      " | Threshold = " + str(threshold) + \
                      " | Time to get image: "+ str(f"%.3f" % timeKeeper) + " seconds")
                file_time.write(str(f"%.3f" % timeKeeper) + '\n')
    elif MEASURE_TIME:
        file = open(os.path.join(OUTPUT_FOLDER, "times.txt"), "w")
        file.write("Filename | Threshold | TimeToBuildTree(seconds) | TimeToGetImage(seconds)\n\n")
        timeKeeper = 0.0
        for filename in INPUT_IMG_FILENAMES:
            for threshold in THRESHOLDS:
                image = Image.open(os.path.join(INPUT_IMG_FOLDER, filename))
                
                start_time = time.perf_counter()
                new_image = QTCimage(image, threshold)
                end_time = time.perf_counter()
                timeKeeper = (end_time - start_time)
                print("File: " + filename + \
                      " | Threshold = " + str(threshold) + \
                      " | Time to build tree: "+ str(f"%.3f" % timeKeeper) + " seconds")
                file.write(filename + " | " + str(threshold) + " | " + str(f"%.3f" % timeKeeper) + " | ")
                
                start_time = time.perf_counter()
                new_image.save(os.path.join(OUTPUT_IMG_FOLDER, filename_without_ext(filename) + "_" + str(threshold) + ".jpg"))
                end_time = time.perf_counter()
                timeKeeper = (end_time - start_time)
                print("File: " + filename + \
                      " | Threshold = " + str(threshold) + \
                      " | Time to get image: "+ str(f"%.3f" % timeKeeper) + " seconds")
                file.write(str(f"%.3f" % timeKeeper) + '\n')
    elif MEASURE_COUNT_OF_NODES:
        file = open(os.path.join(OUTPUT_FOLDER, "count_of_nodes.txt"), "w")
        file.write("Filename | Threshold | Count of nodes\n\n")
        for filename in INPUT_IMG_FILENAMES:
            for threshold in THRESHOLDS:
                image = Image.open(os.path.join(INPUT_IMG_FOLDER, filename))
                
                new_image = QTCimage(image, threshold)
                print("File: " + filename + \
                      " | Threshold = " + str(threshold) + \
                      " | Count of nodes = " +  str(new_image.count_of_nodes))
                file.write(filename + " | " + str(threshold) + " | " + str(new_image.count_of_nodes) + '\n')

if MEASURE_OUTPUT_IMG_SIZES:
    # SETTING OUTPUT_FILENAMES
    OUTPUT_FILENAMES = []
    for filename in os.listdir(OUTPUT_IMG_FOLDER):
        if os.path.isfile(os.path.join(OUTPUT_IMG_FOLDER, filename)):
            OUTPUT_FILENAMES.append(filename)
    
    file = open(os.path.join(OUTPUT_FOLDER, "output_sizes.txt"), "w")
    file.write("Filename | Threshold | Size (Kbytes)\n\n")

    # MEASURING
    for filename in OUTPUT_FILENAMES:
        new_filename = filename.split('_')[0] + '.' + filename_ext(filename)
        threshold = int(filename_without_ext(filename).split('_')[1])

        file_path = Path(os.path.join(OUTPUT_IMG_FOLDER, filename))
        file_size = file_path.stat().st_size
        file_size /= 1024 # to get Kbytes

        file_size_str = str(f"%.3f" % file_size)

        print(new_filename + " | " + str(threshold) + " | " + file_size_str)
        file.write(new_filename + " | " + str(threshold) + " | " + file_size_str + '\n')

if PLOT_IMG_SIZES:
    file = open(os.path.join(OUTPUT_FOLDER, "output_sizes.txt"), "r")

    prev_image_name = ""
    graph_points = [[], []]
    all_graph_points = []
    iteration_number = 0
    for line in file.readlines()[2:]:
        iteration_number += 1
        threshold = int(line.split(' | ')[1])
        size = float(line.split(' | ')[2])
        image_name = filename_without_ext((line.split(' | ')[0]))
        
        if (image_name != prev_image_name) and (iteration_number != 1):
            all_graph_points.append([graph_points[0].copy(), graph_points[1].copy()])
            if not SINGLE_PLOT:
                plt.plot(graph_points[0], graph_points[1], marker='o', color='red')
                plt.title(START_BOLD + "ImageSizes" + END_BOLD + '\n' + \
                            START_BOLD + '[' + END_BOLD + \
                            START_BOLD + prev_image_name + END_BOLD + \
                            START_BOLD + ".jpg" + END_BOLD + \
                            START_BOLD + ']' + END_BOLD)
                plt.xlabel("Threshold")
                plt.ylabel("Size [Kb]")
                if SHOW_GRAPHICS:
                    plt.show()
                plt.savefig(os.path.join(GRAPHICS_SIZES_FOLDER, prev_image_name + ".png"))
                plt.clf()

            graph_points[0].clear()
            graph_points[1].clear()
            graph_points[0].append(threshold)
            graph_points[1].append(size)
        else:
            graph_points[0].append(threshold)
            graph_points[1].append(size)
        
        prev_image_name = image_name

    if SINGLE_PLOT:
        iteration_number = 0
        for points in all_graph_points:
            plt.plot(points[0], points[1], marker='o', color=RED_COLORS[iteration_number])
            iteration_number += 1
        plt.title(START_BOLD + "ImageSizes" + END_BOLD)
        plt.xlabel("Threshold")
        plt.ylabel("Size [Kb]")
        if SHOW_GRAPHICS:
            plt.show()
        plt.savefig(os.path.join(GRAPHICS_SIZES_FOLDER, "SINGLE_PLOT.png"))
        plt.clf()

if PLOT_COUNT_OF_NODES:
    file = open(os.path.join(OUTPUT_FOLDER, "count_of_nodes.txt"), "r")

    prev_image_name = ""
    graph_points = [[], []]
    all_graph_points = []
    iteration_number = 0
    for line in file.readlines()[2:]:
        iteration_number += 1
        threshold = int(line.split(' | ')[1])
        count_of_nodes = int(line.split(' | ')[2])
        image_name = filename_without_ext((line.split(' | ')[0]))
        
        if (image_name != prev_image_name) and (iteration_number != 1):
            all_graph_points.append([graph_points[0].copy(), graph_points[1].copy()])
            if not SINGLE_PLOT:
                plt.plot(graph_points[0], graph_points[1], marker='o', color='red')
                plt.title(START_BOLD + "CountOfNodes" + END_BOLD + '\n' + \
                            START_BOLD + '[' + END_BOLD + \
                            START_BOLD + prev_image_name + END_BOLD + \
                            START_BOLD + ".jpg" + END_BOLD + \
                            START_BOLD + ']' + END_BOLD)
                plt.xlabel("Threshold")
                plt.ylabel("Count of nodes")
                if SHOW_GRAPHICS:
                    plt.show()
                plt.savefig(os.path.join(GRAPHICS_COUNT_OF_NODES_FOLDER, prev_image_name + ".png"))
                plt.clf()

            graph_points[0].clear()
            graph_points[1].clear()
            graph_points[0].append(threshold)
            graph_points[1].append(count_of_nodes)
        else:
            graph_points[0].append(threshold)
            graph_points[1].append(count_of_nodes)
        
        prev_image_name = image_name

    if SINGLE_PLOT:
        iteration_number = 0
        for points in all_graph_points:
            plt.plot(points[0], points[1], marker='o', color=RED_COLORS[iteration_number])
            iteration_number += 1
        plt.title(START_BOLD + "CountOfNodes" + END_BOLD)
        plt.xlabel("Threshold")
        plt.ylabel("Count of nodes")
        if SHOW_GRAPHICS:
            plt.show()
        plt.savefig(os.path.join(GRAPHICS_COUNT_OF_NODES_FOLDER, "SINGLE_PLOT.png"))
        plt.clf()

        # zoomed in
        iteration_number = 0
        for points in all_graph_points:
            plt.plot(points[0], points[1], marker='o', color=RED_COLORS[iteration_number])
            iteration_number += 1
        plt.title(START_BOLD + "CountOfNodes" + END_BOLD + '\n' + \
                  START_BOLD + "(zoomed)" + END_BOLD)
        plt.xlabel("Threshold")
        plt.ylabel("Count of nodes")
        plt.xlim(100, 700)
        if SHOW_GRAPHICS:
            plt.show()
        plt.savefig(os.path.join(GRAPHICS_COUNT_OF_NODES_FOLDER, "SINGLE_PLOT_zoomed.png"))
        plt.clf()