"""
    Matches child detections (e.g., helmets) with parent detections (e.g., persons) 
    from two separate detection lists and outputs the updated parent list.
"""
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Detection, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: List[Detection]
    type: Literal["list"] = "list"

    class Config:
        title = "Detections"

class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: List[Detection]
    type: Literal["list"] = "list"

    class Config:
        title = "Detections"

class TargetAttribute(Config):
    """
        The boolean attribute name to be injected into the parent detection. Example: "hasHelmet"
    """
    name: Literal["AttributeName"] = "AttributeName"
    value: str = Field(default="hasChild")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["e.g., hasHelmet"] = "e.g., hasHelmet"

    class Config:
        title = "Target Attribute"

class Threshold(Config):
    """
        Overlap threshold (Intersection over Child Area). Value between 0.0 and 1.0.
    """
    name: Literal["Threshold"] = "Threshold"
    value: float = Field(ge=0.0, le=1.0, default=0.5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0.0, 1.0]"] = "[0.0, 1.0]"

    class Config:
        title = "Overlap Threshold"

class PackageInputs(Inputs):
    # İki ayrı kaynaktan gelen detection listeleri
    parentDetections: InputDetections
    childDetections: InputDetections

class PackageConfigs(Configs):
    targetAttribute: TargetAttribute
    threshold: Threshold

class PackageOutputs(Outputs):
    # Güncellenmiş ana detection listesini döneceğiz
    outputDetections: OutputDetections

class PackageRequest(Request):
    inputs: Optional[PackageInputs]
    configs: PackageConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class PackageResponse(Response):
    outputs: PackageOutputs

class PackageExecutor(Config):
    name: Literal["DetectionMatcher"] = "DetectionMatcher"
    value: Union[PackageRequest, PackageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "DetectionMatcher"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[PackageExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }

class PackageConfigs(Configs):
    executor: ConfigExecutor

class DetectionMatcherModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DetectionMatcher"] = "DetectionMatcher"
