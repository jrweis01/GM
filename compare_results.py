import datetime


class CompareDetections:
    def __init__(self, results, baseline):
        self.results = results
        self.baseline = baseline

    def compare_objects_to_baselines(self):
        # print("comparing results to baseline while taking into account acceptable threshold")
        return True

    def evaluate_processing_time(self, processing_time,baseline_time, threshold):
        delta = self.__subtract_time_stamps(processing_time, baseline_time) - threshold
        return True if delta <= 0 else False

    def evaluate_num_found_objects(self):
        return True if len(self.results) - len(self.baseline["objects"]) == 0 else False

    def __subtract_time_stamps(self, time1, time2):
        ms_time1 = self.__timestamp_to_milliseconds(time1)
        ms_time2 = self.__timestamp_to_milliseconds(time2)
        return ms_time1 - ms_time2

    def __timestamp_to_milliseconds(self, timestamp):
        timestamp = str(timestamp) if isinstance(timestamp, datetime.timedelta) else timestamp
        timestamp.strftime("%H:%M:%S.%f") if isinstance(timestamp, datetime.datetime) else timestamp
        split_time_stamp = timestamp.split(":")
        sec, ms = split_time_stamp[-1].split(".")
        return int(ms[:3]) + (int(sec) * 1000) + (int(split_time_stamp[-2]) * 60000) + \
               (int(split_time_stamp[-3]) * 3600000)

    def split_objects_by_lables(self, objects):
        car_objects = []
        bus_objects = []
        truck_objects = []
        bicycle_objects = []
        person_objects = []
        unknown_objects = []
        bird_objects = []
        potted_plant_objects = []
        cell_phone_objects = []
        all_sorted_objects = {}
        for object in objects:
            if object['label'] == 'bicycle':
                bicycle_objects.append(object)
            elif object['label'] == 'person':
                person_objects.append(object)
            elif object['label'] == 'car':
                car_objects.append(object)
            elif object['label'] == 'truck':
                truck_objects.append(object)
            elif object['label'] == 'bus':
                bus_objects.append(object)
            elif object['label'] == 'cell phone':
                cell_phone_objects.append(object)
            elif object['label'] == 'potted plant':
                potted_plant_objects.append(object)
            elif object['label'] == 'bird':
                bird_objects.append(object)
            else:
                unknown_objects.append(object)

        all_sorted_objects['persons'] = person_objects
        all_sorted_objects['bicycle'] = bicycle_objects
        all_sorted_objects['car'] = car_objects
        all_sorted_objects['bus'] = bus_objects
        all_sorted_objects['truck'] = truck_objects
        all_sorted_objects['cell phone'] = cell_phone_objects
        all_sorted_objects['potted_plants'] = potted_plant_objects
        all_sorted_objects['bird'] = bird_objects
        all_sorted_objects['unknown'] = unknown_objects

        return all_sorted_objects
