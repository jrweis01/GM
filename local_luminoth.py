import os
import datetime
from luminoth import Detector, read_image, vis_objects


class Perception:
    def __init__(self, list_of_images, to_save_result, checkpoint='accurate'):
        self.list_of_images = list_of_images
        self.to_save_result = to_save_result
        self.checkpoint = checkpoint  # accurate or fast for the luminoth test model

    def run(self):
        """ Detects objects in image and returns list of objects detected.
            Measures the amount of time taken to analyze an image (regardless of the accuracy of the detection)"""
        perception_results = {}
        # If no checkpoint specified, will assume `accurate` by default. In this case,
        # we want to use our traffic checkpoint. The Detector can also take a config
        # object.
        detector = Detector(self.checkpoint)
        for full_image_path in self.list_of_images:
            if os.path.exists(full_image_path):
                image_path, image_name = os.path.split(full_image_path)
                image_ext = image_name.split('.')[-1]
                image = read_image(full_image_path)
                perception_results.update({image_name: {}})
                # Returns a dictionary with the detections.
                start_time = datetime.datetime.now()
                objects = detector.predict(image)
                end_time = datetime.datetime.now()
                time_to_get_objects = end_time - start_time
                # print(objects)
                perception_results[image_name].update({"objects": objects})
                perception_results[image_name].update({"detection_time": time_to_get_objects})
                if self.to_save_result:
                    self.save_image_and_objects(image, image_name, image_ext, objects)
            else:
                print("ERROR: image not found: %s" % full_image_path)
        return perception_results

    def save_image_and_objects(self, image, image_name, image_ext, objects):
        """ Saves the image to a folder of results with a unique file name
            timestamp prevents the files from being over-written
            image nameand checkpoint name help understand what processing was done
            to get the results"""

        timestamp = str(datetime.datetime.now()).replace(':', '_').replace(' ', '_')
        image_output_name = image_name.replace("." + image_ext, "_" + self.checkpoint + "_" +
                                               timestamp + "." + image_ext)
        # If directory does not exist create it
        if not os.path.isdir('.\\results'):
            os.mkdir('.\\results', mode=0o777)
        vis_objects(image, objects).save(os.path.join('.\\results', image_output_name))







