# import the necessary packages
import argparse
import cv2
import os
# construct the argument parser and parse the arguments


curr_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(curr_dir, "data")
image_dir = os.path.join(data_dir, "images")
mask_dir = os.path.join(data_dir, "masks")
output_dir = os.path.join(curr_dir,"output")



if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", type=str, 
        help="path input image on which we'll perform inpainting")
    ap.add_argument("-m", "--mask", type=str, 
        help="path input mask which corresponds to damaged areas")
    ap.add_argument("-a", "--method", type=str, default="telea",
        choices=["telea", "ns"],
        help="inpainting algorithm to use")
    ap.add_argument("-r", "--radius", type=int, default=3,
        help="inpainting radius")
    ap.add_argument("-e", "--example", type=bool, default=False,
        help="run script for sample images")
    args = vars(ap.parse_args())


    is_example = args["example"]
    method = args["method"]
    radius = args["radius"]
    os.makedirs(output_dir, exist_ok=True)
    
    flags = cv2.INPAINT_NS if method == "ns" else cv2.INPAINT_TELEA
    
    if not is_example:
        image_path = args["image"]
        mask_path = args["mask"]

        image = cv2.imread(image_path)
        mask = cv2.imread(mask_path)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        output = cv2.inpaint(image, mask, radius, flags=flags)
        cv2.imwrite("output_image.jpg", output)
    else:
        os.chdir(image_dir)
        image_list = os.listdir()
        os.chdir(mask_dir)
        mask_list = os.listdir()
        for i in range(len(mask_list)):
            image_path = os.path.join(image_dir,image_list[i])
            mask_path = os.path.join(mask_dir,mask_list[i])
            image = cv2.imread(image_path)
            mask = cv2.imread(mask_path)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            print(image_list[i])
            output_file = os.path.join(output_dir,f"{image_list[i]}_output.jpg")
            output = cv2.inpaint(image, mask, radius, flags=flags)
            cv2.imwrite(output_file, output)