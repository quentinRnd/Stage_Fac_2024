def ajout_chemin_data(chemin_ajout):
    instance_chemin={}
    for chemin_ajout in chemin_ajout:
        for noeud1 in chemin_ajout[0]:
            for noeud2 in chemin_ajout[0]:
                if noeud1!=noeud2:
                    instance_chemin[noeud1,noeud2]=chemin_ajout[1]
    return instance_chemin

def ajout_chemin_instance():
    chemin={
    "Instancia1":{
                    #des chemin plutot de entre ville et nature
                    (9,37):[0.3,0.8,0.1,0,0,0.6],(9,35):[0.3,0.8,0.1,0,0,0.6],(9,39):[0.3,0.8,0.1,0,0,0.6]
                    ,(9,44):[0.3,0.8,0.1,0,0,0.6],(9,32):[0.3,0.8,0.1,0,0,0.6],(9,32):[0.3,0.8,0.1,0,0,0.6]
                    ,(9,35):[0.3,0.8,0.1,0,0,0.6]
                    # des chemin plutot de grande nature
                    ,(36,31):[1,0,0.3,0.8,0.5,0.8],(0,31):[1,0,0.3,0.8,0.5,0.8],(9,35):[1,0,0.3,0.8,0.5,0.8]
                    ,(36,41):[1,0,0.3,0.8,0.5,0.8],(31,41):[1,0,0.3,0.8,0.5,0.8],(0,36):[1,0,0.3,0.8,0.5,0.8]
                    #des chemin de ville
                    ,(47,12):[0,1,0.5,0,0,0],(12,24):[0,1,0.5,0,0,0],(47,24):[0,1,0.5,0,0,0]
                    ,(21,12):[0,1,0.5,0,0,0],(38,12):[0,1,0.5,0,0,0],(38,21):[0,1,0.5,0,0,0]
                    ,(38,47):[0,1,0.5,0,0,0],(40,38):[0,1,0.5,0,0,0]

                    #des chemin pres de rivière et de lacs
                    ,(42,43):[1,0,0.4,1,1,1],(42,11):[1,0,0.4,1,1,1],(42,45):[1,0,0.4,1,1,1],(11,45):[1,0,0.4,1,1,1]
                    ,(11,10):[1,0,0.4,1,1,1],(10,34):[1,0,0.4,1,1,1],(10,37):[1,0,0.4,1,1,1],(10,45):[1,0,0.4,1,1,1]
                    ,(10,37):[1,0,0.4,1,1,1],(34,22):[1,0,0.4,1,1,1],(34,7):[1,0,0.4,1,1,1],(34,35):[1,0,0.4,1,1,1]

                    #des chemin de ville avec des lacs
                    ,(23,36):[0.2,1,0.3,0,1,0.3],(23,25):[0.2,1,0.3,0,1,0.3],(23,15):[0.2,1,0.3,0,1,0.3]
                    ,(23,26):[0.2,1,0.3,0,1,0.3],(23,18):[0.2,1,0.3,0,1,0.3],(23,16):[0.2,1,0.3,0,1,0.3]
                    ,(18,26):[0.2,1,0.3,0,1,0.3],(18,36):[0.2,1,0.3,0,1,0.3],(18,17):[0.2,1,0.3,0,1,0.3]
                    ,(18,15):[0.2,1,0.3,0,1,0.3],(41,36):[0.2,1,0.3,0,1,0.3],(36,31):[0.2,1,0.3,0,1,0.3]
                    ,(36,25):[0.2,1,0.3,0,1,0.3],(36,23):[0.2,1,0.3,0,1,0.3],(36,25):[0.2,1,0.3,0,1,0.3]
                    
                    #avec de l'élevation en ville
                    ,(6,45):[0.2,1,0.8,0,1,0.3],(6,3):[0.2,1,0.8,0,1,0.3],(6,27):[0.2,1,0.8,0,1,0.3]
                    ,(6,45):[0.2,1,0.8,0,1,0.3],(6,22):[0.2,1,0.8,0,1,0.3],(6,11):[0.2,1,0.8,0,1,0.3]
                    ,(3,27):[0.2,1,0.8,0,1,0.3],(3,11):[0.2,1,0.8,0,1,0.3],(3,45):[0.2,1,0.8,0,1,0.3]
                    ,(27,45):[0.2,1,0.8,0,1,0.3],(27,10):[0.2,1,0.8,0,1,0.3],(27,7):[0.2,1,0.8,0,1,0.3]

                    #avec de l'élevation en nature
                    ,(40,30):[1,0,0.8,0.4,0.6,0.6],(40,15):[1,0,0.8,0.4,0.6,0.6],(40,25):[1,0,0.8,0.4,0.6,0.6]
                    ,(40,17):[1,0,0.8,0.4,0.6,0.6],(40,18):[1,0,0.8,0.4,0.6,0.6],(40,23):[1,0,0.8,0.4,0.6,0.6]
                    ,(40,2):[1,0,0.8,0.4,0.6,0.6],(32,0):[1,0,0.8,0.4,0.6,0.6],(32,23):[1,0,0.8,0.4,0.6,0.6]
                    ,(32,11):[1,0,0.8,0.4,0.6,0.6]
                }
    }

    instance5_data=[
        [
            #chemin de nature dans la forêt avec certain lac et rivière
            [90,91,89,88,87,86,85,84,83,82],[1,0,0.3,1,0.5,0.8]
        ]
        ,[
            #Chemin de nature avec de l'élévation avec des forêt des rivière
            [80,81,70,71,73,76,77,78,79],[1,0,1,1,0,1]
        ]
        ,[
            #chemin de ville avec des rivière
            [61,62,63,64,65,66,67,68,69,72,74],[0.2,1,0.1,0,0,1]
        ]
        ,[
            #chemin de ville avec des lac et un peu de forêt
            [40,41,42,43,44,45,46,47,48,49,50,51,52],[0.2,1,0.1,0.5,1,0.2]
        ]
        ,[
            #chemin de foret avec des lac et des rivière et de l'élévation           
            [31,32,33,34,35,36,37,38,39],[1,0,1,0.3,0.2,1]
        ]
        ,[
            #chemin de ville avec de l'élévation            
            [53,54,55,56,57,58,59,60],[0,1,1,0,0,0]
        ]
        ,[
            #chemin de ville avec de l'élévation- des lac et des rivière            
            [0,1,2,3,4,5,6,7,8,9,10,11,75],[0,1,1,0,1,1]
        ]
        ,[
            #chemin de foret avec des lac et des rivière et de l'élévation           
            [12,13,14,15,16,17,18,19],[1,0,1,0.3,0.2,1]
        ]
        ,[
            #chemin de ville avec des rivière
            [92,93,94,95,96,97,98,99],[0.2,1,0.1,0,0,1]
        ]
        ,[
            #chemin de nature dans la forêt avec certain lac et rivière
            [0,20,21,22,23,24,25,26,27,28,29,30],[1,0,0.3,1,0.5,0.8]
        ]


    ]

    chemin["Instancia5"]=ajout_chemin_data(instance5_data)
    

    instance6_data=[
        [
            #chemin de nature dans la forêt avec certain lac et rivière
            [40,41,42,43,45,46,47],[1,0,0.3,1,0.5,0.8]
        ]
        ,[
            #Chemin de nature avec de l'élévation avec des forêt des rivière
            [31,32,33,34,35,36,37,38,39],[1,0,1,1,0,1]
        ]
        ,[
            #chemin de ville avec des rivière
            [0,20,21,22,23,24,25,26,27,28,29,30],[0.2,1,0.1,0,0,1]
        ]
        ,[
            #chemin de ville avec des lac et un peu de forêt
            [1,2,3,4,5,6,7,8,9,10,11],[0.2,1,0.1,0.5,1,0.2]
        ]
        ,[
            #chemin de foret avec des lac et des rivière et de l'élévation           
            [12,13,14,15,16,17,18,19],[1,0,1,0.3,0.2,1]
        ]
        
    ]
    chemin["Instancia6"]=ajout_chemin_data(instance6_data)

    instance7_data=[
        [
            #chemin de nature dans la forêt avec certain lac et rivière
            [57,36,61,34,85,67,83,56,8,75],[1,0,0.3,1,0.5,0.8]
        ]
        ,[
            #Chemin de nature avec de l'élévation avec des forêt des rivière
            [19,79,70,24,37,51,46,4,6,75,12,78],[1,0,1,1,0,1]
        ]
        ,[
            #chemin de ville avec des rivière
            [72,74,50,88,52,10,40,73,14,80,3,69],[0.2,1,0.1,0,0,1]
        ]
        ,[
            #chemin de ville avec des lac et un peu de forêt
            [95,13,1,26,71,39,62,17,87,91,45,71,11,27],[0.2,1,0.1,0.5,1,0.2]
        ]
        ,[
            #chemin de foret avec des lac et des rivière et de l'élévation           
            [35,28,5,0,63,92,15,41,84,92,99,23,81,43,18,16,86,21,22,58,68,25],[1,0,1,0.3,0.2,1]
        ]
        ,[
            #chemin de ville avec de l'élévation            
            [20,92,42,44,60,47,89,9,77,30,64,2,97,48,94,7,90,32,81,23,99],[0,1,1,0,0,0]
        ]
    ]
    chemin["Instancia7"]=ajout_chemin_data(instance7_data)


    instance8_data=[
        [
            #chemin de nature dans la forêt avec certain lac et rivière
            [33,6,65,10,11,27,31,20,18,60,9,19,42,30,70,66,36],[1,0,0.3,1,0.5,0.8]
        ]
        ,[
            #Chemin de nature avec de l'élévation avec des forêt des rivière
            [1,23,26,64,47,68,12,43,7,49,61,51,17,41,51,59,13,37,58,13],[1,0,1,1,0,1]
        ]
        ,[
            #chemin de ville avec des rivière
            [50,57,24,63,28,46,5,53,72,52,29,45,15],[0.2,1,0.1,0,0,1]
        ]
        ,[
            #chemin de ville avec des lac et un peu de forêt
            [45,3,16,56,22,44,34,8,69,62,32,25,40],[0.2,1,0.1,0.5,1,0.2]
        ]
        ,[
            #chemin de foret avec des lac et des rivière et de l'élévation           
            [37,58,11,9,19,30,66,48,14,67,0,40,21],[1,0,1,0.3,0.2,1]
        ]
        ,[
            #chemin de ville avec de l'élévation            
            [39,38,2,35,71,36,32],[0,1,1,0,0,0]
        ]
    ]
    chemin["Instancia8"]=ajout_chemin_data(instance8_data)

    instance12_data=[
        [
            #chemin de nature dans la forêt avec certain lac et rivière
            [52,46,70,40,86,58,92,88,50,71,27,2,47,68,76,98,95,7,14,34,43],[1,0,0.3,1,0.5,0.8]
        ]
        ,[
            #Chemin de nature avec de l'élévation avec des forêt des rivière
            [68,95,97,25,87,49,62,77,13,42,62,77,64,5,30,3,10,13,85,79,0,56],[1,0,1,1,0,1]
        ]
        ,[
            #chemin de ville avec des rivière
            [9,32,24,73,66,6,74,82,53,31,89,38,41,45,78,93,8,82,44],[0.2,1,0.1,0,0,1]
        ]
        ,[
            #chemin de ville avec des lac et un peu de forêt
            [48,57,21,96,33,84,11,91,60,75,44,4,15,51,39,94,90,19,1,16],[0.2,1,0.1,0.5,1,0.2]
        ]
        ,[
            #chemin de foret avec des lac et des rivière et de l'élévation           
            [18,36,54,59,79,0],[1,0,1,0.3,0.2,1]
        ]
        ,[
            #chemin de ville avec de l'élévation            
            [72,0,35,81,29,20,55,28,83],[0,1,1,0,0,0]
        ]
    ]
    chemin["Instancia12"]=ajout_chemin_data(instance12_data)

    instance14_data=[
        [
            #chemin de nature dans la forêt avec certain lac et rivière
            [16,93,92,38,91,99,97,95,38,98,43,15,86,44,14,42,57,87,12,96,94,37,85,61,59],[1,0,0.3,1,0.5,0.8]
        ]
        ,[
            #Chemin de nature avec de l'élévation avec des forêt des rivière
            [41,75,23,39,67,22,74,56,72,73,21,4,55,25,40,26,54,24,28,12,80,68,76,77,3,29],[1,0,1,1,0,1]
        ]
        ,[
            #chemin de ville avec des rivière
            [28,12,80,68,24,29,76,77,3,79,1,50,33,78,81,30,51,9,34,35,70,65,66,20,71],[0.2,1,0.1,0,0,1]
        ]
        ,[
            #chemin de ville avec des lac et un peu de forêt
            [83,8,60,6,53,26,18,89,27,76,28,0,82,48,52,69,1,50,30,70,51,31,88,7,11,19,62,10,20,64,63,90,32,66],[0.2,1,0.1,0.5,1,0.2]
        ]
    ]
    chemin["Instancia14"]=ajout_chemin_data(instance14_data)


    instance15_data=[
        [
            #chemin de nature dans la forêt avec certain lac et rivière
            [41,22,23,67,75,39,74,73,72,56,4,25,21,40,58,54,55,26,53,28,12,80,24,68,76,77,3,29,79,50,1,69],[1,0,0.3,1,0.5,0.8]
        ]
        ,[
            #Chemin de nature avec de l'élévation avec des forêt des rivière
            [0,38,14,44,43,15,57,42,86,16,91,85,98,97,17,61,84,5,99,93,92,59,37,87,2,95,13,96,94,60,6,89,45,83,18,8,82,52,27,46,48,7,88,31],[1,0,1,1,0,1]
        ]
        ,[
            #chemin de ville avec des rivière
            [36,47,19,62,10,70,49,11,64,63,90,32],[0.2,1,0.1,0,0,1]
        ]
        ,[
            #chemin de ville avec des lac et un peu de forêt
            [30,51,81,33,9,78,34,20,66,71,35,65],[0.2,1,0.1,0.5,1,0.2]
        ]
        ,[
            #chemin de foret avec des lac et des rivière et de l'élévation           
            [41,0,36,30],[1,0,1,0.3,0.2,1]
        ]
        ,[
            #chemin de ville avec de l'élévation            
            [22,38,47,51],[0,1,1,0,0,0]
        ]
    ]
    chemin["Instancia15"]=ajout_chemin_data(instance15_data)

    instancemoyenne_data=[
        [
            #chemin de nature dans la forêt avec certain lac et rivière
            [19,15,11,7,3],[1,0,0.3,1,0.5,0.8]
        ]
        ,[
            #Chemin de nature avec de l'élévation avec des forêt des rivière
            [2,6,10,14,18],[1,0,1,1,0,1]
        ]
        ,[
            #chemin de ville avec des rivière
            [1,5,9,13,17],[0.2,1,0.1,0,0,1]
        ]
        ,[
            #chemin de ville avec des lac et un peu de forêt
            [16,12,8,4,0],[0.2,1,0.1,0.5,1,0.2]
        ]
        ,[
            #chemin de foret avec des lac et des rivière et de l'élévation           
            [0,3,2,1],[1,0,1,0.3,0.2,1]
        ]
        ,[
            #chemin de ville avec de l'élévation            
            [7,6,9,4],[0,1,1,0,0,0]
        ]
    ]
    chemin["Instanciamoyenne"]=ajout_chemin_data(instancemoyenne_data)

    instancepetite_data=[
        [
            #chemin de nature dans la forêt avec certain lac et rivière
            [3,2],[1,0,0.3,1,0.5,0.8]
        ]
        ,[
            #Chemin de nature avec de l'élévation avec des forêt des rivière
            [0,1],[1,0,1,1,0,1]
        ]
        ,[
            #chemin de ville avec des rivière
            [2,1],[0.2,1,0.1,0,0,1]
        ]
        ,[
            #chemin de ville avec des lac et un peu de forêt
            [2,0],[0.2,1,0.1,0.5,1,0.2]
        ]
        ,[
            #chemin de foret avec des lac et des rivière et de l'élévation           
            [3,0],[1,0,1,0.3,0.2,1]
        ]
        ,[
            #chemin de ville avec de l'élévation            
            [3,1],[0,1,1,0,0,0]
        ]
    ]
    chemin["Instanciapetite"]=ajout_chemin_data(instancepetite_data)


    return chemin
                