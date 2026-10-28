from PIL import Image
import time

class QuadTreeNode:
    def __init__(self, bounds, color=None):
        self.bounds = bounds # (x1, y1, x2, y2)
        self.color = color
        self.quadrants = [None] * 4

    # check if node if a pixel (not quadrant with many pixels)
    def is_pixel(self):
        if (self.bounds[0] == self.bounds[2]) and \
           (self.bounds[1] == self.bounds[3]):
            return True
        return False

    # retruns quadrant index for given point inside the current node
    def get_quadrant_index(self, point):
        x, y = point
        mid_x = (self.bounds[0] + self.bounds[2]) // 2
        mid_y = (self.bounds[1] + self.bounds[3]) // 2
        
        if x <= mid_x:
            if y <= mid_y:
                return 0
            else:
                return 1
        else:
            if y <= mid_y:
                return 3
            else:
                return 2

    # returns bounds for given quadrant inside the current node
    def get_quadrant_bounds(self, quadrant_index):
        x1, y1, x2, y2 = self.bounds

        mid_x = ((x1 + x2) // 2)
        mid_y = ((y1 + y2) // 2)
        
        if quadrant_index == 0:
            return (x1, y1, mid_x, mid_y)
        elif quadrant_index == 1:
            return (x1, mid_y + 1, mid_x, y2)
        elif quadrant_index == 2:
            return (mid_x + 1, mid_y + 1, x2, y2)
        elif quadrant_index == 3:
            return (mid_x + 1, y1, x2, mid_y)


# QuadTree compressed image representation
class QTCimage:
    def __init__(self, image, threshold):
        self.root = None
        self.threshold = threshold
        self.count_of_nodes = 0

        self.__build_tree_compressed(image)

    def __build_tree(self, image):
        width, height = image.size
        bounds = (0, 0, width - 1, height - 1)

        # root is always element without color
        # cause root is like a pointer to tree
        self.root = QuadTreeNode(bounds)
        self.count_of_nodes = 1

        # insert all pixels in the tree
        def __insert_recursion(node):
            if node.is_pixel():
                node.color = image.getpixel((node.bounds[0], node.bounds[1]))
                return

            for i in range(4):
                if ((i == 1 or i == 2) and node.bounds[1] == node.bounds[3]) or \
                    ((i == 2 or i == 3) and node.bounds[0] == node.bounds[2]):
                    # special cases if node is a vertical or horizontal line
                    continue
                bounds = node.get_quadrant_bounds(i)
                node.quadrants[i] = QuadTreeNode(bounds)
                self.count_of_nodes += 1

                __insert_recursion(node.quadrants[i])
            
        __insert_recursion(self.root)
        
    def __build_tree_compressed(self, image):
        width, height = image.size
        bounds = (0, 0, width - 1, height - 1)

        # root is always element without color
        # cause root is like a pointer to tree
        self.root = QuadTreeNode(bounds)
        self.count_of_nodes = 1

        def set_average_color(node):
            colorR = 0; colorG = 0; colorB = 0
            k = 0
            sums = []

            for quadrant in node.quadrants:
                if (quadrant is None) or ((quadrant.color is None) and (quadrant.is_pixel())):
                    # if (quadrant is a pixel) and (it has no color) so we can just remove it
                    continue
                elif (quadrant.color is None) and (not quadrant.is_pixel()):
                    # if (quadrant is not a pixel) and (it has no color) so we can't just remove it
                    # because this quandrant can contain pixels in child quadrants
                    return False
            
                # check if colors are similar with threshold
                currentSum = sum(quadrant.color)
                for summ in sums:
                    if abs(summ - currentSum) >= self.threshold:
                        return False
                sums += [currentSum]

                # calculate colors
                colorR += quadrant.color[0]
                colorG += quadrant.color[1]
                colorB += quadrant.color[2]
                k += 1

            if k > 0:
                node.color = (colorR // k, colorG // k, colorB // k)
            return True

        # insert all pixels in the tree
        def __insert_recursion(node):
            if node.is_pixel():
                node.color = image.getpixel((node.bounds[0], node.bounds[1]))
                return

            for i in range(4):
                if ((i == 1 or i == 2) and node.bounds[1] == node.bounds[3]) or \
                    ((i == 2 or i == 3) and node.bounds[0] == node.bounds[2]):
                    # special cases if node is a vertical or horizontal line
                    continue
                bounds = node.get_quadrant_bounds(i)
                node.quadrants[i] = QuadTreeNode(bounds)
                self.count_of_nodes += 1
                __insert_recursion(node.quadrants[i])

            if set_average_color(node): # sets average color if it's possible
                for i in range(3, 0-1, -1):
                    if node.quadrants[i] is not None:
                        self.count_of_nodes -= 1
                        del node.quadrants[i]
            
        __insert_recursion(self.root)

    def get_image(self):
        width = self.root.bounds[2] + 1
        height = self.root.bounds[3] + 1
        img = Image.new("RGB", (width, height))
        
        def postorder_traversal(node):
            if node is None:
                return

            for quadrant in node.quadrants:
                postorder_traversal(quadrant)

            if node.color is not None: # if node is a pixel or sector
                for x in range(node.bounds[0], node.bounds[2] + 1):
                    for y in range(node.bounds[1], node.bounds[3] + 1):
                        img.putpixel((x, y), node.color)
                

            
        postorder_traversal(self.root)
        return img

    def show(self):
        image = self.get_image()
        image.show()
    
    def save(self, file_path):
        image = self.get_image()
        image.save(file_path, format="JPEG")