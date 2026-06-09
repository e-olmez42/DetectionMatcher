
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DetectionMatcher.src.utils.response import build_response
from components.DetectionMatcher.src.models.PackageModel import PackageModel

class DetectionMatcher(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        self.threshold = self.request.get_param("threshold")
        self.target_attribute = self.request.get_param("targetAttribute")
        
        self.parent_detections = self.request.get_param("inputDetectionsOne")
        self.child_detections = self.request.get_param("inputDetectionsTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def match_detections(self):
        parents = self.parent_detections if self.parent_detections else []
        children = self.child_detections if self.child_detections else []

        for parent in parents:
            parent[self.target_attribute] = False

            px1 = parent["boundingBox"]["left"]
            py1 = parent["boundingBox"]["top"]
            px2 = px1 + parent["boundingBox"]["width"]
            py2 = py1 + parent["boundingBox"]["height"]

            for child in children:
                cx1 = child["boundingBox"]["left"]
                cy1 = child["boundingBox"]["top"]
                cx2 = cx1 + child["boundingBox"]["width"]
                cy2 = cy1 + child["boundingBox"]["height"]

                ix1 = max(px1, cx1)
                iy1 = max(py1, cy1)
                ix2 = min(px2, cx2)
                iy2 = min(py2, cy2)

                if ix2 > ix1 and iy2 > iy1:
                    intersection_area = (ix2 - ix1) * (iy2 - iy1)
                    child_area = child["boundingBox"]["width"] * child["boundingBox"]["height"]

                    if child_area == 0:
                        continue

                    overlap_ratio = intersection_area / child_area

                    if overlap_ratio >= self.threshold:
                        parent[self.target_attribute] = True
                        break

        return parents

    def run(self):
        updated_parents = self.match_detections()
        self.outputDetections = updated_parents
        
        responseModel = build_response(context=self)
        return responseModel

if "__main__" == __name__:
    Executor(sys.argv[1]).run()
