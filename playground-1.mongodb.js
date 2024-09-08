use("projectDatabase");
// Connect to the database and collection
// const db = client.db(projectDatabase); // Replace with your database name
// const collection = db.collection(task); // Replace with your collection name
db.collection.drop();
// Define the document to insert
testTask = {
    task_name: "Sample Task 2",
    description: "This is a sample task for testing.",
    priority: "High",
    tags: ["testing", "mongodb"],
    stage: "Planning",
    assignee: ["Jane Doe"]
};

// Insert the document into the collection
db.collection.insertOne(testTask);

// Confirm the insertion
"Document inserted successfully.";

db.collection.find().pretty();

db.product_backlog.deleteOne({ task_name: "Sample Task" });

db.collection.find().pretty();
