import sys
import click
from local_luminoth import Perception
from compare_results import CompareDetections
import DB
import os


@click.command()
@click.option('--checkpoint', '-c', default='fast',
              help='the name of the checkpoint model to use when processing the images')
@click.option('--save', '-s', default=False, help='Save the image with bounding boxes or not')
@click.option('--images', '-i', multiple=True, default=[], help='list of full paths to images that should be processed')
def main(checkpoint, save, images):
    number_of_passed_tests = 0
    number_of_failed_test = 0
    threshold = 1000  # in milliseconds

    if len(images) > 0:
        my_luminoth = Perception(images, save, checkpoint)
        objects = my_luminoth.run()

        for image in images:
            image_path, image_name = os.path.split(image)
            objects.update({image_name + "_Pass": True})
            comparision = CompareDetections(objects[image_name]["objects"], DB.latest_results)
            accuracy_of_detections = comparision.compare_objects_to_baselines()
            number_of_detections = comparision.evaluate_num_found_objects()
            processing_time = comparision.evaluate_processing_time(objects[image_name]["detection_time"],
                                                  DB.latest_results[image_name]["detection_time"],
                                                  threshold)
            #  TODO: This should be written to a DB of results
            objects[image_name + "_Pass"] = False if not processing_time or \
                                                     not number_of_detections or \
                                                     not accuracy_of_detections else \
                objects[image_name + "_Pass"]
            if objects[image_name + "_Pass"]:
                number_of_passed_tests += 1
            else:
                number_of_failed_test += 1
                print("Image %s failed! Number of detections: %s, Processing time: %s, Accuracy of detections %s"
                      % (image_name, "passed" if number_of_detections else "failed",
                         "passed" if processing_time else "failed",
                         "passed" if accuracy_of_detections else "failed"))
            number_of_tests_run = number_of_passed_tests + number_of_failed_test

            # print(sorted_objects)
        print("%d Tests run;  %d PASSED, %d FAILED" %
              (number_of_tests_run, number_of_passed_tests, number_of_failed_test))
    else:
        print(main.__doc__)
        pass


if __name__ == "__main__":
    main()
    sys.exit(0)