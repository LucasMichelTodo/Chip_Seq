#### Importar taules ####

# Diccionari
rosetta <- read.table("/home/lucas/ISGlobal/Gen_Referencies/Gene_references_rosetta.txt", fill = TRUE, fileEncoding = "UTF-8")

# Màx. differència segons transcripció
diff_trans <- read.table("/home/lucas/ISGlobal/Llista_diff_10G_12B.txt", fill = TRUE, fileEncoding = "UTF-8")

# alguna diferència segons transcripció
diff_trans_all <- read.table("/home/lucas/ISGlobal/Llista_diff_10G_12B_all.txt", fill = TRUE, fileEncoding = "UTF-8")

# Differetial peak calling 10G
diff_10G_met <- read.table("/home/lucas/ISGlobal/metil_diff_10G_12B.txt", fill = TRUE, fileEncoding = "UTF-8")
diff_10G_met <- gsub("ID=", "", diff_10G_met[,1], fixed = TRUE)

# Differential peak calling 1.2B
diff_12B_met <- read.table("/home/lucas/ISGlobal/metil_diff_12B_10G.txt", fill = TRUE, fileEncoding = "UTF-8")
diff_12B_met <- gsub("ID=", "", diff_12B_met[,1], fixed = TRUE)

#Comprovant que tots surten al diccionari
diff_10G_met %in% rosetta[,1]
diff_trans[,1] %in% rosetta[,3] | diff_trans[,1] %in% rosetta[,4] | diff_trans[,1] %in% rosetta[,5]


#### Traduïr tots els gens de "diff_trans" ####
for (i in 1:length(diff_trans[,1])){
  if (diff_trans[i,1] %in% rosetta[,3]){
    diff_trans[i,2] <- rosetta[rosetta[,3] %in% diff_trans[i,1],1]
  } else if (diff_trans[i,1] %in% rosetta[,4]){
    diff_trans[i,2] <- rosetta[rosetta[,4] %in% diff_trans[i,1],1]
  } else if (diff_trans[i,1] %in% rosetta[,5]){
    diff_trans[i,2] <- rosetta[rosetta[,5] %in% diff_trans[i,1],1]
  }
}

# Traduïr diff_trans_all ALERTA!!! alguns tenen multiples traduccions!
for (i in 1:length(diff_trans_all[,1])){
  if (diff_trans_all[i,1] %in% rosetta[,3]){
    diff_trans_all[i,2] <- rosetta[rosetta[,3] %in% diff_trans_all[i,1],1][1]
  } else if (diff_trans_all[i,1] %in% rosetta[,4]){
    diff_trans_all[i,2] <- rosetta[rosetta[,4] %in% diff_trans_all[i,1],1][1]
  } else if (diff_trans_all[i,1] %in% rosetta[,5]){
    diff_trans_all[i,2] <- rosetta[rosetta[,5] %in% diff_trans_all[i,1],1][1]
  }
}

#### Gens de diff_trans que estan en un o altra llista dels diffential peak callings ####

# Taula
table(diff_trans[,2] %in% diff_10G_met | diff_trans[,2] %in% diff_12B_met)

# Gens que són a la llista de diff_peaks
diff_trans[diff_trans[,2] %in% diff_10G_met | diff_trans[,2] %in% diff_12B_met,]

# Gens que no són a la llista de diff_peaks
diff_trans[!(diff_trans[,2] %in% diff_10G_met | diff_trans[,2] %in% diff_12B_met),]

#### Gens que surten differencialment metilats que són a la llista de trans ####

table(diff_10G_met %in% diff_trans[,2])
table(diff_12B_met %in% diff_trans[,2])

#### Gens de diff_trans_all que estan en un o altra llista dels diffential peak callings ####

# Taula
table(diff_trans_all[,2] %in% diff_10G_met | diff_trans_all[,2] %in% diff_12B_met)

# Gens que són a la llista de diff_peaks
diff_trans_all[diff_trans_all[,2] %in% diff_10G_met | diff_trans_all[,2] %in% diff_12B_met,]

# Gens que no són a la llista de diff_peaks
diff_trans_all[!(diff_trans_all[,2] %in% diff_10G_met | diff_trans_all[,2] %in% diff_12B_met),]

#### Gens que surten differencialment metilats que són a la llista de trans ####

table(diff_10G_met %in% diff_trans_all[,2])
table(diff_12B_met %in% diff_trans_all[,2])
