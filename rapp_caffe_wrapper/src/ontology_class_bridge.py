#!/usr/bin/env python

#Copyright 2015 RAPP

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# Author: Athanassios Kintsakis
# contact: akintsakis@issel.ee.auth.gr

import rospy
import sys
from os.path import expanduser
from app_error_exception import AppError
from rapp_platform_ros_communications.srv import (
  ontologyClassBridgeSrv,
  ontologyClassBridgeSrvResponse  
  )

## @class OntologyClassBridge
# @brief Contains the necessary functions for translating caffe classes to ontology classes
class OntologyClassBridge:

  ## @brief Implements the getOntologyClassEquivalent service main function
  # @param req [rapp_platform_ros_communications::ontologyClassBridgeSrvRequest::Request&] The ROS service request
  #
  # @return res [rapp_platform_ros_communications::ontologyClassBridgeSrvResponse::Response&] The ROS service response
  # @exception Exception KeyError  
  def getOntologyClassEquivalent(self,req):
    try:      
      res=ontologyClassBridgeSrvResponse()      
      mapFile = home = expanduser("~")+rospy.get_param("ontology_class_bridge_file")
      caffeToOntologyClassesDict=self.loadMappingIntoDictionary(mapFile)
      if (req.caffeClass in caffeToOntologyClassesDict):
        res.ontologyClass=caffeToOntologyClassesDict[req.caffeClass]  
        res.existsInOntology=True
      else:
        res.existsInOntology=False
        res.ontologyClass="SpatialThing-Localized-Unspecified"
      res.success=True     
    
    except KeyError, e:
      res.success=False
      res.trace.append('"KeyError, probably caffe class does not exist or no ontology equivalent exists for "%s"' % str(e))
      res.error='"KeyError, probably caffe class does not exist or no ontology equivalent exists for "%s"' % str(e)
    return res

  ## @brief Loads the caffeToOntologyClasses file into a dictionary
  # @param mapFilePath [string] The path to the file containing the caffe to ontology classes equivalencies
  #
  # @return caffeToOntologyClassesDict [dictionary] The dictionary containing the caffe to ontology classes 
  def loadMappingIntoDictionary(self,mapFilePath):
    with open(mapFilePath) as f:
      lines = f.read().splitlines()
    caffeToOntologyClassesDict=dict()
    for s in lines:
      currentList=s.split("\t")
      if(len(currentList)>=3):        
        caffeToOntologyClassesDict[currentList[1]]=currentList[2]        
    return caffeToOntologyClassesDict
