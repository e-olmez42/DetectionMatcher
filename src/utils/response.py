from sdks.novavision.src.helper.package import PackageHelper
from components.DetectionMatcher.src.models.DetectionMatcherModel import (
    DetectionMatcher, 
    PackageConfigs, 
    ConfigExecutor, 
    DetectionMatcherOutputs, 
    DetectionMatcherResponse, 
    DetectionMatcherExecutor, 
    OutputDetections
)

def build_response(context):
    output_detections_obj = OutputDetections(value=context.outputDetections)
    
    outputs = DetectionMatcherOutputs(outputDetections=output_detections_obj)
    packageResponse = DetectionMatcherResponse(outputs=outputs)
    packageExecutor = DetectionMatcherExecutor(value=packageResponse)
    
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    
    package = PackageHelper(packageModel=DetectionMatcher, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    
    return packageModel
