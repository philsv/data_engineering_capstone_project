// mongo_commands.js

// show dbs;
// use catalog;
// show collections;

// Database interactions
db.electronics.createIndex({"type":1});

db.electronics.find({"price":"laptop"}).count();

db.electronics.find({"type":"smart phone", "screen size": {$eq: 6}}).count();

db.electronics.aggregate(
    [
        {$match: {"type":"smart phone"}},
        {"$group": {
            "_id": null, 
            "average_screen_size": {"$avg": "$screen size"}
            }
        }
    ]
);