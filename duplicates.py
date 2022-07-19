
my_shp = 'test_poly.shp'
my_tbl = 'test_poly_FindIdentical1.dbf'

#create count of each feature sequence from Find Identical table 
recordHist={}
with arcpy.da.SearchCursor(my_tbl, ["IN_FID", "FEAT_SEQ"]) as rows:
    for row in rows:
        recordHist[row[1]]=recordHist.get(row[1], 0) + 1

#assign FIDs as dup or not (sequences with count>1 are duplicates)
idDupHist={}
with arcpy.da.SearchCursor(my_tbl, ["IN_FID", "FEAT_SEQ"]) as rows:
    for row in rows:
        if recordHist[row[1]]>1:
            idDupHist[row[0]]='Y'
        else:
            idDupHist[row[0]]='N'

#update shape file
with arcpy.da.UpdateCursor(my_shp, ["FID","is_dup"]) as rows:
    for row in rows:
        if idDupHist[row[0]]=="Y":
            row[1]=1
        else:
            row[1]=0
        rows.updateRow(row)  
