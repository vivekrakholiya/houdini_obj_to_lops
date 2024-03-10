import hou

selectedNodes = hou.selectedNodes()


if len(selectedNodes) == 0:
    print('selected Nodes from obj and try again....')



geoCount=0
lightCount=0
cameCount=0
stage = hou.node('/stage/')

geo_merge_created_check = 0
merge_light_data_to_stream_created_check = 0
cam_merge_all_created_check = 0
materieLibrary_created_check= 0



################################################################################
#  defines inputes
################################################################################




for index,node in enumerate(selectedNodes):
    nodeType = node.type()
    if 'geo' in str(nodeType):
        if index == 0:
            text = "do you want"
            userMaterial_inpute = hou.ui.displayMessage("Do You want to transfer materials ?", buttons=("No", "Yes"))
            if userMaterial_inpute == 1:
                userMaterial_type = hou.ui.displayMessage("materials from Obj assing or assingmaterials attrib !!{FROM ATTRIB IS IN DEV STAGE NOT WORKING NOW)!! ?", buttons=("From OBJ", "From Attrib"))

            if userMaterial_inpute == 1:
                
                materieLibrary = stage.createNode('materiallibrary',"ImportMaterials")
                materieLibrary_created_check = 1
        else:
            pass
        


               
    else:
        pass





###########################################################################
############################################################################
#############################################################################
index = 0
i = 0
for node in selectedNodes:
    nodeType = node.type()
    
    
    
    if 'geo' in str(nodeType):
        sopImportGeo = stage.createNode('sopimport',str(node))
        sopImportGeo.parm('soppath').set(str(node.path()))

        
        if geoCount <= 0:
           
            geo_merge_all = stage.createNode ('merge','merge_all_geo_nodes')
        geo_merge_all.setNextInput(sopImportGeo)
        geo_merge_created_check = 1
            
        geoCount += 1

    if materieLibrary_created_check == 1:
        if index == 0:
            
            if geo_merge_created_check == 1:
                materieLibrary.setNextInput(geo_merge_all)
            else:
                pass

    else:
        pass
    
    
    
            
    if "geo" in str(nodeType):
        if userMaterial_inpute == 1 and userMaterial_type == 0:
            if materieLibrary_created_check == 1:
                materieLibrary.parm('materials').set(str(i+1))
                objMaterielPath = node.parm('shop_materialpath').eval()
                materieLibrary.parm('matnode' + str(i+1)).set(str(objMaterielPath))
                materieLibrary.parm('assign'+str(i+1)).set(1)
                materieLibrary.parm('geopath'+str(i+1)).set('/' + str(node.name()).replace('.','_'))

                

                i+=1



    # if lightCount <= 0:
    if 'hlight' in str(nodeType) or 'envlight' in str(nodeType):
        sopImportLight = stage.createNode('sceneimport::2.0',str(node))
        sopImportLight.parm('filter').set("Lights")
        sopImportLight.parm('objects').set(str(node.path()))
        if lightCount <= 0:
            light_merge_all = stage.createNode('merge','merge_all_lights')

        light_merge_all.setNextInput(sopImportLight)

        if lightCount <= 0:
            merge_light_data_to_stream = stage.createNode('merge','merge_light_to_stream')
            merge_light_data_to_stream_created_check = 1
            merge_light_data_to_stream.setNextInput(light_merge_all)
            if geoCount>= 1:
                if userMaterial_inpute == 1:
                    merge_light_data_to_stream.setNextInput(materieLibrary)
                else:
                    merge_light_data_to_stream.setNextInput(geo_merge_all)

        lightCount +=1
        
    if 'cam' in str(nodeType):
        sopImportCam = stage.createNode('sceneimport::2.0',str(node))
        sopImportCam.parm('filter').set("Cameras")
        sopImportCam.parm('objects').set(str(node.path()))
        if cameCount <= 0:
            cam_merge_all = stage.createNode('merge','merge_all_Cameras')
            cam_merge_all_created_check = 1

        cam_merge_all.setNextInput(sopImportCam)

        if cameCount <= 0:
            merge_cam_data_to_stream = stage.createNode('merge','merge_Cameras_to_stream')
            merge_cam_data_to_stream.setNextInput(cam_merge_all)
            if lightCount >= 1:
                merge_cam_data_to_stream.setNextInput(merge_light_data_to_stream)
            elif geoCount >= 1:
                if userMaterial_inpute == 1:
                    merge_light_data_to_stream.setNextInput(materieLibrary)
                else:
                    merge_light_data_to_stream.setNextInput(geo_merge_all)
            else:
                pass

        cameCount += 1

    
    


    index += 1  
        
   

####################################################################

##########################################################################





stage.layoutChildren()



#############################################################################################

# >>> <hou.OpNodeType for Object hlight::2.0> sceneimport::2.0
# <hou.OpNodeType for Object envlight>

# <hou.OpNodeType for Object cam>
