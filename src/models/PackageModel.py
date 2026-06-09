from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import  Package, Inputs, Configs, Outputs, Response, Request, Output, Input, Config, Image, Detection, KeyPoints, Connection


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class KeyPoints(KeyPoints):
    confidence: Optional[float] = None


class Detection(Detection):
    keyPoints: Optional[List[KeyPoints]] = None
    connections: Optional[List[Connection]] = None
    imgUID: Optional[str] = None
    segmentType: Optional[str] = None
    angle: Optional[float] = None


class OutputInfer(Output):
    name: Literal["outputInfer"] = "outputInfer"
    value: list
    type: Literal["list"] = "list"

    class Config:
        title = "Detections"

class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: List[Detection]
    type: Literal["list"] = "list"

    class Config:
        title = "Detections"

class ConfigHalfTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class ConfigHalfFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class ConfigHalf(Config):
    """
        Enables half-precision (FP16) inference.
        This significantly reduces memory usage and speeds up inference on compatible GPUs with minimal loss in accuracy.
    """
    name: Literal["Half"] = "Half"
    value: Union[ConfigHalfTrue, ConfigHalfFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Half"
        json_schema_extra = {
            "shortDescription": "Half-Precision (FP16)"
        }

class ConfigDeviceGPU(Config):
    name: Literal["ConfigDeviceGPU"] = "ConfigDeviceGPU"
    configHalf: ConfigHalf
    value: Literal["GPU"] = "GPU"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "GPU"


class ConfigDeviceCPU(Config):
    name: Literal["ConfigDeviceCPU"] = "ConfigDeviceCPU"
    value: Literal["CPU"] = "CPU"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "CPU"


class ConfigDevice(Config):
    """
        Specifies the hardware device for model execution.
        Select 'GPU' for faster, CUDA-accelerated inference, or 'CPU' for standard execution.
    """
    name: Literal["ConfigDevice"] = "ConfigDevice"
    value: Union[ConfigDeviceCPU, ConfigDeviceGPU]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Device"
        json_schema_extra = {
            "shortDescription": "Processing Device"
        }

class CustomFieldStorageID(Config):
    """
           Selects a specific file or resource ID from the internal storage system.
   """
    name: Literal["Id"] = "Id"
    value: int
    type: Literal["number"] = "number"
    field: Literal["filePicker"] = "filePicker"
    restart: Literal[True] = True

    class Config:
        json_schema_extra = {
            "shortDescription": "File Selector",
            "class": "portalium\\storage\\widgets\\FilePicker",
            "options": {
                "multiple": 0,
                "returnAttribute": [
                    "name"
                ],
                "name": "app::logo_wide"
            }
        }
        title = "Storage Source"


class CustomFieldStorage(Config):
    name: Literal["storageID"] = "storageID"
    storageID: CustomFieldStorageID
    value: Literal["storageID"] = "storageID"
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Storage ID"

class ConfigConfidenceThreshold(Config):
    """
        Sets the minimum confidence score required for a detection to be considered valid.
        Values range from 0.0 to 1.0. Higher values reduce false positives but may miss some objects.
    """
    name: Literal["conf_threshold"] = "conf_threshold"
    value: float = Field(default=0.3, ge=0, le=1)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Confidence Threshold"
        json_schema_extra = {
            "shortDescription": "Confidence Threshold"
        }

class ConfigDetectionConfidence(Config):
    """
        Specific confidence threshold for the detection task.
    """
    name: Literal["configDetectionConfidence"] = "configDetectionConfidence"
    value: float = Field(default=0.3, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Detection Confidence"
        json_schema_extra = {
            "shortDescription": "Detection Confidence"
        }

class ConfigKeyPointConfidence(Config):
    """
        Minimum confidence score required for individual keypoints (e.g., joints in Pose estimation) to be visible.
    """
    name: Literal["configKeyPointConfidence"] = "configKeyPointConfidence"
    value: float = Field(default=0.3, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "KeyPoint Confidence"
        json_schema_extra = {
            "shortDescription": "KeyPoint Confidence"
        }

# Detection
class DetectionModels(Config):
    """
    This detection model supports only the detection models provided by Ultralytics.
    For the available models and their details, please refer to the releases at:
    https://github.com/ultralytics/assets/releases.

    Example usage:
    Model = "yolo26n.pt"
    """
    name: Literal["DetectionModels"] = "DetectionModels"
    value: str = "yolo26n.pt"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    restart: Literal[True] = True

    class Config:
        title = "Model"

class DetectionPreTrained(Config):
    detectionModels : DetectionModels
    configDevice: ConfigDevice
    configConfidenceThreshold : ConfigConfidenceThreshold
    name: Literal["PreTrained"] = "PreTrained"
    value: Literal["PreTrained"] = "PreTrained"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "PreTrained"


class DetectionCustomWeight(Config):
    customFieldStorage: CustomFieldStorage
    configDevice: ConfigDevice
    configConfidenceThreshold: ConfigConfidenceThreshold
    name: Literal["CustomWeight"] = "CustomWeight"
    value: Literal["CustomWeight"] = "CustomWeight"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Custom Weight"


class ConfigDetectionModelType(Config):
    """
        Selects the source of the model weights.
        'PreTrained' uses standard Ultralytics models, while 'CustomWeight' allows loading user-trained models.
    """
    name: Literal["ConfigDetectionModelType"] = "ConfigDetectionModelType"
    value: Union[DetectionPreTrained, DetectionCustomWeight]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Model Type"
        json_schema_extra = {
            "shortDescription": "Model Source Type"
        }

class DetectionInputs(Inputs):
    inputImage: InputImage


class DetectionConfigs(Configs):
    configDetectionModelType: ConfigDetectionModelType


class DetectionOutputs(Outputs):
    outputDetections: OutputDetections


class DetectionRequest(Request):
    inputs: Optional[DetectionInputs]
    configs: DetectionConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class DetectionResponse(Response):
    outputs: DetectionOutputs


class DetectionExecutor(Config):
    name: Literal["Detection"] = "Detection"
    value: Union[DetectionRequest, DetectionResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Detection"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# Classification

class ConfigWeightsTop5(Config):
    name: Literal["top5"] = "top5"
    value: Literal["5"] = "5"
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "Top 5"


class ConfigWeightsTop1(Config):
    name: Literal["top1"] = "top1"
    value: Literal["1"] = "1"
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "Top 1"


class ConfigNumPredictions(Config):
    """
        Determines how many top class predictions to return.
        'Top 1' returns the single most likely class, 'Top 5' returns the five most likely classes.
    """
    name: Literal["NumPredictions"] = "NumPredictions"
    value: Union[ConfigWeightsTop1,ConfigWeightsTop5]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Num Predictions"
        json_schema_extra = {
            "shortDescription": "Prediction Count (Top-k)"
        }

class ClassificationModels(Config):
    """
        Specifies the Ultralytics YOLO classification model weight file.
        Example: 'yolo11n-cls.pt'.
    """

    name: Literal["ClassificationModels"] = "ClassificationModels"
    value: str = "yolo11n-cls.pt"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    restart: Literal[True] = True

    class Config:
        title = "Model"
        json_schema_extra = {
            "shortDescription": "Classification Model File"
        }

class ClassificationPreTrained(Config):
    classificationModels: ClassificationModels
    configDevice: ConfigDevice
    configNumPredictions: ConfigNumPredictions
    name: Literal["PreTrained"] = "PreTrained"
    value: Literal["PreTrained"] = "PreTrained"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "PreTrained"


class ClassificationCustomWeight(Config):
    customFieldStorage: CustomFieldStorage
    configDevice: ConfigDevice
    configNumPredictions: ConfigNumPredictions
    name: Literal["CustomWeight"] = "CustomWeight"
    value: Literal["CustomWeight"] = "CustomWeight"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Custom Weight"


class ConfigClassificationModelType(Config):
    """
        Selects the source of the classification model weights (PreTrained vs CustomWeight).
    """
    name: Literal["ConfigClassificationModelType"] = "ConfigClassificationModelType"
    value: Union[ClassificationPreTrained, ClassificationCustomWeight]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Model Type"
        json_schema_extra = {
            "shortDescription": "Model Source Type"
        }

class ClassificationInputs(Inputs):
    inputImage: InputImage


class ClassificationConfigs(Configs):
    configClassificationModelType: ConfigClassificationModelType


class ClassificationOutputs(Outputs):
    outputDetections: OutputDetections


class ClassificationRequest(Request):
    inputs: Optional[ClassificationInputs]
    configs: ClassificationConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class ClassificationResponse(Response):
    outputs: ClassificationOutputs


class ClassificationExecutor(Config):
    name: Literal["Classification"] = "Classification"
    value: Union[ClassificationRequest, ClassificationResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Classification"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# Segmentation

class SegmentModels(Config):
    """
        Specifies the Ultralytics YOLO segmentation model weight file.
        Example: 'yolo11n-seg.pt'.
    """

    name: Literal["SegmentModels"] = "SegmentModels"
    value: str = "yolo11n-seg.pt"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    restart: Literal[True] = True

    class Config:
        title = "Model"
        json_schema_extra = {
            "shortDescription": "Segmentation Model File"
        }

class ConfigIOUThreshold(Config):
    """
        Intersection Over Union (IoU) threshold used for Non-Maximum Suppression (NMS).
        Helps in filtering out overlapping bounding boxes.
    """
    name: Literal["conf_ıou_threshold"] = "conf_ıou_threshold"
    value: float = Field(default=0.3, ge=0, le=1)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Confidence IOU Threshold"
        json_schema_extra = {
            "shortDescription": "IoU Threshold"
        }


class PreTrained(Config):
    segmentModels: SegmentModels
    configDevice: ConfigDevice
    configConfidenceThreshold: ConfigConfidenceThreshold
    configIOUThreshold: ConfigIOUThreshold
    name: Literal["PreTrained"] = "PreTrained"
    value: Literal["PreTrained"] = "PreTrained"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "PreTrained"


class CustomWeight(Config):
    customFieldStorage: CustomFieldStorage
    configDevice: ConfigDevice
    configConfidenceThreshold: ConfigConfidenceThreshold
    configIOUThreshold: ConfigIOUThreshold
    name: Literal["CustomWeight"] = "CustomWeight"
    value: Literal["CustomWeight"] = "CustomWeight"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Custom Weight"


class ConfigModelType(Config):
    """
        Selects the source of the segmentation model weights (PreTrained vs CustomWeight).
    """
    name: Literal["ConfigModelType"] = "ConfigModelType"
    value: Union[PreTrained, CustomWeight]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Model Type"
        json_schema_extra = {
            "shortDescription": "Model Source Type"
        }

class SegmentationInputs(Inputs):
    inputImage: InputImage


class SegmentationConfigs(Configs):
    configModelType : ConfigModelType


class SegmentationOutputs(Outputs):
    outputDetections: OutputDetections


class SegmentationRequest(Request):
    inputs: Optional[SegmentationInputs]
    configs: SegmentationConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class SegmentationResponse(Response):
    outputs: SegmentationOutputs


class SegmentationExecutor(Config):
    name: Literal["Segmentation"] = "Segmentation"
    value: Union[SegmentationRequest, SegmentationResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Segmentation"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# Pose
class PoseModels(Config):
    """
        Specifies the Ultralytics YOLO pose estimation model weight file.
        Example: 'yolo11n-pose.pt'.
    """
    name: Literal["PoseModels"] = "PoseModels"
    value: str = "yolo11n-pose.pt"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    restart: Literal[True] = True

    class Config:
        title = "Model"
        json_schema_extra = {
            "shortDescription": "Pose Model File"
        }

class PosePreTrained(Config):
    poseModels: PoseModels
    configDevice: ConfigDevice
    configDetectionConfidence: ConfigDetectionConfidence
    configKeyPointConfidence: ConfigKeyPointConfidence
    name: Literal["PreTrained"] = "PreTrained"
    value: Literal["PreTrained"] = "PreTrained"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "PreTrained"


class PoseCustomWeight(Config):
    customFieldStorage: CustomFieldStorage
    configDevice: ConfigDevice
    configConfidenceThreshold: ConfigConfidenceThreshold
    name: Literal["CustomWeight"] = "CustomWeight"
    value: Literal["CustomWeight"] = "CustomWeight"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Custom Weight"


class ConfigPoseModelType(Config):
    """
        Selects the source of the pose estimation model weights.
    """
    name: Literal["ConfigPoseModelType"] = "ConfigPoseModelType"
    value: Union[PosePreTrained, PoseCustomWeight]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Model Type"
        json_schema_extra = {
            "shortDescription": "Model Source Type"
        }

class PoseInputs(Inputs):
    inputImage: InputImage


class PoseConfigs(Configs):
    configPoseModelType: ConfigPoseModelType


class PoseOutputs(Outputs):
    outputDetections: OutputDetections


class PoseRequest(Request):
    inputs: Optional[PoseInputs]
    configs: PoseConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class PoseResponse(Response):
    outputs: PoseOutputs


class PoseExecutor(Config):
    name: Literal["Pose"] = "Pose"
    value: Union[PoseRequest, PoseResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Pose"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# General

class ConfigExecutor(Config):
    """
        The main controller for the computer vision pipeline.
        Selects which task (executor) to run: Detection, Classification, Segmentation, or Pose.
    """
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[DetectionExecutor, ClassificationExecutor, SegmentationExecutor, PoseExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Task"
        json_schema_extra = {
            "shortDescription": "Select Vision Task"
        }



class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["capsule"] = "capsule"
    name: Literal["Yolo"] = "Yolo"
