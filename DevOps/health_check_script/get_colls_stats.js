// get all dbs stats //
// db.getMongo().setSlaveOk()
rs.secondaryOk();

var alldbs = db.getMongo().getDBNames();

for(var j = 0; j < alldbs.length; j++){
    var db = db.getSiblingDB(alldbs[j]);

    print("\n\n================================== DB: " + db.getName() + " ==================================")
    
    db.getCollectionNames().forEach((c) => 
    {printjson(db.runCommand({
        collStats: c
    }))})
}